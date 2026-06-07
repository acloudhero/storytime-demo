# Phase 14 — Live System / Cloud-Distributed Architecture Baseline

**Phase:** 14A.1 — Local Live Proof Loop Before Cloud (implementation candidate; pending review; NOT locked).
**Status of Phase 14:** STARTED. This document is the architecture baseline (slice 14A.1.A).

> **Guiding principle:** local live *before* cloud. The next proof priority is
> local live behavior that can later be hosted or distributed. Cloud is not
> useful until the local live proof loop is undeniable. This baseline therefore
> defines the local-live foundation first and treats cloud/distributed concerns
> as explicitly deferred future boundaries (Phase 14C.1+).

## 1. What makes StoryTime more than a static site?

Through Phase 13, the operator console was a static Demo Snapshot: a read-only
export of a prior run, useful for narrative but unable to *do* anything. A
reviewer could fairly say it "mostly claims that a system exists."

Phase 14A.1 changes that locally. There is now a real backend service
(`storytime local-live`) that:

- owns durable state in SQLite (the source of truth),
- creates a real, backend-owned proof run on request,
- records stages, append-only audit events, and an evidence artifact, and
- exposes that state read-only to the console over a loopback HTTP API.

The difference from a static page is observable: the run id, stages, artifacts,
and events are produced by the backend (not hardcoded in the browser), the
state lives in SQLite (not browser storage), and the run history survives a
server restart.

## 2. The minimum local live proof loop

1. The operator starts the loopback backend (`storytime local-live`).
2. The console connects and shows backend health (backend-owned, loopback-only).
3. The operator triggers one controlled, approved, deterministic proof run.
4. The backend creates and durably persists the run (run → stages → events →
   artifact) in SQLite.
5. The console renders the run's id, stages, artifact evidence (name, size,
   sha256), and audit events.
6. The operator restarts the backend; the prior run is still present.

This loop is intentionally small, safe, local, deterministic, and durable. It
uses no cloud credentials, no paid providers, no external APIs, no ffmpeg, and
no unsafe browser authority.

## 3. What moves from static export into backend-owned durable state?

| Concern | Phase 13 (static) | Phase 14A.1 (local live) |
| --- | --- | --- |
| Run records | baked into a JSON export | created by the backend in SQLite |
| Stage/event/artifact data | snapshot fields | live reads from durable tables |
| Triggering work | impossible | one controlled proof-run action |
| Persistence across restart | n/a (static file) | durable in SQLite |
| State owner | the export file | the backend database |

## 4. Architecture layers

The baseline defines these layers. Layers marked *(present)* exist after Phase
14A.1; layers marked *(future)* are deferred to Phase 14C.1+ and are described
only as target boundaries.

- **Frontend operator console** *(present)* — React/TS app; renders
  backend-owned state; requests controlled actions; owns no durable state.
- **Local live API / bridge service** *(present)* — `src/storytime/local_live/`;
  a loopback-only stdlib HTTP service exposing read-only run state plus one
  controlled proof-run action.
- **Backend command handlers** *(present)* — the service methods that validate
  a request and decide whether an action is allowed.
- **Pipeline runner / proof-run harness** *(present, proof-run only)* — the
  durable proof-run harness (`proof_run.py`). The full pipeline runner remains
  the canonical execution path for real runs; the proof harness deliberately
  exercises only the durable-state contracts without provider/ffmpeg paths.
- **Durable local SQLite state store** *(present)* — `src/storytime/state/`;
  the source of truth (ARCH-LOCK).
- **Artifact store** *(present)* — the run directory on disk; the proof run
  writes a real evidence artifact and records its relative key.
- **Audit / event log** *(present)* — the append-only `event_log` table.
- **Read model DTOs** *(present)* — `read_model.py`; typed, deterministic
  projections of durable state into safe JSON.
- **Telemetry boundary** *(present, unchanged)* — OpenTelemetry stays confined
  to the telemetry adapter; the local-live module imports no telemetry SDK.
- **Future queue / orchestrator** *(future)* — to schedule and sequence runs.
- **Future cloud API / auth boundary** *(future)* — a hosted API with
  authentication; provider credentials live server-side only.
- **Future object storage boundary** *(future)* — durable artifact storage off
  the local filesystem.
- **Future worker boundary** *(future)* — workers that execute real synthesis /
  assembly off the request path.

## 5. Operating modes

### Demo Snapshot Mode (present)
- **Owns state:** the committed static export file.
- **Actions:** none (read-only).
- **Browser may:** load and render the snapshot.
- **Backend must:** nothing (no backend required).
- **Deferred:** all live behavior.

### Local Live Mode (present — Phase 14A.1)
- **Owns state:** the backend SQLite database.
- **Actions:** read run state; trigger one approved, deterministic proof run.
- **Browser may:** request reads and the one controlled action; it owns no
  durable state and holds no credentials.
- **Backend must:** validate the request, perform and durably persist the state
  transition, record evidence, and serve backend-owned reads over loopback only.
- **Deferred:** provider-backed TTS, audio, RSS, cloud — see below.

### Cloud / Distributed Mode (future — Phase 14C.1+, NOT STARTED)
- **Owns state:** a hosted durable store behind a cloud API.
- **Actions:** authenticated, authorized operations routed through a queue.
- **Browser may:** call an authenticated API; still owns no durable state and
  never holds provider credentials.
- **Backend must:** authenticate, authorize, enqueue, execute on workers, and
  persist to durable cloud storage.
- **Deferred / not started:** everything in this mode. It is described here only
  as a target boundary; Phase 14A.1 does not implement, deploy, or start it.

## 6. What remains impossible from the browser?

Owning durable state; holding provider or cloud credentials; submitting
arbitrary text, paths, URLs, or provider selections; executing privileged work;
or binding a public network interface. The browser only ever *requests*; the
backend decides and owns truth.

## 7. What does "cloud / distributed" mean concretely (future)?

A future hosted deployment would add a cloud API/auth boundary, a queue and
orchestrator, a worker pool that performs real synthesis/assembly, and an
object-storage boundary for artifacts — all server-side, with credentials never
reaching the browser. This is reserved as Phase 14C.1+ and is NOT STARTED. See
`docs/phase14-cloud-distributed-roadmap.md`.
