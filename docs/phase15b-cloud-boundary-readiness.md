> **Phase 15B — Cloud Boundary Readiness (current implementation candidate; pending review; NOT locked).** Phase 15A — Cloud Runtime Skeleton — is LOCKED (last locked phase). Phase 15 — Cloud / Distributed Runtime — remains STARTED, and **Phase 15B is STARTED as the current implementation candidate** on top of the locked Phase 15A skeleton. Phase 15B combines the previously planned queue/worker, artifact/storage, observability/export, and recovery/idempotency readiness seams into one disciplined boundary-readiness phase. It adds a single pure-data `storytime.runtime.boundary_readiness` module, a design doc, a deferred-work register, guard tests, and state records; it adds no new dependency, no new environment variable, no CLI command, and changes no existing behaviour. It does not implement an external broker, a distributed worker, object storage, authentication, provider TTS, RSS, cloud deployment, or Kubernetes/Terraform, and it is not a distributed system and does not run in the cloud. Phase 14E remains NOT STARTED and was not opened (intentionally bypassed). Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED.

# Phase 15B — Cloud Boundary Readiness

This phase draws the safe, load-bearing seams for cloud growth before any cloud
span is built. It is derived from the proven local contracts locked through
Phase 15A and the as-built mapping locked in Phase 14D, not from a greenfield
cloud design. Its job is to make the eventual cloud work narrower and more
obvious — not to build the cloud.

The discipline is:

```text
Build local behavior before mapping cloud architecture.    (through Phase 14C)
Map cloud architecture before naming runtime shape.        (Phase 14D, LOCKED)
Name the runtime shape before drawing cloud seams.         (Phase 15A, LOCKED)
Draw the cloud seams before building any cloud span.       (Phase 15B, here)
```

Phase 15B turns four cloud-growth seams from prose into one small, typed,
testable readiness model that the existing local process can describe itself
with — provider-neutral, pure data, and changing nothing.

It builds on, and does not modify, these locked documents:

- `docs/phase15a-cloud-runtime-skeleton.md` — the locked runtime role skeleton.
- `docs/phase14d-cloud-distributed-architecture-baseline.md` — the locked
  as-built mapping of local contracts to a future cloud architecture.
- `docs/phase14d-deferred-cloud-work-register.md` — the prior deferred register.

The Phase 15B deferred work is tracked in
`docs/phase15b-deferred-cloud-work-register.md`.

---

## 1. Purpose

Phase 15B answers four questions with typed, pure-data contracts rather than prose:

> For each of the queue/worker, artifact/storage, observability/export, and
> recovery/idempotency seams: what is locally active and proven, what is
> deferred to a future phase, and what must remain true before that seam may
> safely cross from local-first into cloud-native implementation?

Concretely, Phase 15B delivers a `storytime.runtime.boundary_readiness` module
that produces a `BoundaryReadinessSnapshot` with four nested boundary summaries.
Each summary names the active local backend, the source of truth, the current
guarantees, the invariants required before cloud, the deferred capabilities, and
the explicit non-goals. The model is pure data: constructing it starts no
worker, claims no queue work, binds no socket, and opens no database.

The winning outcome is honest and almost underwhelming in code: StoryTime can
now state and test what must be true before each seam grows cloud behaviour,
while the running system stays exactly the local-first, observability-native
proof it already is.

---

## 2. Non-goals

Phase 15B is deliberately small — one pure-data module plus documentation,
tests, and state records. It explicitly does not implement:

- an external broker, a distributed worker runtime, or any distributed claim/lease change;
- object storage, signed/time-limited links, or public artifact serving;
- authentication, public ingress, or wildcard CORS;
- cloud deployment, Kubernetes, Terraform, Helm, or blue/green mechanics;
- a telemetry collector, vendor exporter, dashboards, service-level objectives, or alerting;
- a distributed idempotency store, distributed locks, a new retry engine, dead-letter handling, or a scheduler;
- provider TTS, audio, or RSS;
- any frontend control-plane expansion, polling, WebSockets, or EventSource;
- any new dependency or new environment variable.

Phase 15B is not a distributed system and does not run in the cloud. It changes
no WorkQueue, ArtifactStore, StateStore, recovery, or observer semantics, and it
wraps, proxies, or adapts none of those contracts.

---

## 3. Locked Phase 15A baseline (what this builds on)

Phase 15A locked a pure-data runtime role vocabulary (`api` / `worker` /
`combined`, default `combined`), a configuration-derived health/readiness model,
and a runtime config boundary reading only `STORYTIME_RUNTIME_ROLE`. Phase 15B
consumes that unchanged: the boundary-readiness snapshot is generated for a
runtime role, and the queue seam reports as not-applicable for the `api` role
(which does not drain or claim queue work) and locally active for the `worker`
and `combined` roles. Phase 15A remains LOCKED; Phase 15B does not re-litigate it.

---

## 4. Why Phase 15B combines the prior 15B–15D seams

The earlier roadmap split queue, artifact, observability, and recovery into
separate cloud rounds. In practice these four seams share one readiness shape:
each has a proven local backend, a backend-owned source of truth, a set of
invariants that any cloud implementation must preserve, and a set of deferred
capabilities. Modelling them with one shallow, provider-neutral readiness model
is clearer and less error-prone than four parallel frameworks, and it keeps the
phase boring: one module, one document, one register, one test file. The cloud
implementations themselves remain separate, deferred future work.

---

## 5. Readiness model overview

The model lives in `storytime.runtime.boundary_readiness` and is pure data:

- `BoundaryStatus` — a closed `StrEnum`: `local-active` or `not-applicable`.
  There is deliberately no cloud-certifying value.
- `OverallReadiness` — a closed `StrEnum`: `ready-for-local` or (fail-closed)
  `blocked`.
- `parse_boundary_status` — case-insensitive, fails closed on any unknown value
  so an unknown status can never silently pass.
- `BoundarySummary` — a frozen dataclass per seam: `boundary_name`,
  `active_backend`, `status`, `source_of_truth`, `current_guarantees`,
  `required_before_cloud`, `deferred_capabilities`, `explicit_non_goals`,
  `known_blockers`.
- `BoundaryReadinessSnapshot` — a frozen dataclass holding the four summaries
  plus the runtime role and deployment; it derives `overall_status`, aggregate
  `blockers`, and aggregate `deferred_capabilities`, and renders a safe,
  JSON-friendly `to_summary()` with no secrets or paths.

`evaluate_boundary_readiness(runtime_config, config)` is a pure function of its
inputs. The model clearly distinguishes active local capability (the status and
guarantees), future deferred capability (the deferred list and the
required-before-cloud invariants), and forbidden current capability (the
explicit non-goals).

---

## 6. Queue + worker boundary

The active queue backend is the local durable work queue behind the existing
WorkQueue port, drained by the single in-process local worker. The source of
truth is backend-owned durable state, not any observation stream. Claim, lease,
completion, failure, and attempt-limit semantics are the existing locked
behaviour and are unchanged. Before any cloud queue may cross this seam, single
delivery-effect claim semantics, cross-worker lease safety, and idempotent stage
execution must be proven, and durable backend state must remain authoritative.
An external/cloud queue transport, a replica-safe worker pool, dead-letter
handling, and backoff expansion are deferred. The `api` role reports this seam
as not-applicable because it does not drain or claim queue work.

---

## 7. Artifact + object-storage boundary

The active artifact backend is local filesystem storage behind the existing
ArtifactStore port, written by the worker and surfaced read-only by the
read-model. The source of truth is backend-owned storage plus the manifest /
envelope / SHA-256 semantics; the browser never learns a path, URL, or
credential. Key normalization, envelope validation, hash verification, and
archive hygiene are unchanged. Before any object-storage backend may cross this
seam, it must preserve key normalization, reject path traversal, keep envelope
and hash validation intact, and keep access server-mediated. A managed
object-storage backend, server-mediated time-limited links, and public serving
are deferred.

---

## 8. Observability export boundary

StoryTime is already observability-native. The active observability backend is
the in-process, fail-soft queue/worker observation with a stdlib-only event
boundary; the event vocabulary is native to the StoryTime domain and the
optional tracing dependency stays confined to its adapter. Observations are
explanatory signals only and are never the source of truth for queue, artifact,
recovery, or run state. Before observations may export to an external telemetry
backend, the export path must map native domain events without back-propagating
vendor naming into the core domain model, and observations must remain
explanatory rather than becoming control-plane state. Cloud/vendor export,
collector/vendor field mapping, dashboards, service-level objectives, and
alerting are deferred.

---

## 9. Recovery / idempotency / distributed-safety boundary

This is the most dangerous seam. The active recovery backend is the
backend-owned durable recovery lineage and eligibility recorded in the local
store and decided by the backend; a single in-process worker prevents double
execution within one process. Eligibility, attempt limits, and lineage are read
from durable state, never from observations. Before recovery may operate across
distributed infrastructure, cross-worker duplicate prevention and distributed
coordination must be backend-decided and durable, and attempt-limit and
eligibility semantics must remain unchanged. A distributed idempotency store,
cross-worker duplicate prevention, cloud retry orchestration, and dead-letter
replay are deferred. Phase 15B does not change any recovery code.

---

## 10. Runtime-role integration

The snapshot is generated for a Phase 15A runtime role. The `api` role reports
the queue seam as not-applicable (it does not claim or drain work) and exposes
no API behaviour through the readiness model. The `worker` role reports queue
readiness and exposes no public API. The `combined` role reports local/dev
readiness and remains representational and non-supervisory: the readiness model
imports no concurrency primitive and starts no API or worker loop. Combined mode
does not become a process supervisor.

---

## 11. Configuration stance

Phase 15B introduces no new environment variable. It reads only the existing
`STORYTIME_RUNTIME_ROLE` from Phase 15A, indirectly via the runtime config. It
adds no queue, artifact, observability, or recovery backend configuration, and
no placeholder or "local-only for now" config keys that would become future
compatibility burdens. Readiness is expressed entirely through pure-data
contracts and documentation.

---

## 12. What remains deferred

All cloud-growth capability beyond drawing the seams is deferred and recorded in
`docs/phase15b-deferred-cloud-work-register.md`: an external/cloud queue
transport and replica-safe worker pool; a managed object-storage backend and its
access strategy; cloud telemetry export and collector/vendor mapping; a
distributed idempotency store, cross-worker duplicate prevention, cloud retry
orchestration, and dead-letter replay; authentication and secrets; cloud runtime
deployment and orchestration; and dashboards, service-level objectives, and
alerting. None of these exist; Phase 15B neither builds nor starts them.

---

## 13. Phase 15C readiness implications

Phase 15C is the likely first cloud infrastructure skeleton candidate — the
narrow place where one of these seams could first gain a real, provider-neutral
adapter boundary behind an existing port, proven against the invariants this
phase records. Phase 15C is **not** designed here and remains NOT STARTED. Phase
15B only draws the seams and states the invariants; it does not start Phase 15C
and does not mark any later phase active.

---

## 14. Validation expectations

Phase 15B is validated by the full locked gate, expected green in the canonical
POSIX/Linux environment:

- `uv run pytest` — the existing suite plus the new
  `tests/test_cloud_boundary_readiness.py` cases (the readiness model, the four
  boundaries, runtime-role integration, boundary preservation including the
  provider-token scan, and the phase-state discipline records).
- `uv run ruff check .` — lint clean.
- `uv run mypy src` — strict type-check clean; the module is fully annotated.
- `uv run lint-imports` — both contracts kept (the module imports no tracing
  dependency).
- `uv run storytime doctor` — unchanged: it adds no CLI command and no doctor
  check.

A behaviour-level expectation accompanies the gate: the default role is
`combined`, every boundary reports `local-active` (or `not-applicable` for the
queue seam on the `api` role), the overall status is `ready-for-local`, and no
existing behaviour changes.

---

## 15. Explicit statement — no cloud behavior implemented

Phase 15B implements no cloud / distributed behavior. No external broker,
distributed worker, object storage, authentication, telemetry export, collector,
dashboard, scheduler, distributed lock, or dependency was added. The
`storytime.runtime.boundary_readiness` module is pure, provider-neutral data:
it names, for four seams, what is locally active, what is deferred, and what must
remain true before cloud implementation. The running system remains a
local-first, observability-native, single-process proof; the cloud seams named
here are a readiness map, and a later phase must provide the evidence each
boundary requires before any cloud behavior is trusted.
