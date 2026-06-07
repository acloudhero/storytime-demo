# StoryTime Architecture Baseline

> **Status:** Canonical candidate — Phase 1 Architecture Baseline.
> **Phase:** Planning. Phase 0 Product Charter is locked. This document, once
> reviewed and locked, is one of the three gates blocking Phase 2.
> **Supersedes:** All legacy (pre-RoundTable) architecture notes. Legacy
> material is reference only and is not canonical.
> **Authority:** This document may transcribe and structure ratified
> decisions. It does not resolve open architectural questions; those are
> listed in Section 22.

## 1. Architecture Summary

StoryTime is a local-first, CLI-driven, observability-native content-to-audio
pipeline. It converts one approved CC0 or US public-domain text into one
podcast-ready audio file, publishes one RSS item, and produces one traceable
journey across the pipeline.

The pipeline is a single Python process in Phase 1–3. Work moves through
ordered stages: `ingest → approve_text → synthesize → approve_audio →
assemble → publish`. A `PipelineRunner` orchestrates these stages. Stages do
not call one another. Each stage receives a serializable `StageInput` DTO and
returns a `StageResult` (which carries a declarative `StateUpdate`, produced
artifacts, and internal events). The runner applies state changes, persists
events, emits telemetry, and constructs the next stage's input.

The architecture rests on a small set of load-bearing decisions, ratified
separately and restated in Section 21:

- `pipeline_run_id` is the durable correlation key. Trace IDs are ephemeral.
- Stages communicate through on-disk artifacts, not shared mutable memory.
- The SQLite state store, the `event_log`, and the artifact files are the
  source of truth. OpenTelemetry is a *view* over that source of truth.
- Only the telemetry adapter module may import OpenTelemetry.
- Approval is a real, persisted pipeline stage, not an interrupt.
- Local-first is implemented so that the boundaries needed for future
  cloud-native deployment are preserved from the start.

## 2. Repository Structure

```
storytime/
├── pyproject.toml
├── README.md
├── Makefile                          # canonical task entrypoints
├── .env.example
├── .gitignore
├── docker-compose.observability.yml  # OTel Collector + Jaeger only
├── docs/
│   ├── product-charter.md            # locked
│   ├── architecture-baseline.md      # this document
│   └── phase-closure-protocol.md     # pending generation
├── config/
│   └── storytime.toml                # default configuration
├── src/
│   └── storytime/
│       ├── __init__.py
│       ├── __main__.py               # python -m storytime
│       ├── cli/
│       ├── runner/                   # PipelineRunner, RunnerContext
│       ├── stages/                   # one module per stage
│       ├── dto/                      # StageInput / StageResult / StateUpdate
│       ├── adapters/
│       │   ├── tts/                  # base + mock + manual_import (+ piper later)
│       │   ├── storage/              # local filesystem now
│       │   └── telemetry/            # OTel adapter + noop adapter
│       ├── manifest/                 # source manifest schema + validator
│       ├── artifacts/                # artifact envelope schema + io
│       ├── state/                    # SQLite store, migrations, DAO
│       ├── events/                   # internal event model (data only)
│       ├── rss/                      # feed builder + validator hook
│       ├── http/                     # local static feed/audio server
│       └── util/                     # hashing, ids, time, fs helpers
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│       ├── texts/                    # CC0 / US-PD sample texts
│       └── manifests/
├── runs/                             # gitignored; per-run working dirs
│   ├── state.db
│   └── <pipeline_run_id>/
│       ├── manifest.json
│       ├── text.txt
│       ├── *.artifact.json           # one envelope per stage output
│       ├── audio.wav | audio.mp3
│       └── episode.metadata.json
└── feed/                             # gitignored; published outputs
    ├── feed.xml
    └── audio/
        └── <episode_guid>.mp3
```

Two deliberate choices: `runs/<pipeline_run_id>/` is a self-contained
directory (mirrors a per-run object-storage prefix); `feed/` is kept separate
from `runs/` because published artifacts are immutable once published and must
not be subject to run-cleanup.

## 3. Python Package / Module Structure

Module responsibilities and the permitted import direction (a lower layer may
never import an upper layer):

```
cli         → orchestration entrypoints; imports runner, dto, adapters, config
runner      → PipelineRunner + RunnerContext; imports stages, dto, state, events
stages      → stage logic; imports dto, artifacts, manifest, events, adapter ifaces
dto         → StageInput / StageResult / StateUpdate; imports events, artifacts
adapters/*  → adapter interfaces + implementations; import dto, events, artifacts
manifest    → manifest schema + loader + validator; imports util only
artifacts   → artifact envelope schema + io; imports manifest, util
state       → SQLite DAO + migrations; imports events, util
events      → internal event dataclasses; imports nothing internal
rss         → feed builder + validator; imports artifacts, manifest, util
http        → local static server; imports config, util only
util        → leaf; imports nothing internal
```

The single rule that prevents structural rot: `events` imports nothing
internal, and `adapters/telemetry` is the only module anywhere that imports
`opentelemetry`. The import direction is enforced mechanically (see
Section 21, decision 11).

## 4. CLI Command Structure

Invocation: `python -m storytime <command>` (or a `storytime` entrypoint).

```
storytime ingest    --text PATH --manifest PATH
        Creates a pipeline_run_id, validates the manifest, writes runs/<id>/,
        persists the run row. Emits TextIngested.

storytime approve   <pipeline_run_id> --stage text|audio --decision approve|reject
        Records an operator approval/rejection. Crosses a linked-trace boundary.

storytime synthesize <pipeline_run_id> --tts mock|manual|piper
        Invokes the selected TTS adapter, writes a WAV audio artifact.

storytime assemble  <pipeline_run_id>
        Encodes MP3, computes duration/size, writes episode.metadata.json.

storytime publish   <pipeline_run_id>
        Copies audio into feed/, regenerates and validates feed.xml.

storytime run       <pipeline_run_id>
        Convenience: runs consecutive non-approval stages, stops at gates.

storytime status    [<pipeline_run_id>]
        Reads SQLite; shows stage states, last events, trace ids.

storytime serve     [--port 8000]
        Starts the local static HTTP server for feed/.

storytime clean     [--older-than 7d] [--keep-published] [--dry-run]
        Applies the retention policy of Section 18.
```

Every substantive command takes or produces a `pipeline_run_id`. `--tts mock`
is a first-class option, not a hidden test flag. There is no single
end-to-end mega-command in Phase 1; the approval gates must remain visible as
discrete operator steps.

## 5. Local State Store Design

A single SQLite database at `runs/state.db`, opened in **WAL mode** to allow
concurrent reads while a stage writes. Five tables:

```sql
CREATE TABLE pipeline_run (
    pipeline_run_id      TEXT PRIMARY KEY,   -- ULID, sortable
    created_at           TEXT NOT NULL,      -- ISO-8601 UTC
    updated_at           TEXT NOT NULL,
    current_stage        TEXT NOT NULL,
    status               TEXT NOT NULL,      -- pending|running|awaiting_approval|completed|failed
    source_manifest_hash TEXT NOT NULL,
    run_dir              TEXT NOT NULL
);

CREATE TABLE stage_execution (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_run_id  TEXT NOT NULL REFERENCES pipeline_run(pipeline_run_id),
    stage_name       TEXT NOT NULL,
    started_at       TEXT NOT NULL,
    ended_at         TEXT,
    status           TEXT NOT NULL,          -- running|succeeded|failed|skipped
    trace_id         TEXT,
    span_id          TEXT,
    parent_trace_id  TEXT,                   -- set across linked-trace boundaries
    error_kind       TEXT,
    error_message    TEXT
);

CREATE TABLE approval (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_run_id   TEXT NOT NULL REFERENCES pipeline_run(pipeline_run_id),
    stage_name        TEXT NOT NULL,         -- approve_text|approve_audio
    decision          TEXT NOT NULL,         -- approved|rejected
    operator          TEXT NOT NULL,
    decided_at        TEXT NOT NULL,
    notes             TEXT,
    inbound_trace_id  TEXT,
    outbound_trace_id TEXT
);

CREATE TABLE event_log (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_run_id  TEXT NOT NULL,
    occurred_at      TEXT NOT NULL,
    event_type       TEXT NOT NULL,
    payload_json     TEXT NOT NULL,
    trace_id         TEXT,
    span_id          TEXT
);

CREATE TABLE published_episode (
    episode_guid     TEXT PRIMARY KEY,       -- ULID, stable across re-publish
    pipeline_run_id  TEXT NOT NULL REFERENCES pipeline_run(pipeline_run_id),
    title            TEXT NOT NULL,
    published_at     TEXT NOT NULL,
    audio_path       TEXT NOT NULL,
    audio_bytes      INTEGER NOT NULL,
    duration_seconds REAL NOT NULL,
    feed_version     INTEGER NOT NULL        -- monotonic per publish
);
```

`event_log` is authoritative: events are written here before any telemetry
emission. Migrations are plain numbered SQL files (`NNNN__name.sql`) tracked
by a `schema_version` table; no migration framework in Phase 1.

Edge cases pre-decided: a crash mid-stage leaves a `running` row with a null
`ended_at`; the runner detects such orphans at startup and requires an
explicit `--resume` or `--abort` rather than recovering silently. A single
operator is assumed; a lock file guards `state.db` against accidental
concurrent runs.

## 6. Source Manifest Schema

The manifest is JSON, validated against a vendored JSON Schema on `ingest`.
The schema is **closed** (`additionalProperties: false`).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "StoryTimeSourceManifest",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "manifest_version", "source_id", "title", "author", "source_url",
    "retrieval_date", "jurisdiction", "license", "text_sha256",
    "text_encoding", "text_path", "language", "approval"
  ],
  "properties": {
    "manifest_version": { "const": 1 },
    "source_id":        { "type": "string", "pattern": "^[a-z0-9-]{3,64}$" },
    "title":            { "type": "string", "minLength": 1 },
    "author":           { "type": "string" },
    "source_url":       { "type": "string", "format": "uri" },
    "retrieval_date":   { "type": "string", "format": "date" },
    "jurisdiction":     { "const": "US" },
    "license":          { "enum": ["CC0-1.0", "PD-US"] },
    "text_sha256":      { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "text_encoding":    { "const": "utf-8" },
    "text_path":        { "type": "string" },
    "language":         { "const": "en" },
    "approval": {
      "type": "object",
      "additionalProperties": false,
      "required": ["approved_by", "approved_at", "review_notes"],
      "properties": {
        "approved_by":  { "type": "string" },
        "approved_at":  { "type": "string", "format": "date-time" },
        "review_notes": { "type": "string" }
      }
    }
  }
}
```

`license` is restricted to two values and `jurisdiction` is fixed at `US`,
consistent with the Product Charter's conservative licensing boundary.
`ingest` recomputes the SHA-256 of the text file; a mismatch against
`text_sha256` is a hard failure. `manifest_version` is a `const`; widening the
schema requires a new version and explicit migration handling.

## 7. Inter-Stage Artifact Format

Every stage output is described by a uniform JSON envelope written next to its
payload file (`<stage>.artifact.json` alongside `<stage>.<ext>`).

```json
{
  "artifact_version": 1,
  "pipeline_run_id": "01J...ULID",
  "stage": "synthesize",
  "produced_at": "2026-05-21T20:00:00Z",
  "payload_kind": "audio.wav",
  "payload_path": "runs/01J.../audio.wav",
  "payload_sha256": "...",
  "payload_bytes": 1234567,
  "depends_on": [
    { "stage": "ingest", "payload_sha256": "..." }
  ],
  "trace_context": {
    "traceparent": "00-<trace-id>-<span-id>-01",
    "tracestate": ""
  },
  "producer": {
    "stage_impl": "synthesize.v1",
    "tts_adapter": "mock",
    "tts_version": "0.0.1"
  }
}
```

`artifact_version` is present from the start so the envelope can evolve safely
behind a dual-version reader. The envelope is the source of truth for the
handoff; the payload file is opaque bytes. `trace_context.traceparent` carries
W3C trace context across stage boundaries (see Section 12). `depends_on` lets
a stage refuse to run if an upstream input has drifted.

## 8. Stage DTO / Runner Context Model

This section transcribes the pre-resolved architecture decision. StoryTime
uses **DTO-style stage contracts as the primary stage boundary**. There is no
mutable god-object `PipelineContext`.

**`RunnerContext`** — a minimal, frozen, runner-level execution context. It
carries only stable orchestration services:

```
RunnerContext (frozen):
    config        : immutable configuration
    clock         : time source (injectable for tests)
    state_store   : SQLite DAO
    telemetry     : TelemetryAdapter (may be NoopTelemetry)
    storage       : StorageAdapter (local filesystem in Phase 1)
```

`RunnerContext` **must not** carry: mutable per-stage business state,
OpenTelemetry `Span` objects, artifact payloads, or stage outputs. It is owned
by the `PipelineRunner` and reconstructed at each process boundary; it is not
itself serializable because it holds live adapter instances.

**`StageInput`** — a per-stage, serializable DTO carrying the business inputs
a stage needs: `pipeline_run_id`, references to input artifacts (paths and
hashes, never payloads), the inbound `traceparent`, and stage-specific
parameters. Because it is serializable, a stage invocation can be persisted,
inspected, and — in future projects' cloud deployment — relocated to a worker.

**`StageResult`** — a per-stage return object with a status discriminant:
`Succeeded`, `AwaitingApproval`, or `Failed`. It carries the produced artifact
references, the internal events emitted, and a `StateUpdate`.

**`StateUpdate`** — a declarative description of the state-store mutations the
stage requires (run-status transition, `stage_execution` row, `approval` row,
`published_episode` row). The runner — not the stage — applies it to SQLite.
This keeps the state store out of stages as shared mutable memory.

**Stage signature:**

```
Stage.run(ctx: RunnerContext, stage_input: StageInput) -> StageResult
```

The DTO carries business data; `RunnerContext` injects cross-cutting services.
The runner builds each `StageInput` from prior artifacts and run state,
invokes the stage, then applies the returned `StateUpdate`, persists events,
and emits telemetry.

> **Assumption A1 (flagged for mediator).** The ratified service list for
> `RunnerContext` does not include a TTS adapter. This document therefore
> treats stage-specific adapters (notably the TTS adapter) as constructor
> dependencies of the relevant stage instance, injected by the runner
> according to `StageInput.tts_adapter_name`. Whether stage-specific adapters
> are constructor-injected or resolved via a registry is a scaffold-level
> detail and is left for Phase 2 confirmation.
>
> **Assumption A2 (flagged for mediator).** This document models `StateUpdate`
> as a component carried inside `StageResult` (a single return value), rather
> than as a separate second return value. Either reading satisfies the
> ratified decision; the bundled form is presented here for a single, clean
> return contract.

## 9. Pipeline Stage Model

A `Stage` is a unit conforming to the `Stage.run` signature in Section 8, with
declared `name`, `inputs`, and `outputs` (artifact kinds). The `PipelineRunner`
is generic: it sequences stages, builds `StageInput` DTOs, invokes `run`,
applies `StateUpdate`, persists events, emits telemetry, transitions run
state, and sets the process exit code.

Phase 1 stages:

| Stage          | Inputs                         | Outputs                        | May return AwaitingApproval |
|----------------|--------------------------------|--------------------------------|-----------------------------|
| `ingest`       | manifest + text paths          | `text.plain` artifact          | no                          |
| `approve_text` | `text.plain`                   | (approval row via StateUpdate) | yes                         |
| `synthesize`   | `text.plain` + text approval   | `audio.wav` artifact           | no                          |
| `approve_audio`| `audio.wav`                    | (approval row via StateUpdate) | yes                         |
| `assemble`     | `audio.wav` + audio approval   | `audio.mp3`, `episode.metadata`| no                          |
| `publish`      | `audio.mp3`, `episode.metadata`| feed.xml + published_episode   | no                          |

**Approval is a real persisted stage.** `approve_text` and `approve_audio`
return `AwaitingApproval`; the runner records the pause and the process exits
cleanly. A subsequent `storytime approve` command records the operator
decision as an `approval` row and unblocks the run. This is the only sound way
to model an arbitrarily long human delay without holding a process open or
introducing a queue.

## 10. Internal Event Model

Internal events are **data only** — frozen dataclasses with no behavior and no
internal imports beyond `datetime`/`typing`. There is **no event bus** in
Phase 1; events are produced by stages, returned inside `StageResult`, and
persisted by the runner.

```
PipelineEvent (frozen):
    event_type       : str
    pipeline_run_id  : str
    occurred_at      : datetime
    stage_name       : str
    payload          : dict   # JSON-serializable, small — paths/hashes only
```

Canonical event types: `RunCreated`, `TextIngested`, `TextApprovalRequested`,
`TextApproved`, `TextRejected`, `SynthesisStarted`, `SynthesisCompleted`,
`SynthesisFailed`, `AudioApprovalRequested`, `AudioApproved`, `AudioRejected`,
`AssemblyCompleted`, `RSSPublished`, `RSSPublishFailed`, `RunCompleted`,
`RunFailed`.

Two rules: events are persisted to `event_log` **before** telemetry emission,
so telemetry being unavailable never loses an event; and no event carries a
large payload — audio bytes never appear in an event, only paths and hashes.

## 11. Telemetry Adapter Design

A single interface with two implementations. The OpenTelemetry implementation
is the **only** module in the codebase permitted to import `opentelemetry`.

```
TelemetryAdapter (interface):
    on_run_started(run_id, attributes)        -> RunHandle
    on_stage_started(run_id, stage, attrs)    -> StageHandle
    on_stage_ended(stage_handle, result)      -> None
    on_event(event: PipelineEvent)            -> None
    on_run_ended(run_handle, status)          -> None
    start_linked_run(run_id, prior_trace_id)  -> RunHandle
```

- `NoopTelemetry` — does nothing; used in tests and when telemetry is disabled.
- `OtelTelemetry` — maps run → root span, stage → child span, event → span
  event plus a counter on a `storytime.events` metric labelled by
  `event_type`; a `Failed` stage records an exception and sets span status to
  error.

OpenTelemetry is a **view** over the source of truth (SQLite + `event_log` +
artifacts), never the source itself. **Decoupling invariant:** deleting
`OtelTelemetry` and running with `NoopTelemetry` must leave every functional
test green. Telemetry export must never block pipeline progress: a bounded
batch processor with a finite shutdown timeout is used, and a collector outage
drops spans with a warning rather than stalling a run.

## 12. Trace-Context and Linked-Trace Strategy

`pipeline_run_id` is the durable correlation key and is the only identifier
guaranteed to connect a run end to end. Trace topology is a derived view.

Three regimes:

1. **Within one CLI invocation:** one root span per run, child spans per
   stage — standard in-process tracing.
2. **Across invocations within a non-approval stage chain:** the next
   invocation reads `trace_context.traceparent` from the most recent artifact
   envelope and sets it as the parent of its new span, producing one connected
   trace across processes.
3. **Across an approval boundary:** the post-approval invocation starts a
   **new trace with a `Link`** to the prior trace, not a continuation.
   Rationale: an operator gate may last hours or days; a single continuous
   span would render an unreadable timeline and a meaningless duration metric.
   The `approval` table's `inbound_trace_id` / `outbound_trace_id` columns,
   together with `stage_execution.parent_trace_id`, let the full chain be
   reconstructed.

Sampling is 100% in Phase 1.

## 13. TTS Adapter Interface

TTS is accessed through a swappable adapter. All adapters **emit WAV only**;
MP3 encoding is the responsibility of the `assemble` stage (Section 14).

```
TTSAdapter (interface):
    name     : str
    version  : str
    synthesize(text: str, *, out_path, voice=None,
               sample_rate_hz=22050) -> TTSResult

TTSResult (frozen):
    audio_path        : Path
    audio_format      : "wav"
    sample_rate_hz    : int
    channels          : int
    duration_seconds  : float
    audio_sha256      : str
```

Phase 1 implementations, both of which must work before Piper is required:

- `MockTTS` — generates a deterministic WAV (e.g., a tone whose duration
  scales with text length). No external dependencies; used in CI and the
  scaffold gate.
- `ManualImportTTS` — verifies and ingests a WAV that the operator generated
  externally and placed at a known path.

`PiperTTS` is a Phase 3 concern; its only obligation is to satisfy this
interface. The selected adapter is identified by `StageInput.tts_adapter_name`
(see Assumption A1 in Section 8).

## 14. RSS / Audio Output Model

The `assemble` stage encodes the WAV to MP3 and writes an
`episode.metadata.json` artifact (episode GUID, title, author, description,
RFC-822 publication date, audio MIME, byte length, duration in seconds and in
`HH:MM:SS`, license attribution, source manifest hash).

The `publish` stage produces two outputs: `feed/audio/<episode_guid>.mp3` and
a regenerated `feed/feed.xml`. `episode_guid` is a ULID generated at first
publish and stored in `published_episode`; it is **stable across re-publishes**
so subscribers never see a duplicate episode.

The feed is RSS 2.0 with the iTunes podcast namespace. Each item carries an
`enclosure` with `url`, `length` (bytes), and `type` (`audio/mpeg`); a `guid`
with `isPermaLink="false"`; an RFC-822 `pubDate`; and `itunes:duration`.
`feed.xml` is written atomically: write to a temp file, validate, then
atomically replace — a partial feed is never served. Feed validity is checked
in the `publish` stage before the replace.

## 15. Local HTTP Serving Model

`storytime serve` runs a minimal static HTTP server over `feed/`. It serves
`/feed.xml` as `application/rss+xml` and `/audio/*.mp3` as `audio/mpeg`, and
**must support HTTP range requests** — mainstream podcast clients issue range
requests for audio, and a server that ignores them will misbehave. The Python
standard-library `http.server` does not handle ranges correctly and is not
used for audio.

The server binds `127.0.0.1` only. The Phase 1–3 threat model is the
operator's own machine; the feed is not exposed to the local network. Any
external exposure (for testing on a phone, for example) is a deliberate,
explicit operator action, not a default.

## 16. Local OpenTelemetry Collector + Jaeger Topology

Observability infrastructure runs via `docker-compose.observability.yml` with
two services:

- **OpenTelemetry Collector** — receives OTLP over gRPC (4317) and HTTP
  (4318); pipeline of `otlp` receiver → `batch` / `memory_limiter` /
  `resource` processors → exporters to Jaeger plus a debug exporter.
- **Jaeger** — all-in-one; trace storage and UI (16686).

All ports bind to `127.0.0.1`. The StoryTime process exports to the local
Collector. If the Collector is down, the pipeline still completes and spans
are dropped with a warning. Docker is used **only** for this observability
stack in the scaffold phase; the StoryTime application itself is not
containerized in Phase 1–3. A metrics backend and a logs backend are deferred;
Jaeger covers traces, which is the signal the MVP's "one traceable journey"
gate depends on.

> Specific Collector and Jaeger image tags are an open Phase 2 prerequisite
> (Section 22) and are not pinned in this document.

> **Documentation note (Phase 7B, not an amendment).** Phases 7A and 7B keep
> the rule in this section intact: the StoryTime *application* is not
> containerized — Docker is for the local observability stack only. Phase 7B's
> blue/green front door is a native Python reverse proxy (standard library,
> uncontainerized), so it introduces no new container and needs no change
> here. This note exists only to record, for any future phase, that
> introducing an application container or image — for a versioned artifact, a
> managed-cloud path, or an orchestrator — would be a material change to this
> section and **requires an explicit Architecture Baseline amendment approved
> by the user**. It must never be introduced as an implementation detail. No
> such amendment is made or implied by Phase 7A or Phase 7B.

> **Amendment note (Phase 7C / 7C.1 — locked).** The amendment anticipated by
> the note above has since been authored (Phase 7C), reviewed by GPT-5.5 and
> Gemini, revised (Phase 7C.1), and **locked** with explicit user approval.
> It amends this section narrowly: **optional, local, single-host, demo-grade
> application containerization** of the existing blue/green slots is now
> permitted. Bare-metal local Python remains the default supported mode;
> Docker remains optional and is never required by the quality gates. The
> amendment authorizes nothing further — no cloud deployment, no image-registry
> publishing, no Kubernetes, no Terraform, no production HA/auth, no
> multi-tenancy, and no vendor telemetry fan-out; each would still require its
> own separate amendment or phase. Hard rules carried by the amendment:
> per-slot named Docker volumes for SQLite state and feed (host bind mounts of
> the state DB are prohibited); loopback-only backend exposure (§15 preserved);
> a stable, slot-derived `service.instance.id` with automatic Docker/host/
> process resource detectors banned; and strictly isolated blue/green state
> with no automated cross-slot migration. The implementation lives in the
> `Dockerfile`, `.dockerignore`, and `docker-compose.app.yml`; see
> `docs/deployment-containerized.md` and `docs/canonical-state.md`. Future app
> containerization beyond this local-demo scope still requires a further
> explicit amendment.

> **Amendment note (Phase 8A — locked).** Phase 8 adds optional,
> Collector-owned telemetry fan-out to external observability backends. The
> governing rules are the Phase 8A amendment in Section 23 of this document,
> which was authored as a candidate, reviewed by GPT-5.5 and Gemini
> (`SAFE TO LOCK`), and **locked** with explicit user approval (2026-05-24).
> Section 23 narrowly amends the Phase 7C / 7C.1 note above: the OpenTelemetry
> Collector — never the StoryTime application — may make explicitly enabled
> outbound telemetry-export calls. The "no vendor telemetry fan-out" statement
> in the Phase 7C / 7C.1 note is superseded to exactly that narrow extent.
> Phase 8A is an architecture/governance amendment only; it implements no
> vendor fan-out (that is the future Phase 8B / 8C).

## 17. Environment / Dependency Strategy

Ratified elements: a `src/` layout; a `pyproject.toml` with PEP 621 metadata;
optional dependency groups separating development tooling, audio handling,
OpenTelemetry, and the (later) Piper TTS engine; static type checking in
strict mode over the core packages; linting; and mechanically enforced import
direction (Section 21, decision 11). `ffmpeg` is expected to be the system-level
audio dependency, with the `Makefile` checking for its presence.

Open and **not resolved in this document** (see Section 22): the exact Python
version floor; the package manager and CLI framework; and whether MP3 encoding
uses `ffmpeg` via subprocess or an in-process encoder. These are Phase 2
prerequisites and the architecture-control rule prevents resolving them here.

## 18. Data Retention and Cleanup Model

Three tiers:

- **Transient** — `runs/<id>/` directories for runs that are `completed` and
  whose episode is recorded in `published_episode`. Eligible for automatic
  cleanup after a default of 7 days.
- **Quarantined** — runs with status `failed` or `awaiting_approval`. Never
  auto-cleaned; they exist for forensic and decision purposes and require an
  explicit operator action to remove.
- **Permanent** — `feed/feed.xml`, `feed/audio/*.mp3`, and `published_episode`
  rows. Not removed by Phase 1 tooling; deletion of a published episode is a
  later, explicitly confirmed operation.

`event_log` rows are retained while the corresponding run directory exists and
are purged when it is removed, keeping the table bounded without losing data
for live runs. `storytime clean` implements these tiers; `--dry-run` is
mandatory on first use, and the cleanup itself emits a `RunsCleaned` event.

## 19. Future Cloud Migration Mapping

Local-first is implemented so the boundaries needed by future projects'
cloud-native deployment are preserved. Indicative mapping:

| Phase 1 (local)                     | Future cloud-native              | Migration cost |
|-------------------------------------|----------------------------------|----------------|
| `runs/<id>/` filesystem             | Object storage, prefix per run   | Low — storage adapter swap |
| `runs/state.db` SQLite              | Managed relational database      | Medium — portable schema, replace DAO |
| `feed/` static directory            | Object storage + CDN             | Low — publish writes via storage adapter |
| Local static HTTP server            | Static hosting behind a CDN      | Trivial — server is a dev convenience |
| In-process stage calls via runner   | Workers behind a queue           | Medium — `StageInput` is already serializable |
| Local Collector + Jaeger            | Managed collector + backend      | Trivial — endpoint configuration |
| `pipeline_run_id` correlation       | Unchanged                        | Zero |
| CLI approval command                | Approval service + thin UI       | Medium — `approval` table is the contract |

The migration is mechanical only while the import-direction rules and adapter
boundaries hold. The largest standing migration risk is a stage bypassing the
storage adapter to touch the filesystem directly.

## 20. Major Risks

Ranked by probability times impact:

1. **Trace continuity across process and approval boundaries** — highest risk;
   the "one traceable journey" gate fails silently if `traceparent`
   propagation and linked traces are implemented incorrectly.
2. **A stage bypassing an adapter** (storage or telemetry) — slow-burn; turns
   the future cloud migration into a rewrite.
3. **MP3 encoding environment inconsistency** — `ffmpeg` present on one
   machine and absent on another (e.g., CI).
4. **RSS feed validity drift** — subtle iTunes-namespace and enclosure
   requirements break podcast-client compatibility quietly.
5. **SQLite integrity on crash** — mitigated by WAL mode and default sync;
   no exotic tuning in Phase 1.
6. **Telemetry export blocking shutdown** — mitigated by a bounded batch
   processor and a finite shutdown timeout.
7. **Manifest schema drift** — mitigated by the closed schema and the
   `manifest_version` `const`.
8. **Audio loudness inconsistency across episodes** — cosmetic; a normalization
   step may be added in `assemble` later.

## 21. Eleven Hard Decisions Ratification Block

These eleven decisions are ratified. Any change to one of them requires
explicit mediator review; they are not safe to revise casually.

1. `pipeline_run_id` is the durable correlation key, not `trace_id`.
2. `adapters/telemetry` is the only module that may import OpenTelemetry.
3. Stages communicate through artifacts, not shared mutable memory.
4. Artifact envelopes carry W3C `traceparent` where applicable.
5. Linked traces are used across approval gates.
6. Approval is a persisted pipeline stage.
7. TTS adapters emit WAV; MP3 encoding lives later in assemble/package.
8. MockTTS and ManualImportTTS work before Piper is required.
9. Internal events are data only; no event bus in Phase 1.
10. Manifest is constrained to CC0 + US public domain and uses a closed schema.
11. Import direction must be mechanically enforceable, preferably with
    import-linter.

## 22. Open Phase 2 Prerequisites

The following are open and are deliberately **not** resolved by this document,
per the architecture-control rule that document-generation rounds may not
resolve open architectural questions. They must be decided before Phase 2
scaffold work begins:

1. **Lock tooling choices** — package manager and CLI framework.
2. **Decide `event_log` semantics** — `event_log` is ratified as a source of
   truth; the remaining open question is whether it is a strictly forensic
   authoritative log or a replayable event store from which telemetry can be
   regenerated on demand. This affects the state DAO contract and must be
   settled before the state layer is scaffolded.
3. **Re-verify the Python version floor** — prior planning figures are treated
   as stale until confirmed.
4. **Re-verify OpenTelemetry Collector and Jaeger image tags.**
5. **Decide the MP3 / ffmpeg strategy** — `ffmpeg` via subprocess versus an
   in-process encoder.
6. **Decide the disposition of the prior external scaffold** — discarded, or
   archived as explicitly non-canonical reference.

Additionally, if future projects' proving-ground use imposes process or
architecture requirements, those must be surfaced before Phase 2.

> Confirmation note for the verification round: two faithful-transcription
> assumptions are flagged in Section 8 (A1: stage-specific adapter injection;
> A2: `StateUpdate` bundled within `StageResult`). These were adopted to keep
> the document concrete and are explicitly offered for mediator correction;
> they are not new architectural decisions.

## 23. Phase 8A Amendment — Collector-Owned Multi-Backend Telemetry Fan-Out

> **Status:** **Locked** — Phase 8A Architecture Baseline amendment, accepted.
> Authored by Claude Opus 4.7 as a Phase 8A candidate; reviewed by GPT-5.5
> (clean); reviewed by Gemini (`SAFE TO LOCK`); locked with explicit user
> approval (2026-05-24). This follows the precedent of the Phase 7C / 7C.1 §16
> amendment — authored as a candidate, then locked. This section is now
> canonical: Phase 8 implementation (Phase 8B, Phase 8C) may depend on it.
> Any further change to it requires a new explicit, user-approved amendment.
> **Scope:** Architecture and governance only. Phase 8A authorized nothing to
> be built; it defines the rules the future Phase 8B (local multi-backend
> stack) and Phase 8C (optional vendor export profiles) must obey.

### 23.1 Why this amendment exists

Phase 8 introduces optional observability fan-out to external telemetry
backends (Dynatrace, New Relic, and possibly others). StoryTime's locked
posture is local-first with no required outbound network calls (§1, §15, §16,
§19). Exporting telemetry to a hosted backend is, by definition, an outbound
network call. Without an explicit amendment Phase 8 would either violate the
local-first baseline or be blocked. This amendment resolves that by
authorizing one narrow, well-fenced exception and codifying the governance
that keeps the exception from eroding the baseline.

The exception, stated once:

> The OpenTelemetry Collector — and only the Collector — may make explicitly
> enabled outbound network calls for observability export. The StoryTime
> application itself remains local-first and must not contain vendor SDKs,
> vendor exporters, or vendor-specific telemetry logic.

### 23.2 Collector-owned fan-out (rule)

Multi-backend telemetry fan-out is owned exclusively by the OpenTelemetry
Collector. Application services emit telemetry only to the configured local
Collector endpoint (`STORYTIME_OTLP_ENDPOINT`, default
`http://127.0.0.1:4318`). The application must never send telemetry directly
to Dynatrace, New Relic, Datadog, Honeycomb, Grafana Cloud, or any other
vendor ingest endpoint. The application produces one OTLP stream to one local
Collector; the Collector alone decides where copies of that stream are routed.

### 23.3 No vendor SDKs in application code (rule)

No vendor-specific Python SDK, agent, or telemetry package may be added to
StoryTime application code or to the `pyproject.toml` runtime dependencies.
Explicitly forbidden (non-exhaustive): Dynatrace Python telemetry packages,
New Relic Python agents, Datadog Python agents (`ddtrace` and the like),
vendor-specific tracing wrappers, proprietary auto-instrumentation agents, and
direct HTTP calls from application code to any vendor ingest API. Generic
OpenTelemetry SDK usage stays exactly as established by Phase 5 —
`opentelemetry-api`, `opentelemetry-sdk`,
`opentelemetry-exporter-otlp-proto-http` — and remains confined to the single
`storytime.adapters.telemetry.otel` module behind the import-linter contract
(§21 decision 2; `docs/telemetry-map.md`). Phase 8 adds no new application
telemetry dependency.

### 23.4 Standard OTLP only (rule)

Vendor fan-out, when later built, uses standard OpenTelemetry protocols from
the Collector. Allowed Collector exporter families: `otlp` (OTLP over gRPC)
and `otlphttp` (OTLP over HTTP). Forbidden unless a future explicit amendment
approves them: proprietary vendor exporters, the Datadog exporter,
vendor-specific agents, sidecar agents, host agents, and proprietary protocol
bridges. If a vendor cannot accept a standard OTLP / OTLP-HTTP ingest path
suitable for this project, that vendor is deferred — vendor-specific
architecture is never forced into StoryTime to accommodate a backend.

### 23.5 The outbound-network exception is narrow (rule)

The local-first constraint of §1 / §15 / §16 / §19 remains fully intact for
core StoryTime operation. The only authorized outbound network exception is
explicitly enabled telemetry export from the OpenTelemetry Collector to
configured observability backends. The following remain mandatory:

- the core application must continue to run with no internet access;
- the entire test suite must continue to run with no internet access and no
  Docker;
- vendor credentials must never be required for local development, tests,
  demos, or default operation.

### 23.6 Disabled-by-default vendor profiles (rule)

Vendor export is disabled by default. `STORYTIME_TELEMETRY=noop` remains the
default telemetry mode (§11; `.env.example`). When telemetry is enabled
(`STORYTIME_TELEMETRY=otel`), local-only Collector routing — to the local
Prometheus / Loki / Jaeger / Grafana stack — must work with no vendor
credentials present. Vendor fan-out is reached only by explicit, additional
environment configuration; absent that configuration the Collector routes
locally and nowhere else. No committed file may contain a real secret, token,
tenant ID, API key, or user-specific vendor endpoint; `.env.example` carries
obvious fake placeholders only.

### 23.7 Secret handling (rule)

All vendor endpoints and tokens are injected through environment variables at
runtime. No secret may be hardcoded in source code, Docker Compose files,
Collector configuration, docs, tests, dashboards, scripts, or Makefile
targets. `.env` remains git-ignored; the existing `*.local.env` /
`*.secret.env` / `*.env.local` git-ignore patterns — reserved in Phase 7C.1
for exactly this purpose — are the home for any vendor credentials.
`.env.example` uses obvious fake placeholders.

### 23.8 Telemetry data hygiene (rule)

Telemetry remains control-plane metadata only. This rule **strengthens, and
never weakens,** the Phase 5 data-hygiene rule (§10, §11;
`storytime.adapters.telemetry.hygiene`). Fanning telemetry out to an external
backend does not change what may be placed into telemetry.

Forbidden telemetry content (non-exhaustive): raw story text, source text,
generated narration text, full RSS XML payloads, full article/source
payloads, secrets, tokens, private user content, large content blobs,
sensitive data, unbounded exception payloads, and high-cardinality arbitrary
text.

Allowed telemetry content (examples): pipeline run ID, story ID, episode ID,
workflow stage, status, retry count, durations, byte counts, artifact hash
references, source/license classification, service name, service version,
deployment slot, environment, error category, and bounded error code.

Traces, logs, and metrics observe control flow, reliability, latency,
retries, cost estimates, and stage health — never data-plane payloads.

### 23.9 Log routing for Phase 8B (rule / direction)

For Phase 8B, logs are routed to Loki via container stdout / Docker log
collection / Collector-supported local routing. StoryTime's Python logging
system is **not** to be rewritten around direct OTLP log export in Phase 8.
Python OTLP log export may be considered only in a later phase, only with a
clear reason, and only under a separate amendment or implementation gate. The
preferred Phase 8 log model:

> the application writes structured logs to stdout; local infrastructure
> routes or scrapes those logs into the observability stack.

This is consistent with `docs/telemetry-map.md`, which records that a separate
in-application structured-logging surface was intentionally not added: Phase
8B adds log *routing* infrastructure, not a new in-app logging system.

### 23.10 Collector resiliency (rule)

Future Phase 8B / 8C Collector configurations must be designed so that vendor
endpoint failure cannot break local StoryTime execution. Required resilience
patterns:

- a `batch` processor on every pipeline;
- a `memory_limiter` processor to bound Collector memory;
- sending queues where the exporter supports them;
- `retry_on_failure` where appropriate;
- graceful disablement when vendor environment variables are empty — a
  disabled vendor profile contributes no exporter to any pipeline;
- no crash loops when vendor profiles are disabled;
- no application dependency on vendor exporter health.

If a vendor endpoint rejects data, times out, rate-limits, or is unreachable,
the StoryTime application must continue to run unaffected. This extends the
existing §11 rule — a Collector outage drops spans with a warning rather than
stalling a run — to also cover vendor-leg failure beyond the Collector.

### 23.11 Backend priority (record)

Phase 8 external-backend routing priority:

1. **Dynatrace** — primary external backend target.
2. **New Relic** — secondary external backend target.
3. **Datadog** — deferred unless a standard OTLP / OTLP-HTTP ingest path can
   be used cleanly, without a proprietary exporter or agent.

Datadog must not be integrated through the Datadog Collector exporter in
Phase 8 unless a future explicit amendment changes rule 23.4.

### 23.12 Local stack direction for Phase 8B (record)

The intended Phase 8B local observability stack:

- OpenTelemetry Collector
- Prometheus
- Loki
- Jaeger
- Grafana

Phase 8B's purpose is to prove local routing and demo topology before any
vendor fan-out exists. Phase 8B extends the current Phase 6A stack — Collector
+ Prometheus + Jaeger + Grafana — by adding Loki and local log routing.

### 23.13 Accepted Phase 8 split (record)

Phase 8 is split into three phases, each closed under the Phase Closure
Protocol before the next begins:

- **Phase 8A — Architecture Baseline Amendment (this section).** Authorizes
  the Collector-owned fan-out rules and governance above.
  Architecture/documentation only; authorizes no implementation.
- **Phase 8B — Local Multi-Backend Stack Expansion.** Strengthens local
  observability routing (adds Loki and log routing; proves the local
  topology) with no vendor credentials and no network egress.
- **Phase 8C — Optional Vendor Export Profiles.** Adds disabled-by-default
  vendor export profiles using standard OTLP / OTLP-HTTP, governed entirely by
  this amendment.

### 23.14 What this amendment does NOT authorize

For the avoidance of doubt, Phase 8A authorizes none of the following; each
would need its own phase and, where it touches the baseline, its own
amendment: vendor SDKs or agents in application code; the Datadog exporter or
any proprietary exporter; direct application-to-vendor network calls; cloud
deployment; Kubernetes, Terraform, or Helm; hosted databases; production
authentication; alerting systems; making telemetry mandatory; making Docker
mandatory for tests; or any change to the SQLite / artifact source-of-truth
semantics. The Phase 7C / 7C.1 §16 note's "no vendor telemetry fan-out"
statement is superseded **only** to the narrow extent stated in 23.1–23.13.
This Section 23 amendment is **locked** (2026-05-24); that narrow supersession
is now in effect.

## 24. Phase 9A Amendment — Governance Baseline (Trust Envelope, Licensing, Fail-Closed Gating)

> **Status:** **Locked** — Phase 9A Architecture Baseline amendment, accepted.
> Authored by Claude Opus 4.7 as a Phase 9A candidate; reviewed by GPT-5.5
> (docs-only, review-ready); reviewed by Gemini (`SAFE WITH EDITS`); the
> **Phase 9A.1 cleanup** folded in the two required clarifications before lock
> — the source-authorization-not-viewpoint rule (§24.5) and the early
> fail-closed clarification (§24.6); locked with explicit user approval
> (2026-05-24). This follows the precedent of the Phase 7C / 7C.1 §16 and the
> Phase 8A §23 amendments — authored as a candidate, then locked. This section
> is now canonical: Phase 9B (Minimal Trust Envelope Implementation) may depend
> on it. Any further change to it requires a new explicit, user-approved
> amendment.
> **Scope:** Architecture, governance, and documentation only. Phase 9A
> authorized **nothing to be built**. It defines the governance law that the
> future Phase 9B (Minimal Trust Envelope Implementation) must obey, and the
> dependency contract Phase 10 (Product UI / Operator Experience) may build on.
> Phase 9A changed no application code, no database schema, no artifact
> envelope code, and no configuration behaviour.

### 24.1 Why this amendment exists

Phase 9 is **Security, Licensing, and Governance**. Three Phase 9 structures
were reviewed; the accepted structure is a hybrid:

```text
Phase 9A — Governance Baseline Amendment        (this section)
Phase 9B — Minimal Trust Envelope Implementation
Phase 9C — Docs / Audit Polish, if needed
```

StoryTime already constrains source material to CC0 and US public domain
(Product Charter §6, §7; §6 of this baseline — the closed source-manifest
schema with `license` ∈ {`CC0-1.0`, `PD-US`}). What StoryTime does **not** yet
have is an explicit, durable, queryable governance record of *who* approved a
source, *under what license category*, *with what justification*, and an
explicit, fail-closed rule that the expensive and externally sensitive stages
of the pipeline must not run unless that approval exists.

Phase 9A defines that governance law **before** Phase 9B implements it, so the
implementation is the concrete artifact/projection of an already-agreed model
rather than an architecture decision smuggled in as an implementation detail
(LLM_DIRECTOR architecture-amendment rule).

The amendment, stated once:

> Licensing approval is a **human operator decision**. StoryTime **records,
> preserves, and later enforces** that decision; it does **not** infer,
> compute, or certify legal status, and it does not replace legal judgment.

### 24.2 StoryTime is not a legal rights-clearance engine (rule)

StoryTime is a local-first portfolio/demo content-to-audio pipeline. It is
**not** a legal rights-clearance platform, a copyright adjudicator, or a
compliance product.

- StoryTime must never claim that it, or any AI/model, has *legally
  determined* copyright status, public-domain status, or licensing validity.
- StoryTime documentation may honestly say the system helps an operator
  **maintain an audit trail** of their own licensing decisions. It must not
  claim **legal compliance**, **legal advice**, or **legal clearance**.
- The human operator is the source of truth for every licensing decision. The
  system's role is durable record-keeping and later enforcement of that
  recorded human decision.

### 24.3 No legal automation / no legal hallucination (rule)

No Phase 9 work may introduce automated legal determination or AI-generated
legal assertions. The following concepts are **forbidden** as field names,
config keys, schema values, telemetry attributes, or documented claims:

- `legal_verified_by_llm`
- `copyright_cleared_by_ai`
- `compliance_score`
- `rights_confidence_score`
- `copyright_safe_score`
- any AI-generated assertion that a source is *legally safe*
- any automatic legal determination derived from model inference

No AI copyright classifier, no compliance-scoring mechanism, and no
model-inferred rights status may be added. A licensing decision exists in the
system **only** because a human operator made it and it was recorded. See also
§24.14 (the future static grep/regex gate that mechanically enforces this).

This rule **strengthens** the Product Charter's conservative licensing posture;
it weakens nothing.

### 24.4 Allowed source categories (rule)

For StoryTime's current local/demo use case, the allowed source categories
are:

- `CC0` — Creative Commons Zero / public-domain dedication.
- `US_PUBLIC_DOMAIN` — works in the public domain in the United States.
- `EXPLICIT_PERMISSION` — the operator holds documented, explicit permission
  from the rights holder.
- `LOCAL_TEST_FIXTURE` — content generated locally for demo/test use, carrying
  no third-party rights.

These names are intended to be **stable** Phase 9B `license_type` values
(§24.8). There is deliberately **no** `AMBIGUOUS` category: ambiguity is not a
license. Ambiguous material must resolve into an explicit *decision* state —
`NEEDS_REVIEW`, `REJECTED`, or a manually justified `APPROVED` under one of the
recognized categories above with a written `review_context_summary`. The
governance model never carries "maybe" as a steady state.

### 24.5 Disallowed / blocked source categories (rule)

The following source material is disallowed unless an explicit, recognized,
human-justified approval exists for it:

- copyrighted works used without permission;
- paywalled content;
- private or personal user content;
- ambiguous-license content, unless the operator explicitly approves it with
  notes under a recognized license category (§24.4);
- arbitrary website scraping or bulk web ingestion;
- any source matched by the local blocked-source config once Phase 9B
  implements it (§24.9).

Ambiguous content **fails closed**: absent an explicit operator approval with a
recognized decision category and a written justification, ambiguous material
is treated as not approved and the pipeline must not proceed past the
fail-closed gate (§24.6).

**Governance is source authorization, not viewpoint acceptability.** This rule
bounds what the categories above mean. StoryTime governs source authorization,
not viewpoint acceptability. Controversial, sensitive, political, religious,
historical, philosophical, or unpopular perspectives are **not** blocked
merely because of their viewpoint. Governance decisions concern source
authorization, licensing provenance, privacy, operator approval,
blocked-source status, and auditability — never the opinions, themes, or
positions expressed in a source. A source is `BLOCKED` or `REJECTED` because of
*how it was obtained or licensed* (unlicensed copyright, paywalled, private,
scraped, blocked-source-config match, unresolved ambiguity), not because of
*what it says*. StoryTime governance is **not** a content-moderation system: it
introduces no topic-policy categories, no viewpoint screening, and no content
safety classification, and Phase 9B must not add any.

### 24.6 Fail-closed governance gate (rule — Phase 9B implementation requirement)

Phase 9B must implement a **fail-closed** governance gate. Phase 9A defines the
required behaviour; it does **not** implement it.

Required behaviour:

> Before the pipeline initiates **TTS / audio synthesis** or **RSS publish**,
> it must verify that the source has an `APPROVED` Trust Envelope (§24.7,
> §24.8). If a source's governance decision is `BLOCKED`, `REJECTED`,
> `NEEDS_REVIEW`, or `UNKNOWN`, or if the Trust Envelope is missing,
> malformed, or unverifiable, the pipeline must **abort before TTS** and must
> **not publish to RSS**.

**Check early; block hard.** Phase 9B should check governance status **as early
as practical** in the pipeline — ideally before or during approval /
rehydration — so that an unauthorized source is surfaced and stopped as soon
as possible rather than only at the last moment. Early checking is a usability
and fail-fast improvement; it does **not** relax the hard requirement. The
**hard block** remains: regardless of how early a check runs, the pipeline
**must block execution before TTS, audio processing, or RSS publishing** if no
`APPROVED` Trust Envelope exists. An early check that passes never licenses a
later stage to skip the hard gate, and an early check is never a substitute
for the before-TTS/audio/RSS block. The before-TTS/audio/RSS block is the
load-bearing invariant; early checking is an additional, earlier safeguard on
top of it.

The gate exists to stop expensive or externally sensitive stages from running
without an approved governance decision. It must protect, at minimum:

- TTS / audio synthesis;
- audio processing that is downstream of an unapproved TTS step;
- RSS publishing.

Fail-closed means the **absence, malformation, or non-`APPROVED` state** of a
Trust Envelope blocks the run — the gate never "fails open" on a missing or
unreadable record. An `APPROVED` Trust Envelope must **exist** before TTS or
RSS publish; nothing weaker satisfies the gate.

Phase 9A does not implement this gate, wire it into the runner, or change the
stage model (§9). Phase 9B implements it.

### 24.7 The Trust Envelope (concept)

The **Trust Envelope** is the durable governance record for a source's
license, the operator's decision about it, and the justification for that
decision. It is an **audit artifact, not a legal opinion**.

- The Trust Envelope records a *human* decision. It does not assert legal
  truth; it asserts "operator X decided Y about source Z, for reason R, at
  time T."
- It is intended to be represented in **two** surfaces:
  1. the **durable artifact envelope** / exported state — for portability and
     recovery;
  2. a **SQLite projection** — for operational queries.

Source-of-truth reconciliation with §1 and §7: §1 establishes that the SQLite
state store, the `event_log`, and the artifact files are the source of truth
and OpenTelemetry is a view. The Trust Envelope is consistent with that model.
For the Trust Envelope specifically, the **durable artifact envelope is the
governance source of truth for portability and recovery**; the SQLite
projection is an operational-query convenience and must be rebuildable from the
durable envelopes. This specifies *which surface wins on conflict* for this one
record type — the durable envelope — without rewriting the §1 model or
reopening any prior phase. Phase 9B may refine exactly how the envelope is
embedded in or linked from the existing artifact envelope format (§7); it must
not weaken the durable-envelope-wins rule.

### 24.8 Trust Envelope schema (canonical architecture law)

The minimum Phase 9B Trust Envelope schema is defined here, in the Architecture
Baseline, as **canonical architecture law** — not as an implementation detail.
Phase 9B implements a record conforming to this schema.

```yaml
schema_version: string
source_ref: string
source_url: string | null
source_title: string | null
source_author: string | null
license_type: enum
license_url: string | null
license_evidence_ref: string | null
decision: enum
decision_timestamp: ISO-8601 string
approver_id: string
allowed_use: string | null
attribution_required: boolean | null
commercial_use_allowed: boolean | null
blocked_reason: string | null
governance_notes: string | null
review_context_summary: string | null
artifact_hash_refs: list[string]
```

Field semantics:

- `schema_version` — the Trust Envelope schema version; widening the schema
  requires a new version, mirroring the closed-schema discipline of §6.
- `source_ref` — stable internal reference to the source (e.g. the manifest
  `source_id`); the join key to the rest of the run record.
- `source_url`, `source_title`, `source_author` — descriptive provenance;
  nullable because not every source (e.g. a `LOCAL_TEST_FIXTURE`) has them.
- `license_type` — see allowed values below.
- `license_url`, `license_evidence_ref` — pointers to the licence text and to
  local evidence the operator relied on; references, never payloads.
- `decision` — see allowed values below.
- `decision_timestamp` — ISO-8601 time the operator's decision was recorded.
- `approver_id` — identifier of the **human** operator who made the decision.
- `allowed_use`, `attribution_required`, `commercial_use_allowed` — bounded
  descriptors of the operator's recorded understanding of the licence; never
  AI-inferred legal conclusions.
- `blocked_reason` — required justification when `decision` is `BLOCKED` or
  `REJECTED`; null otherwise.
- `governance_notes` — optional free-text operator notes.
- `review_context_summary` — a short, human-readable justification for the
  operator's decision (see below).
- `artifact_hash_refs` — list of artifact hash references tying the envelope
  to the run's artifacts; consistent with the §7 artifact-hash model.

`review_context_summary` is a brief operator-written justification, for
example:

```text
Verified CC0 via source page.
Verified public-domain text via Project Gutenberg reference.
Explicit permission documented in local approval note.
Local test fixture generated for demo use.
```

`review_context_summary` **must not** contain raw story text, full source
text, narration text, or private content. It is a short rationale, not a
content store.

Allowed `license_type` values (minimum set):

```text
CC0
US_PUBLIC_DOMAIN
EXPLICIT_PERMISSION
LOCAL_TEST_FIXTURE
BLOCKED
UNKNOWN
```

Allowed `decision` values (minimum set):

```text
APPROVED
REJECTED
BLOCKED
NEEDS_REVIEW
```

Phase 9B **may refine field names only** where repo consistency genuinely
requires it (for example, aligning casing or a prefix with existing manifest
or envelope fields), but it **must preserve the semantics, the enum value
sets, and the durable-envelope-wins rule**. The enum value sets above are a
*minimum*; Phase 9B may not silently drop a value, and adding a value is a
schema change governed by `schema_version`.

### 24.9 Blocked-source policy (direction for Phase 9B)

Phase 9B should implement a simple, **local** blocked-source configuration,
expected at approximately:

```text
config/governance/blocked-sources.yaml
```

The blocked-source list must be local, explicit, and human-inspectable. It
must **not** be a cloud service, must **not** fetch remote blocklists, and must
**not** automatically scrape or classify websites. It is a static, committed,
reviewable file of sources the operator has chosen to block.

Expected per-entry shape (Phase 9B refines exact field names):

- a source pattern, URL, or domain reference;
- a `reason`;
- an `added` timestamp, if practical;
- an optional `note`.

A source matched by this config resolves to a `BLOCKED` governance decision and
fails the §24.6 gate. Phase 9A defines this concept and expected schema only;
Phase 9B implements it.

### 24.10 Secrets policy (reinforcement)

Phase 9A reinforces, and does not weaken, the project-wide secrets rule
(Product Charter §9; §17 of this baseline; the locked §23.6 / §23.7 vendor
secret rules; the Phase 8C vendor-profile lesson):

- no real secret is ever committed;
- `.env` is git-ignored;
- example env files contain **obvious placeholders only**;
- external credentials exist only in environment variables at runtime;
- **no credentials are stored in SQLite**;
- **no credentials are stored in artifact envelopes** (including the Trust
  Envelope);
- no attempt is made to encrypt credentials into SQLite;
- no production secrets manager is introduced in Phase 9;
- no CI/CD secrets are introduced in Phase 9.

Stated as one rule:

> If it is an external credential, it does not exist in source code, committed
> docs, SQLite, or artifact envelopes. It exists only in the volatile runtime
> environment.

Phase 8C's lesson carries forward: committed examples may contain only obvious
placeholders, while real external values live in git-ignored runtime files or
process environment variables. The Trust Envelope is an audit record of
licensing decisions — it is **not** a credential store.

### 24.11 Deletion and retention posture (record)

Phase 9A records an honest, local-first deletion/retention posture. It does not
implement any deletion feature.

- StoryTime is **local-first**.
- Deletion is a **host-level / local filesystem operation**.
- There is **no cloud-native soft delete**.
- There is **no compliance shredder**.
- There is **no GDPR/CCPA compliance claim**.
- The project documents local deletion expectations honestly.

This is consistent with §18 (Data Retention and Cleanup Model) and the standing
`storytime clean` carryover (OI-15); Phase 9A neither implements nor changes
that tooling. Trust Envelopes, like other run records, live on local disk and
are removed by local filesystem operations; there is no remote authoritative
copy to reconcile.

### 24.12 Telemetry / privacy carryover (rule)

Phase 9A carries forward, and does not weaken, the Phase 5 / Phase 8 telemetry
hygiene rules (§11; §23.8; `docs/telemetry-map.md`):

- no raw story text in spans, logs, or metrics;
- no generated narration text in telemetry;
- no full RSS XML payloads in telemetry;
- no secrets in telemetry;
- no private content in telemetry;
- governance audit logs reference IDs and hashes, **not** content payloads.

If a future phase adds governance telemetry, it may include only **bounded
status metadata**, for example:

- `governance.decision`
- `governance.license_type`
- `governance.review_required`
- `source.ref_hash`
- `pipeline.run_id`

Governance telemetry must **not** include raw source text, full URLs that
contain secrets, long notes, `review_context_summary` text, or any free-text
content. Phase 9A adds **no** telemetry; this clause governs any future
governance telemetry so it cannot erode the hygiene baseline.

### 24.13 Public / demo disclaimers (record)

StoryTime's public/demo framing must state honestly:

- StoryTime is a **local-first portfolio/demo project**.
- StoryTime is **not legal advice**.
- StoryTime is **not a production rights-clearance platform**.
- Human operators remain responsible for source and licence validation.
- The demo uses **CC0, US public-domain, explicit-permission, or local test
  fixture content only**.

These disclaimers align with the locked Product Charter (§1, §4, §6) and
require no change to the charter; the charter's conservative licensing
boundary already supports them. Phase 9A records the disclaimers here as
governance law; any later doc/UI that surfaces them must not contradict
§24.2 / §24.3 by overclaiming legal certification.

### 24.14 Future legal-hallucination grep/regex gate (direction for Phase 9B)

Phase 9B should add a **static grep/regex verification gate** that prevents
forbidden legal-certification language from entering docs, configuration, or
implementation. Phase 9A documents this requirement; it does not implement an
enforcement gate.

The gate's forbidden set should include at minimum:

```text
legal_verified_by_llm
copyright_cleared_by_ai
compliance_score
rights_confidence_score
copyright_safe_score
GDPR compliant
CCPA compliant
legal clearance
legally certified
AI-verified copyright
```

The gate's intent is narrow: it must **not** ban ordinary, honest discussion of
"legal advice" disclaimers (StoryTime *should* say it is not legal advice).
It must prevent StoryTime from **claiming** legal determination, compliance
certification, or AI rights clearance.

Implementation note for Phase 9B: this Architecture Baseline section, and any
other governance document that must *define* the forbidden vocabulary in order
to ban it, legitimately contain those terms. The Phase 9B gate must therefore
either (a) match assertion-style usage rather than the bare token, or
(b) maintain a small, explicit allowlist of governance documents that define
the vocabulary (this §24, and the state docs that quote it). The gate must not
flag a document for honestly *prohibiting* a term.

### 24.15 Phase 10 dependency (record)

Phase 10 is Product UI / Operator Experience. So Phase 10 can safely build on
Phase 9B without overclaiming, Phase 9B must deliver:

- a **parseable** Trust Envelope;
- clear decision/status fields;
- a **stable, UI-safe status enum**;
- a rejected/blocked **reason** field;
- a source/licence summary;
- the ability to show whether a source is approved, rejected, blocked, or
  needs review;
- **no legal-compliance overclaiming**.

The UI-facing status enum aligns with the `decision` enum (§24.8):

```text
APPROVED
REJECTED
BLOCKED
NEEDS_REVIEW
```

Phase 10 UI **visualizes** governance status. It must **not** present that
status as a legal certification of content. A Phase 10 screen may say "this
source is marked APPROVED by operator X on date T"; it may not say "this
source is legally cleared."

### 24.16 Accepted Phase 9 split (record)

Phase 9 — Security, Licensing, and Governance — is split into three phases,
each closed under the Phase Closure Protocol before the next begins:

- **Phase 9A — Governance Baseline Amendment (this section).** Architecture,
  governance, and documentation only. Defines the governance law. Authorizes
  no implementation.
- **Phase 9B — Minimal Trust Envelope Implementation.** Implements the Trust
  Envelope schema (§24.8), the fail-closed governance gate (§24.6), the local
  blocked-source config (§24.9), and the static legal-hallucination grep/regex
  gate (§24.14), as the concrete artifact/projection of this law.
- **Phase 9C — Docs / Audit Polish, if needed.** Optional follow-up.

Phase 9B may begin only after Phase 9B is itself scoped and gated under the
Phase Closure Protocol. This Section 24 is now reviewed, cleaned (the Phase
9A.1 cleanup), and **locked**, so that precondition on Section 24 is satisfied.

### 24.17 What this amendment does NOT authorize

For the avoidance of doubt, Phase 9A authorizes none of the following; each
would need its own phase and, where it touches the baseline, its own
amendment: implementing the Trust Envelope, its SQLite projection, or any
schema; implementing the fail-closed gate or wiring it into the runner;
implementing the blocked-source config; implementing the grep/regex gate (as
anything other than docs); any change to application code, database schema,
artifact envelope code, or configuration behaviour; authentication, users,
roles, or permissions; cloud security, hosted databases, or a production
secrets manager; CI/CD secrets; scraping systems or arbitrary website
ingestion; legal-determination logic, an AI copyright classifier, or
compliance scoring; payment or monetization; production compliance claims; any
weakening of the Phase 8 telemetry/privacy rules; storing secrets in SQLite or
artifact envelopes; and reopening any locked phase. This Section 24 is
**locked** (2026-05-24); it is governance law and authorizes no implementation
— Phase 9B implements that law as a separately scoped and gated phase.

## 25. Phase 10A Amendment — Operator Experience Baseline

> **Status:** **LOCKED / ACCEPTED / CANONICAL.** Phase 10A Operator
> Experience Baseline Amendment was authored by Claude Opus 4.7, verified by
> GPT-5.5, reviewed by Gemini 3.1 Pro, and locked with explicit user approval
> on 2026-05-24. This Section 25 is now a locked, canonical part of the
> Architecture Baseline. Gemini's review returned **SAFE TO LOCK (PENDING
> VERIFICATION)**; GPT-5.5 satisfied that pending verification by confirming
> the amendment was documentation-only, changed no implementation files, and
> left Phase 10B not started. Gemini's local-web-server aside was not accepted
> as Phase 10B authorization; the locked first implementation target remains a
> generated static local HTML operator report with no server runtime.
> **Scope:** Architecture, governance, and documentation only. Phase 10A
> authorizes **nothing to be built**. It defines the operator-experience law
> that the future Phase 10B (Generated Local Operator Report) must obey, and
> the Phase 10B handoff specification. Phase 10A changed no application code,
> no database schema, no artifact envelope code, no Trust Envelope semantics,
> no governance gate behaviour, no telemetry behaviour, and no configuration
> behaviour. It added no dependency and no template, report-generator, CLI,
> or UI code. Phase 10A does **not** start Phase 10B, 10C, or 10D.

### 25.1 Why this amendment exists

Phase 10 is titled **Product UI / Operator Experience**. Phase 9B closed with
a locked governance layer — the Trust Envelope, its SQLite projection, and the
fail-closed gate — and §24.15 records a deliberate dependency contract from
Phase 10 onto Phase 9B's stable, parseable, UI-safe governance status. What
Phase 10 does **not** yet have is an agreed definition of what "Operator
Experience" means for a local-first portfolio pipeline, or a guard against the
phase quietly becoming a hosted SaaS web application.

Phase 10A defines that operator-experience law **before** Phase 10B implements
any of it, so the implementation is the concrete artifact of an already-agreed
model rather than an architecture decision smuggled in as an implementation
detail (the LLM_DIRECTOR architecture-amendment rule). The accepted Phase 10
structure is staged and conditional:

```text
Phase 10A — Operator Experience Baseline Amendment   (this section, docs-only)
Phase 10B — Generated Local HTML Operator Report     (first likely build)
Phase 10C — Operator CLI Helpers / Failure Queue     (future, only if needed)
Phase 10D — Optional Local Web Dashboard             (future, only if justified)
```

Phase 10A was reviewed in planning by multiple independent reviewers (GPT-5.5
Thinking as architect/mediator; Claude Haiku 3.5, Copilot Think Deeper,
GPT-5 mini, Gemini 3.5 Flash Lite Extended, and Llama 4 Scout as critics).
Reviewer consensus: Phase 10A should be docs-only; Phase 10B should be a
generated local HTML operator report; Phase 10 must be read-only-first; Phase
10 must not become a SaaS/web-app rewrite; Phase 10 must preserve the Phase 9
governance boundaries; and Phase 10B must have a hard floor and a hard ceiling
fixed before implementation. This section codifies that consensus.

The amendment, stated once:

> Phase 10 makes StoryTime **understandable, operable, and demoable by a local
> human operator** — by showing, faithfully and read-only-first, what the
> pipeline already did. It does **not** turn StoryTime into a hosted product,
> and it never re-states a recorded operator decision as a legal certification.

### 25.2 Operator experience goal (rule)

The Phase 10 operator-experience goal:

```text
Make StoryTime understandable, operable, and demoable by a local human
operator, without turning it into a premature SaaS product.
```

The operator is a **single, local, trusted human** running StoryTime on one
machine — the same person who runs `storytime run`, `storytime doctor`, and
the blue/green scripts today. There is exactly one such role; Phase 10 invents
no others.

Operator-persona example (illustrative, not a product spec):

```text
A local operator has run StoryTime several times. They generate the operator
report to answer: What happened in the last runs? Which runs completed? Which
runs were blocked or rejected by governance? Which runs failed, and at which
stage? Where are the audio and RSS artifacts on disk? Where are the
observability dashboards for a run, if telemetry was enabled?
```

Phase 10 must **not** create personas that imply SaaS, multi-user accounts,
authentication, role hierarchies, customer/tenant separation, or production
account management. There is one operator, on one host, with filesystem
access to the repository.

### 25.3 Read-only-first operator rule (rule)

```text
Phase 10 begins with read-only — or at most mostly-read-only — visibility into
existing pipeline state. State mutation remains CLI/pipeline-controlled unless
a later, separately-gated phase explicitly scopes an operator action surface.
```

The operator surface must show **what happened** before it is ever allowed to
let an operator **change what happens**. Phase 10B (§25.8) is strictly
read-only: it renders existing state and creates no new state. Any operator
*action* — approve, retry, reject, rerun, edit, delete — is out of scope for
Phase 10B and gated behind §25.17 and a future phase.

### 25.4 Source of truth rule (rule)

```text
SQLite and the on-disk artifact files remain the source of truth.
Operator reports and any operator UI READ from SQLite and the artifact
envelopes; they are never themselves authoritative.
The durable Trust Envelope artifact remains the governance source of truth
(§24.7); the SQLite trust_envelope table remains a rebuildable projection.
Observability dashboards (Grafana, Jaeger, Prometheus, Loki) are links/views,
never the source of truth.
```

Phase 10 must not make a generated report, an HTML file, a Grafana panel, or
any telemetry store authoritative. A generated report is a **projection** of
the SQLite state and the artifact envelopes at the moment it was generated; if
it is deleted, nothing of value is lost and it can be regenerated. This
preserves the Phase 1 source-of-truth model and the §24.7 governance-truth
rule unchanged.

### 25.5 Governance display rule (rule)

Phase 10 surfaces present governance status by faithfully **transcribing** the
locked Trust Envelope (§24.8) and pipeline state. They visualize a recorded
human operator decision; they never compute, infer, or certify anything.

A Phase 10 surface **may** display:

```text
source title or source ID
run ID (pipeline_run_id)
pipeline / run status
stage names and stage statuses
governance decision (the §24.8 decision enum)
license type (the §24.8 license_type enum)
approver_id / human reviewer label
approval timestamp
a bounded review_context_summary (see §25.13)
the Trust Envelope artifact path / link
a structured blocked or rejected reason, if present and safe
artifact paths (audio, RSS/feed, Trust Envelope, stage artifacts)
configured observability links (see §25.14)
```

A Phase 10 surface **must not** display, assert, or imply any of the following
legal/compliance overclaiming phrases (this list extends, and must stay
consistent with, the §24.3 / §24.14 forbidden vocabulary):

```text
Legally cleared
Legal clearance
Legal certification
Legally certified
Copyright verified
AI-verified copyright
Copyright verified by AI
Copyright cleared by AI
Compliance approved
Compliance certified
Safe for publication
Cleared for publication
No DMCA risk detected
No copyright risk
Copyright-safe score
copyright_safe_score
Compliance score
compliance_score
Rights confidence score
rights_confidence_score
GDPR compliant
CCPA compliant
legal_verified_by_llm
```

Every Phase 10 surface that shows governance status must carry, in substance,
a standing disclaimer:

```text
This is a record of a human operator's decision and of pipeline state. It is
not legal advice and not a certification of copyright safety.
```

A Phase 10 screen or report row may honestly say "this source is marked
APPROVED by operator X on date T"; it may never say or imply that the source
is "legally cleared" or that any automated check certified it. This restates
§24.15 ("Phase 10 UI visualizes governance status; it must not present that
status as a legal certification of content") as an explicit display rule.

### 25.6 Viewpoint neutrality carryover (rule)

The locked Phase 9 rule (§24.5) is preserved unchanged:

```text
StoryTime governs source authorization, not viewpoint acceptability.
```

Phase 10 surfaces must not add topic categories, viewpoint screening, content
moderation labels, content-safety classification, or political / religious /
philosophical acceptability judgments. The operator report shows *how a source
was licensed or obtained and what the operator decided* — never *what the
source says*. StoryTime governance is not, and Phase 10 does not make it, a
content-moderation system.

### 25.7 Operator surfaces (record)

Phase 10's operator surface is, for now, a **generated local artifact** — the
Phase 10B report (§25.8). The existing CLI (`storytime run`, `status`,
`doctor`, `serve`, the blue/green scripts) remains the operational control
surface and is unchanged by Phase 10. Phase 10A authorizes exactly one new
surface to be *planned*: the generated local operator report. A CLI failure
queue (Phase 10C) and an optional local web dashboard (Phase 10D) remain
future, conditional, and not started; neither is authorized by this amendment.

### 25.8 Phase 10B target — Generated Local HTML Operator Report (record)

The recommended and accepted first Phase 10 implementation target is:

```text
Phase 10B — a generated, static, local HTML operator report.
```

Phase 10B generates a set of static HTML files from the existing SQLite state
and artifact envelopes. The operator opens those files directly in a browser
from the local filesystem. The report is regenerated on demand; it is a
read-only projection (§25.3, §25.4). Phase 10B is the **first likely
implementation phase** of Phase 10 — but it is still a separate phase that
must be scoped and gated under the Phase Closure Protocol before any code is
written. This section authorizes Phase 10B's *shape*, not its execution.

### 25.9 Phase 10B hard floor (rule)

Phase 10B must deliver at least a usable report. The minimum acceptable
Phase 10B implementation produces a generated local report directory with
something equivalent to:

```text
operator-report/index.html
operator-report/runs.html
operator-report/run-<run_id>.html   (one per recent run)
```

Minimum report capabilities (the hard floor):

```text
- a latest-runs summary (the most recent runs at a glance);
- a run list showing, per run: run_id, run status, created/updated
  timestamps, governance decision, and links to that run's artifacts;
- a single-run detail page showing: the run's stages and stage statuses,
  governance detail (decision, license type, approver, approval timestamp,
  bounded review_context_summary), artifact paths, failure status if any,
  and configured observability links if any.
```

The floor exists so Phase 10B cannot be underbuilt into an unusable stub. A
report that omits the run list, or the single-run detail page, or governance
status, is below the floor and is not an acceptable Phase 10B.

### 25.10 Phase 10B hard ceiling (rule)

Phase 10B must not exceed a generated, static, read-only report. Phase 10B
must **not** include any of:

```text
interactive mutation of any kind
HTML forms
buttons or controls that change state
an approval / retry / reject / rerun / delete workflow
a server process or persistent backend service
live telemetry polling
websockets or live streaming
a frontend framework (React, Vue, Svelte, etc.)
an asset build pipeline / bundler / transpiler
authentication, login, sessions, users, or roles
cloud or hosted deployment
a responsive design system
a dark-mode / theme system
animations
recreation of the Grafana dashboards
charts embedded from telemetry data
a full visual-polish / design-system pass
```

Skeleton HTML is acceptable and expected. A single small, static CSS file is
permitted for basic legibility (readable typography, simple table layout) —
but **minimal CSS only**: no design system, no framework, no CSS build step,
and no major visual-polish pass. Phase 10B is judged on faithful, deterministic
content, not on appearance. The CSS allowance is guidance for restraint, not a
licence for a styling phase; if repo conventions later support a precise size
limit, Phase 10B may adopt one, but the intent — minimal, static, hand-written
CSS — is the binding rule.

### 25.11 Phase 10B report data model / schema (rule)

Phase 10B must build the report from a **deterministic, explicit report data
model** assembled from existing state — never from raw source content. The
model's fields and their sources:

```text
run_id                       — SQLite run state (pipeline_run_id)
run_status                   — SQLite run state
created_at                   — SQLite run state
updated_at                   — SQLite run state
stage_statuses               — SQLite stage/run state (per-stage name+status)
governance_decision          — Trust Envelope projection / durable artifact
license_type                 — Trust Envelope projection / durable artifact
approver_id                  — Trust Envelope projection / durable artifact
approval_timestamp           — Trust Envelope projection / durable artifact
review_context_summary       — Trust Envelope (bounded display only — §25.13)
trust_envelope_artifact_path — run artifact reference (the durable JSON path)
audio_artifact_path          — artifact reference
rss_feed_path                — artifact reference
failure_code / failure_category — structured run/stage state, if available
observability_links          — configured links only (§25.14)
```

The report data model must contain **no raw-content fields** — no source story
text, no source body, no generated narration text, and no transcript. Phase
10B may refine the exact field names for repository consistency, but must
preserve these field semantics and sources, and must not add a raw-content
field. The Trust Envelope projection already exposes bounded status fields
(Phase 9B); the report reads those, not raw text.

### 25.12 Report output field allowlist / blacklist (rule)

This is the field-level output policy the future Phase 10B report must obey.

**Allowed report fields** — the report may show these bounded fields:

```text
run_id
run status
created_at / updated_at timestamps
stage names
stage statuses
governance decision (APPROVED / REJECTED / BLOCKED / NEEDS_REVIEW)
license_type (CC0 / US_PUBLIC_DOMAIN / EXPLICIT_PERMISSION /
              LOCAL_TEST_FIXTURE / BLOCKED / UNKNOWN)
approver_id
approval timestamp
a bounded review_context_summary (§25.13)
Trust Envelope artifact path
artifact paths
audio output path
RSS / feed output path
a structured failure code or structured failure category
configured observability links
```

**Forbidden report fields** — the report must never show, embed, or inline any
of these:

```text
raw source story text
raw source body
generated narration text
TTS transcript / audio transcript
full reviewer notes
long free-text governance notes
secrets, tokens, API keys, credentials
private content
full environment dumps
stack traces containing sensitive data
unbounded exception text
raw telemetry payloads
embedded dashboard data
```

A forbidden field appearing in report output — even indirectly, even
truncated-but-still-raw — is a Phase 10B defect and a §25.24 stop/revert
trigger. Phase 10B must include tests (§25.19) proving the forbidden fields
are absent.

### 25.13 Bounded review_context_summary rule (rule)

The Trust Envelope's `review_context_summary` (§24.8) is the operator's short
governance rationale. The report **may** display it, but only bounded and
safe:

```text
review_context_summary may be displayed only as a SHORT governance rationale.
It must not contain — and Phase 10B must not display from it — raw story text,
private content, secrets, legal advice, or long deliberation history.
Phase 10B must enforce a MAXIMUM displayed length, and that bound must be
testable.
If the summary is absent, the report shows a safe, neutral placeholder.
If the summary exceeds the bound, the report shows safely-truncated bounded
text with a clear truncation indicator — never the unbounded original.
```

**Concrete bound for Phase 10B:** the displayed `review_context_summary` is
capped at **500 characters**. Phase 10B may refine this number (for example to
240 characters) only if its tests continue to prove the privacy guarantee —
that no raw content and no unbounded text reaches the report. The number is a
guardrail; the privacy guarantee is the binding rule.

### 25.14 Observability link rule (rule)

```text
Observability links are optional references only.
They may link to configured local or vendor observability dashboards
(Grafana, Jaeger, Prometheus, Loki, or a configured vendor backend).
They must NOT embed dashboard data, panels, charts, or query results.
They must NOT embed credentials.
They must NOT include tokens, API keys, or secrets in URLs.
They must NOT be treated as a source of truth.
If observability systems are unavailable or not configured, the report is
still complete and correct — observability links are purely additive.
```

Phase 10B must define the allowed observability-link patterns or a safe
URL-construction rule: links are built only from configured base URLs plus the
run's `pipeline_run_id` (the durable correlation key), and a generated link
must never carry a secret. A report generated on a host with no observability
stack configured simply omits the links; it does not fail and does not degrade.

### 25.15 Static-only / no-server rule for Phase 10B (rule)

```text
The generated Phase 10B operator report must be STATIC-ONLY.
It must be viewable directly from local files (file:// or a plain file open).
It must NOT require a web server to view.
It must NOT introduce a persistent backend service.
It must NOT introduce a frontend framework or an asset build pipeline.
It must NOT introduce live polling, streaming, websockets, or real-time
telemetry ingestion.
```

The Phase 10B report is generated once per invocation and then read as inert
files. Generating the report is allowed to be a CLI action in a later-scoped
sense, but Phase 10A does not authorize that CLI command — Phase 10B will
specify and gate its own generation entry point.

### 25.16 No auth / cloud / SaaS rule (rule)

```text
No authentication, users, roles, or permissions.
No login. No sessions. No accounts.
No hosted backend. No cloud deployment.
No multi-tenant assumptions.
No production security model.
No external service dependency.
No server-side report runtime.
```

Phase 10 is a local-operator experience over a local-first pipeline. The
report runs offline, on one host, for one trusted operator. This rule extends
the §24.10 secrets posture and the local-first baseline; Phase 10 must not
weaken either.

### 25.17 Mutation gate rule (rule)

```text
No approvals, retries, rejections, reruns, edits, deletes, or any
state-changing action may be introduced in Phase 10B.
Any mutation UI or operator action surface requires a separate, future,
explicitly-gated phase with its own security / privacy / governance review.
```

The Phase 10B report **displays past decisions; it does not create new
decisions.** Approval remains a CLI/pipeline operation against the persisted
governance gate, exactly as Phase 9B left it. An operator-action surface is a
deliberate future question, not a Phase 10B feature.

### 25.18 Determinism / snapshot-test rule (rule)

```text
For identical fixture input, Phase 10B report generation must produce
identical, or normalized-identical, output.
Phase 10B must include snapshot / golden-output tests, or an equivalent
deterministic-assertion strategy.
```

If volatile fields (timestamps, absolute paths, host-specific values) make
byte-for-byte snapshots impractical, Phase 10B must normalize those fields
before snapshotting, or assert against the deterministic sections of the
output. Determinism is what makes the report trustworthy and testable; a
report that varies run-to-run on identical input is a Phase 10B defect.

### 25.19 Privacy / no-raw-content tests (rule)

Phase 10B must include tests that prove, on representative fixtures, that the
generated report:

```text
does not include raw source story text;
does not include generated narration text;
does not include TTS / audio transcripts;
does not include secrets, tokens, API keys, or credentials;
does not include long free-text governance notes (the review_context_summary
  bound of §25.13 is enforced and tested);
does not include any of the §25.5 / §24.14 forbidden legal/compliance
  overclaiming phrases.
```

These tests are a Phase 10B lock prerequisite. A report that can leak raw
content or overclaiming language is not lockable.

### 25.20 Governance-copy linting (rule)

Phase 10B must apply the Phase 9B static legal-hallucination scanner
(`storytime.governance.legal_terms`, §24.14) — or an equivalent
template/report-copy check — to its report templates and to its generated
report strings. The report's fixed copy and its templates must not contain the
§24.14 forbidden legal-certification vocabulary.

If Phase 10B introduces report templates or generated HTML files into the
repository tree, it must keep the §24.14 scanner green — either by ensuring the
templates contain no forbidden vocabulary (the expected and preferred outcome),
or, only if a template legitimately must *quote* the forbidden vocabulary in
order to ban or test it, by extending the scanner's governance-doc allowlist as
an explicit, reviewed Phase 10B change. Phase 10B must not silently weaken the
scanner.

### 25.21 Performance / size guardrail (rule)

```text
Report generation should complete within ~5 seconds for ~100 recent runs on a
typical development machine.
The generated report should avoid runaway asset bloat (no large embedded
binaries, no embedded audio, no embedded telemetry payloads).
```

This is a sanity guardrail for a local demo tool, **not** a production SLO. A
report that links to audio artifacts on disk rather than embedding them, and
that paginates or bounds the run list rather than rendering unbounded history,
satisfies the guardrail. Phase 10B may refine the exact numbers with
justification.

### 25.22 Phase 10B example run types (rule)

Phase 10B's handoff and tests must cover at least three run shapes:

```text
- a completed run            (all stages SUCCEEDED; APPROVED governance;
                              audio + RSS artifacts present);
- a governance-blocked run   (governance decision BLOCKED or REJECTED;
                              pipeline halted at the fail-closed gate;
                              a structured blocked/rejected reason present);
- a failed run               (a stage failed for a non-governance reason;
                              a structured failure code/category present;
                              no audio/RSS artifacts, or partial artifacts).
```

These may be documented in Phase 10B as fixture *shapes*. Phase 10A does not
create fixture files — describing the three shapes here is documentation only.

### 25.23 Handoff to Phase 10B — Generated Local Operator Report

This is the Phase 10B handoff specification. Phase 10B, when scoped and gated,
must satisfy all of it.

**Expected report directory structure**

```text
operator-report/index.html              — landing page / latest-runs summary
operator-report/runs.html               — the full run list
operator-report/run-<run_id>.html        — one single-run detail page per run
operator-report/style.css                — optional, minimal, static CSS only
```

**Required pages**

```text
index.html      — latest runs at a glance; links into runs.html and run pages
runs.html       — every recent run: run_id, status, created/updated, decision,
                  artifact links
run-<id>.html   — one run in detail: stages + stage statuses, governance
                  detail, artifact paths, failure status, observability links
```

**Required data fields and their sources** — exactly the §25.11 report data
model.

**Forbidden fields** — exactly the §25.12 blacklist; never rendered.

**Governance display rules** — §25.5 (allowed vs forbidden vocabulary; the
standing "record of a human decision, not legal advice" disclaimer) and §25.6
(viewpoint neutrality).

**Observability link rules** — §25.14 (links only; no embedded data; no
secrets in URLs; report complete without them).

**Test requirements** — §25.18 (determinism / snapshot), §25.19 (privacy /
no-raw-content), §25.20 (governance-copy linting). All three are Phase 10B
lock prerequisites.

**Hard floor** — §25.9. **Hard ceiling** — §25.10.

**Performance guardrail** — §25.21.

**Phase 10B archive name (recommended)**

```text
storytime-phase10b-generated-local-operator-report.tar.gz
```

Phase 10B remains read-only-first (§25.3), static-only / no-server (§25.15),
no-auth / no-cloud (§25.16), and mutation-gated (§25.17). It keeps SQLite and
the artifact envelopes as the source of truth (§25.4).

### 25.24 Stop / revert criterion (rule)

```text
If any Phase 10B implementation introduces — or is found to introduce —
authentication, cloud or hosted services, a server runtime, a persistent
backend, a mutation UI or state-changing action, raw-content display, or
legal/compliance overclaiming, the phase must STOP and return for re-scoping
and re-review before any lock.
```

This is a hard gate. Crossing any item in §25.10's ceiling, §25.12's forbidden
fields, §25.16's no-auth/no-cloud rule, or §25.5's forbidden vocabulary is not
a cleanup item — it is a stop condition. Phase 10B does not lock until it is
back inside the Phase 10A law.

### 25.25 Accepted Phase 10 split (record)

Phase 10 — Product UI / Operator Experience — is split into staged,
conditional phases, each closed under the Phase Closure Protocol before the
next begins:

- **Phase 10A — Operator Experience Baseline Amendment (this section).**
  Architecture, governance, and documentation only. Defines the
  operator-experience law and the Phase 10B handoff. Authorizes no
  implementation. **Locked — accepted/canonical.**
- **Phase 10B — Generated Local HTML Operator Report.** The first likely
  implementation phase: a generated, static, local, read-only HTML operator
  report built to the §25.23 handoff. **Not started.**
- **Phase 10C — Operator CLI Helpers / Failure Queue.** A possible future
  phase, **only if needed**. Not started; not authorized by this amendment.
- **Phase 10D — Optional Local Web Dashboard.** A possible future phase,
  **only if still justified** after 10B/10C. Not started; not authorized by
  this amendment.

Phase 10A is now reviewed and locked. Phase 10B may begin only as a
separately scoped and gated implementation candidate under the Phase Closure Protocol.

### 25.26 What this amendment does NOT authorize

For the avoidance of doubt, Phase 10A authorizes none of the following; each
would need its own phase and, where it touches the baseline, its own
amendment: implementing the Phase 10B report or any report generator;
writing any HTML, CSS, template, Python, CLI, or UI code; starting Phase 10B,
10C, 10D, or 11; adding any dependency; changing application code, database
schema, artifact envelope code, Trust Envelope semantics, governance gate
behaviour, or telemetry behaviour; authentication, users, roles, sessions, or
login; cloud or hosted deployment, hosted services, or a persistent backend;
a server-side report runtime; live telemetry polling, websockets, or
streaming; a frontend framework or an asset build pipeline; a mutation UI or
any approval/retry/reject/delete action surface; content, topic, or viewpoint
filtering or content-moderation labels; legal automation, an AI copyright
classifier, compliance scoring, or any legal/compliance certification claim;
adding secrets; and reopening any locked phase. This Section 25 is **locked** (authored and accepted 2026-05-24); it is
operator-experience law, and even as locked law it authorizes no implementation
by itself — Phase 10B implements that law as a separately scoped and gated
phase.


### 25.27 Lock record

Phase 10A was locked on 2026-05-24 with explicit user approval after:

- Claude Opus 4.7 authored Section 25 as a documentation-only amendment candidate.
- GPT-5.5 verified the candidate archive against the Phase 9B locked bundle and found no code, schema, configuration, dependency, template, CLI, report-generator, HTML, CSS, or UI implementation delta.
- Gemini 3.1 Pro reviewed the candidate and returned **SAFE TO LOCK (PENDING VERIFICATION)**.
- GPT-5.5 satisfied Gemini's pending-verification condition by confirming the docs-only scope and that Phase 10B had not started.
- The user approved locking Phase 10A.

Gemini's mention of possible local-web-server alternatives was reviewed as general commentary, not accepted as authorization for Phase 10B. The locked Phase 10B target remains **Generated Local HTML Operator Report**: static, local-file based, read-only, and no server runtime.

Phase 10B, Phase 10C, and Phase 10D remain not locked. Phase 10B may now be scoped and implemented as a candidate under the Phase Closure Protocol.
