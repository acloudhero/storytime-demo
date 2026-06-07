# Phase 14 — Local Live Proof Loop

**Phase:** 14A.1 — Local Live Proof Loop Before Cloud (implementation candidate; pending review; NOT locked).
**Scope slices:** 14A.1.B (local live backend / durable read model) and 14A.1.C (first operator proof loop).

This document describes the first real operator proof loop: what it does, how it
persists state, why it is not a fake, and how it stays safe.

## 1. Chosen implementation option

The prompt offered three options. **Option B — a narrow proof-run harness** was
chosen.

- **Option A (full vertical slice)** was rejected because the real assembly /
  publish path can depend on ffmpeg and provider configuration, which makes it
  fragile in a clean local/dev context and risks pulling audio/provider work
  into a round that must not.
- **Option C (mock TTS proof integration)** was viable but still couples the
  proof loop to the TTS-proof subsystem's surface.
- **Option B** gives the strongest visible proof at the lowest risk: it writes
  the *real* durable state contracts (`pipeline_run`, `stage_execution`,
  append-only `event_log`, `stage_artifact`) and a real evidence artifact,
  while remaining deterministic and free of provider/ffmpeg/network paths.

The proof run is therefore backend-owned, durable, and honest: it proves the
state/stage/event/artifact machinery end to end without pretending to have
generated real audio.

## 2. Backend API (loopback only)

Served by `storytime local-live` (default `http://127.0.0.1:8770`). All routes
return JSON. Reads are GET; the single controlled action is POST.

```
GET  /health                         backend health + mode + state-owner metadata
GET  /api/runs                       durable run summaries (newest first)
GET  /api/runs/{run_id}              full run detail (stages, artifacts, events)
GET  /api/runs/{run_id}/artifacts    artifact evidence for the run
GET  /api/runs/{run_id}/events       append-only audit events for the run
POST /api/proof-runs                 controlled proof-run action (see §4)
```

The server binds loopback only (validated by
`storytime.http.server.validate_bind_host`) and enforces a strict origin
allowlist: loopback origins on the bound port plus the Vite dev origins
(`http://localhost:5173`, `http://127.0.0.1:5173`). It never emits a wildcard
`Access-Control-Allow-Origin`, and a request from an unlisted origin is `403`.

## 3. Durable persistence

The proof run is persisted to the actual local SQLite state database
(`runs/state.db`) through the existing `StateStore` contracts — not an in-memory
dictionary. Each proof run:

1. inserts a `pipeline_run` row (status `running`),
2. records four `stage_execution` rows (`ingest`, `governance`, `synthesize`,
   `assemble`), each with an append-only event,
3. writes a real evidence artifact to `runs/<run_id>/proof/evidence.json` and
   records its relative key in `stage_artifact`,
4. updates the run to status `completed` and appends a terminal `RunCompleted`
   event.

Because the state lives in SQLite, **the run history survives a server
restart** — the local-live service opens a fresh database connection per
request, and a restarted process sees every previously persisted run. This is
verified by the test suite (a run created through one connection is read back
through a new one).

## 4. Controlled action safety

`POST /api/proof-runs` accepts only an empty body `{}` or `{"fixture": "<id>"}`
where the id is on a fixed allowlist (currently just `golden-path`, an approved
public-domain CC0 demo fixture already in the repo). The handler rejects:

- any non-object body,
- any unexpected field (e.g. arbitrary `text`, `path`, `url`, `provider`),
- any unknown fixture id, and
- bodies larger than a small fixed cap.

The browser cannot submit story text, file paths, URLs, provider selections, or
credentials. Only bounded fixture metadata (title / source id / licence / text
hash) is recorded; the raw story text is never exposed in the read model or the
evidence artifact.

## 5. Frontend surface

The console gains a **Live Proof Loop** view that distinguishes three states —
*Local Live* (backend connected), *Checking*, and *Backend unavailable* (static
demo only) — and never silently blends static fixture data with live data. It
shows backend health evidence, a durable runs list, run detail (stages,
artifacts with size + sha256, events), a "Run approved proof fixture" button,
and a short "Why this is not just a static page" explanation. Refresh is manual
(with a single one-shot refresh after a proof run); there is no auto-polling and
no browser durable storage.

## 6. Controlled failure / recovery proof (Phase 14B.1)

Phase 14A.1 proved a single successful path. Phase 14B.1 makes the proof loop
harder to dismiss by adding controlled, deterministic **failure** scenarios so a
reviewer can see that the system produces intelligible, durable failure
evidence, not only a green success.

The proof-run action accepts an allowlisted `scenario` (the browser may name
only these; it can never submit arbitrary text, paths, providers, credentials,
or failure messages):

- `success` — all four stages (ingest → governance → synthesize → assemble)
  complete; the run ends `completed` with a `RunCompleted` event and an
  evidence artifact. This is the preserved Phase 14A.1 behaviour.
- `governance_failure` — ingest completes, then governance evaluates to
  *blocked*. The run ends `failed` after two stages: a failed `stage_execution`
  records `error_kind = GovernanceBlocked`, a `GovernanceEvaluated` event
  records the blocked decision, and a terminal `RunFailed` event carries the
  failed stage and a deterministic reason.
- `artifact_validation_failure` — ingest, governance, and synthesize complete,
  then assemble fails deterministic artifact validation. The run ends `failed`
  with `error_kind = ArtifactValidationFailed` and a `RunFailed` event carrying
  the stage and reason.

Both failure scenarios are **real durable state** — a failed run row, a failed
stage execution, append-only events, and an evidence artifact, all in SQLite and
all surviving a server restart — but the failure itself is an *intentional,
controlled proof scenario*, not a real provider or ffmpeg error. No scenario
invokes a provider, ffmpeg, RSS, cloud, or the network. The read model exposes
the failure reason (derived from the first failed stage); the frontend renders
it in a dedicated failure-reason panel and marks the failed stage in the
timeline. Recovery/retry is intentionally **not** implemented here and remains
deferred to Phase 14C.1+ — Phase 14B.1 implements failure *proof* only.

## 7. Deferred (Phase 14C.1+, NOT STARTED)

Real provider-backed TTS, frontend audio/TTS generation, audio playback, RSS
publishing, authentication, and cloud/distributed mode are all future work and
are not part of this proof loop.
