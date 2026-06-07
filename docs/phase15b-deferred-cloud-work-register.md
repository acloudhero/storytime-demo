> **Phase 15B — Deferred Cloud Work Register (current implementation candidate; pending review; NOT locked).** This register tracks the cloud-growth work that Phase 15B deliberately defers. Phase 15A is LOCKED; Phase 15B is STARTED as the current candidate; Phase 14E remains NOT STARTED and was not opened; Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED. Nothing here is implemented or started — it is a deferral record, not a roadmap that opens future phases. Entries are provider-neutral on purpose; specific vendors are intentionally not named.

# Phase 15B — Deferred Cloud Work Register

Each entry records: a description, why it is deferred, what it depends on, the
risk of implementing it too early, and the expected future phase or phase
family. None of these items is started by Phase 15B.

---

## Queue / worker

### External / cloud queue transport
- **Description:** a managed/hosted message-broker queue transport behind the existing WorkQueue port.
- **Why deferred:** Phase 15B only draws the seam; a transport swap must preserve claim semantics exactly.
- **Depends on:** proven single delivery-effect claim semantics and durable backend state remaining authoritative.
- **Risk if too early:** double execution or lost work if claim/lease semantics are not preserved.
- **Expected phase:** Phase 15C+ (first cloud infrastructure skeleton candidate).

### Replica-safe distributed worker pool
- **Description:** more than one worker draining the queue concurrently.
- **Why deferred:** cross-worker safety is unproven; only a single in-process worker exists today.
- **Depends on:** lease ownership, reclaim-on-expiry, and idempotent stage execution.
- **Risk if too early:** duplicate execution and corrupted run state under concurrency.
- **Expected phase:** Phase 15C+ family.

### Dead-letter handling and replay; backoff/retry expansion
- **Description:** dead-letter capture, replay, and richer backoff policy.
- **Why deferred:** current attempt limits and recovery eligibility are backend-decided and bounded; expansion is out of scope.
- **Depends on:** distributed-safe recovery semantics.
- **Risk if too early:** unbounded or duplicated retries crossing the recovery boundary.
- **Expected phase:** Phase 15C+ family.

---

## Artifact / storage

### Managed object-storage backend
- **Description:** a managed object-storage backend behind the existing ArtifactStore port.
- **Why deferred:** Phase 15B preserves local filesystem storage and its manifest/envelope/hash semantics.
- **Depends on:** preserved key normalization, path-traversal rejection, and envelope + SHA-256 validation.
- **Risk if too early:** integrity or traversal-safety regressions if validation is weakened.
- **Expected phase:** Phase 15C+ family.

### Server-mediated access links; public artifact serving
- **Description:** time-limited, server-mediated download links and any public serving.
- **Why deferred:** the browser must never learn a path, URL, or credential; public serving is a non-goal now.
- **Depends on:** a managed object-storage backend and a server-mediated access contract.
- **Risk if too early:** leaking backend-owned paths/credentials to the browser.
- **Expected phase:** Phase 15C+ family.

---

## Observability / export

### Cloud telemetry export and collector/vendor mapping
- **Description:** exporting native domain events to an external telemetry backend.
- **Why deferred:** StoryTime stays observability-native; export must not back-propagate vendor naming into the domain.
- **Depends on:** a stable native event vocabulary and a one-way mapping to the external backend.
- **Risk if too early:** observations becoming control-plane state or the domain model adopting vendor semantics.
- **Expected phase:** Phase 15C+ family.

### Dashboards, service-level objectives, alerting
- **Description:** operational dashboards, SLOs, and alerting on exported telemetry.
- **Why deferred:** depends on an export path that does not yet exist.
- **Depends on:** cloud telemetry export.
- **Risk if too early:** building dashboards on an unstable or absent export contract.
- **Expected phase:** Phase 15C+ family.

---

## Recovery / idempotency / distributed safety

### Distributed idempotency store and cross-worker duplicate prevention
- **Description:** a durable, backend-decided idempotency/coordination mechanism across workers.
- **Why deferred:** the most dangerous seam; only single-process double-execution prevention exists today.
- **Depends on:** distributed-safe, backend-owned coordination and unchanged eligibility/attempt-limit semantics.
- **Risk if too early:** silent duplicate execution or split-brain recovery decisions.
- **Expected phase:** Phase 15C+ family (likely the last and most carefully gated).

### Cloud retry orchestration; dead-letter replay
- **Description:** orchestrated retry/replay across distributed infrastructure.
- **Why deferred:** retry must remain bounded and backend-decided.
- **Depends on:** distributed idempotency and duplicate prevention.
- **Risk if too early:** runaway or duplicated retries.
- **Expected phase:** Phase 15C+ family.

---

## Cross-cutting

### Authentication and secrets
- **Description:** authentication, public ingress, and secret handling.
- **Why deferred:** the local contract is loopback-only with no auth; introducing it is a separate, security-sensitive effort.
- **Depends on:** a cloud runtime that actually exposes a network surface.
- **Risk if too early:** attack surface with no operational need.
- **Expected phase:** a later cloud phase, scoped explicitly.

### Cloud runtime deployment and orchestration
- **Description:** cloud deployment, container orchestration, and infrastructure-as-code.
- **Why deferred:** there is no cloud behaviour to deploy yet.
- **Depends on:** at least one proven cloud adapter behind an existing port.
- **Risk if too early:** infrastructure complexity with nothing real to run.
- **Expected phase:** a later cloud phase.

### Provider TTS; RSS publishing
- **Description:** real provider-backed text-to-speech and RSS feed publishing.
- **Why deferred:** out of the cloud boundary-readiness mission; long-standing deferred product work.
- **Depends on:** separate product phases unrelated to cloud seam readiness.
- **Risk if too early:** scope creep that mixes product features into infrastructure readiness.
- **Expected phase:** a separate product phase family.
