# Phase 14 — Cloud / Distributed Roadmap (future boundaries)

**First-read state (current).** Phase 14A.1 — Local Live Proof Loop Before
Cloud — is **LOCKED**. Phase 14B.1 — Live Proof Loop Hardening / Operator
Trust — is **LOCKED**. Phase 14C.1 — Local Durable Queue / Worker Shape Proof —
is **LOCKED**. Phase 14C.2 — Contracts-as-Built / Cloud-Distributed Seam
Baseline — is **LOCKED**. Phase 14C.3 — Object Storage Boundary / Artifact
Store Adapter — is **LOCKED**. Phase 14C.4 — Minimal Observability Boundary for
Queue/Worker — is **LOCKED** (its observer events are explanatory only and are
not the recovery-lineage source of truth). Phase 14C.5.1 — Durable Recovery
Control Plane Boundary — is **LOCKED** (locked using
`storytime-phase14c5-1-durable-recovery-control-plane-boundary.tar.gz`, SHA-256
`73a9ee1bdcbca295037f4852375d3f6b1ff155c3a0ea9d1b0fe498de3862e604`). Phase 14D — Cloud / Distributed Architecture Baseline from
Proven Local Contracts — is **LOCKED** (locked using
`storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256
`a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`) and is the
last locked phase. Phase 14D is the documentation-and-mapping round that maps the
proven, locked local contracts (request acceptance, the `WorkQueue` port, the
`LocalWorker`, the `ArtifactStore` port, the durable `recovery_action` control
plane, in-process observation, and the operator read-model) to their future
cloud / distributed equivalents on paper, and recommends how a later Phase 15
could be decomposed. It implements **no** cloud behavior: no cloud queue, no
external broker, no dead-letter queue, no automatic retries, no backoff, no
retry scheduler, no distributed worker, no cloud lease, no distributed lock, no
object/cloud storage, no Kubernetes, no Terraform, no authentication, and no new
dependency. The previously sketched provider-TTS / frontend-audio / RSS
content-production items (formerly the 14D.1–14D.4 labels) are **deferred future
work**, not part of Phase 14D. Phase 14E and Phase 15 are **NOT STARTED**. This
document describes target *future* boundaries for a hosted/distributed system;
**none of the cloud/distributed work described here is implemented or started.**
(Historical note: earlier revisions of this file called the reserved future
combined bundle "Phase 14B.1"; that label now denotes the locked hardening
round. Phase 14D is the as-built cloud/distributed mapping round, and the
reserved future cloud/distributed runtime work is Phase 15 and later.)

> Cloud is not useful until the local live proof loop is undeniable. This
> roadmap exists so the local-live foundation is built with the eventual hosted
> shape in mind — not as a commitment to build the hosted shape now.

## 1. Why local-live first

A hosted/distributed deployment only adds value once the local proof loop is
real and trustworthy. Phase 14A.1 establishes backend-owned durable state, a
controlled action boundary, and an honest read model locally. Those same
contracts are what a future cloud deployment would host.

## 2. Future service boundaries (not started)

- **Cloud API / auth boundary** — a hosted HTTP API in front of the command
  handlers, with authentication and authorization. Provider and cloud
  credentials would live server-side only and never reach the browser.
- **Queue / orchestrator** — to accept work requests, sequence them, and
  decouple request handling from execution.
- **Worker boundary** — workers that perform real synthesis and assembly off
  the request path (where provider-backed TTS and ffmpeg would eventually run).
- **Object storage boundary** — durable artifact storage off the local
  filesystem, addressed by the same relative-key discipline the state store
  already uses.
- **Durable hosted state** — the SQLite source-of-truth pattern would be
  carried forward to a hosted durable store, preserving the "backend owns
  truth" invariant.

## 3. Invariants carried forward

Whatever the deployment, these remain fixed: the backend owns truth and durable
state; the browser only requests and never owns durable state or holds
credentials; artifacts, manifests, hashes, and audit events are backend-owned;
and honest framing (mock is labelled mock; acceptance is not success) is
preserved.

## 4. Explicitly out of scope for Phase 14A.1

Docker, Kubernetes, Terraform, Helm, any cloud deployment resource, any external
service dependency, real paid provider invocation, RSS publishing, audio
playback, public network binding, and wildcard CORS. None of these are added in
Phase 14A.1; all are reserved for Phase 14C.1+ and are NOT STARTED.

## 5. Where Phase 14B.1 sits on this path

Phase 14A.1 *proved* a local, backend-owned execution path. Phase 14B.1 does not
move toward the cloud; it **hardens operator trust** in that local path so the
contracts a cloud deployment would later host are well-defined and reviewable
first. Concretely, Phase 14B.1 maps onto the future boundaries like this:

| Phase 14B.1 (local, now) | Maps later to (Phase 14C.1+, not started) |
| --- | --- |
| Allowlisted `scenario` on the proof-run action; deterministic failure runs | Hosted API request validation + an auth boundary; real failures from workers |
| Failed `stage_execution` + `RunFailed` event + failure reason in the read model | The same durable failure contract surfaced from a queue/worker over a hosted API |
| Evidence artifact written under a relative run key | An object-storage boundary addressed by the same relative-key discipline |
| Health DTO with no absolute paths; typed request/response/error DTOs | Stable hosted API contracts (the typed shapes are the seam a cloud client would bind to) |
| SQLite source-of-truth, durable across restart | A managed/Postgres durable store carrying the "backend owns truth" invariant |
| Mock, in-process stage walk | OpenTelemetry traces/metrics/logs + a provider-adapter boundary around real synthesis |

The discipline is deliberate: **14A.1 proved local execution; 14B.1 hardens the
trust, evidence, and contracts of that local execution; cloud/distributed work
is Phase 14C.1+ and has NOT STARTED.** Hardening the contracts before hosting
them is what keeps a future cloud step small and reviewable rather than a
rewrite. Phase 14B.1 implements none of the boundaries in section 2 — it only
sharpens the local contracts they would later be built on.

## 6. Phase 14C.1 update — the local execution spine is built

Phase 14C.1 — Local Durable Queue / Worker Shape Proof — has built the first of
these seams **locally**: request acceptance now enqueues a durable work item and
a single bounded local worker claims and executes it, with atomic claiming,
lease-based stale-claim recovery, and no double execution (see
`docs/phase14-queue-worker.md`). The queue is a replaceable port with a SQLite
adapter, so the queue/worker boundary in section 2 now exists as a real,
testable local contract rather than only a description.

This does not change the discipline: the queue/worker is LOCAL only — not a
cloud queue, a distributed system, or an external broker. Documenting these
contracts-as-built for a future hosted/distributed adapter is **Phase 14C.2**
(Contracts-as-Built / Cloud-Distributed Seam Baseline); the object-storage
adapter is **14C.3**; and real cloud/distributed deployment remains later still
and NOT STARTED. The mapping in section 5 stands: 14A.1 proved local execution,
14B.1 hardened trust, 14C.1 proves the local durable execution shape, and cloud
is a hosting problem to be addressed only once these local contracts are locked.
