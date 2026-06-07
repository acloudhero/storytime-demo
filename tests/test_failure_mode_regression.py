"""Phase 11C — failure-mode / regression hardening: state-doc discipline tests.

These tests protect an existing project invariant that, before Phase 11C, was
enforced only by prose and review: the State Preservation Bundle must describe
the *current* phase honestly. Concretely, the living state docs must keep the
current phase marked as a pending-review implementation candidate, keep the
correct phase as the last locked phase, never claim a future phase has started
or locked, and never erase the append-only historical lock records that
earlier phases wrote.

This is a regression surface, not a product feature: if a future phase's state
synchronization drifts — for example by marking a future phase started or
locked, or by truncating the append-only history — these tests fail. The tests
read only repository documents; they need no network, no database, and no
toolchain beyond Python.

The expectations below are deliberately tolerant about wording (they match
case-insensitively and allow ordinary prose) and strict only about the claims
that would represent real drift.

Phase 12B note: this module was introduced in Phase 11C as a phase-specific
state-discipline guard, and advanced in Phase 12A. Phase 12B — Portfolio
Evidence Pack / Reviewer Assets — advanced it again (under the explicit §5
mechanical exception authorized for Phase 12B) so it tracks the Phase 12B
current-state expectations: Phase 12A was the last locked phase, Phase 12B was
the current implementation candidate, and the guard protected against a
premature Phase 12B lock, a premature Phase 12 closure, and a premature Phase
12C (or later) start.

Phase 12C note: Phase 12C — Portfolio Demo Narrative / Public Presentation
Kit — advanced this guard again, under the same narrow, explicitly authorized
mechanical exception, so it tracks the Phase 12C current-state expectations.
Phase 12B (with its Phase 12B.1 / 12B.2 / 12B.3 cleanup sub-rounds folded into
its lock lineage) is now the last locked phase, Phase 12C is the current
implementation candidate, and the guard now protects against a premature
Phase 12C lock, a premature Phase 12 closure, and a premature Phase 12D (or
later) start. The guardrail concept is unchanged and coverage is strengthened,
not weakened — only the phase the guard is anchored to moved forward, and the
append-only lock-record checks now also require the Phase 12B lock record.

Phase 12D note: Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff
Definition — advanced this guard again, under the same narrow, explicitly
authorized mechanical exception, so it tracks the Phase 12D current-state
expectations. Phase 12C — Portfolio Demo Narrative / Public Presentation Kit —
is now the last locked phase, Phase 12D is the current implementation
candidate, and the guard now protects against a premature Phase 12D lock, a
premature Phase 12 closure, and a premature Phase 12E (or later) start. Phase
12D is a closure-definition round: it does not itself close Phase 12 — closing
Phase 12 remains a separate, explicit review/lock decision — so "phase 12 is
closed" stays forbidden. The guardrail concept is unchanged and coverage is
strengthened, not weakened — only the phase the guard is anchored to moved
forward, and the append-only lock-record checks now also require the Phase 12C
lock record.

Phase 13A note: Phase 13A — Portfolio Website / Operator GUI Architecture
Baseline — advanced this guard again, under the same narrow, explicitly
authorized mechanical exception, so it tracks the Phase 13A current-state
expectations. Phase 12D — Phase 12 Closure Plan / Final Portfolio Handoff
Definition — was locked out-of-band and, with it, Phase 12 — Portfolio / SE
Demo Packaging — was formally CLOSED; Phase 12D is now the last locked phase.
Phase 13 — Portfolio Website / Operator GUI — is STARTED, and Phase 13A is the
current implementation candidate. The guard now protects against a premature
Phase 13A lock, a premature Phase 13 closure, and a premature Phase 13B (or
later) start. It also adds a new check: Phase 13A is a documentation-only
architecture-baseline round that designs the portfolio website and the
decoupled operator GUI on paper but does not build them, so the current-state
docs must never claim Phase 13A implemented the frontend, the portfolio
website, or the operator GUI. Phase 13 is legitimately STARTED, so "phase 13
has started" / "phase 13 is in progress" are intentionally NOT forbidden —
only a premature Phase 13 *closure* is. The guardrail concept is unchanged and
coverage is strengthened, not weakened — only the phase the guard is anchored
to moved forward, the append-only lock-record checks now also require the
Phase 12D lock record, and the new no-frontend-implementation check is added.

Phase 13B note: Phase 13B — Typed Static Portfolio Shell / Minimal Visual
Pipeline Scaffold — advanced this guard again, under the same narrow,
explicitly authorized mechanical exception, so it tracks the Phase 13B
current-state expectations. Phase 13A was locked, so Phase 13A is now the last
locked phase and Phase 13B is the current implementation candidate. The guard
now protects against a premature Phase 13B lock, a premature Phase 13 closure,
and a premature Phase 13C (or later) start. Phase 13B is the first frontend
round: it legitimately builds a static, read-only, demo-data-backed frontend
shell, so — unlike the Phase 13A check — building a frontend is no longer
forbidden. The no-frontend-implementation check is therefore replaced by a
no-overclaim check: Phase 13B is static, read-only, and backed by demo data
only, so the current-state docs must never claim Phase 13B is backend-
connected, uses live data, implements mutations, or is production-hosted /
cloud-deployed. The guardrail concept is unchanged and coverage is
strengthened, not weakened — only the phase the guard is anchored to moved
forward, and the append-only lock-record checks now also require the Phase 13A
lock record.

Phase 13C note: Phase 13C — Deterministic Read-Only Static Export / Frontend
Data Alignment — advanced this guard again, under the same narrow, explicitly
authorized mechanical exception, so it tracks the Phase 13C current-state
expectations. Phase 13B was locked, so Phase 13B is now the last locked phase
and Phase 13C is the current implementation candidate. The guard now protects
against a premature Phase 13C lock, a premature Phase 13 closure, and a
premature Phase 13D (or later) start. Phase 13C legitimately produces a
deterministic, read-only static data export and aligns the frontend to it, so
producing a static export is not forbidden; the no-overclaim check is retained
and re-anchored to Phase 13C: the current-state docs must never claim Phase
13C is backend-connected, uses live data, implements mutations, or is
production-hosted / cloud-deployed. The guardrail concept is unchanged and
coverage is strengthened, not weakened — only the phase the guard is anchored
to moved forward, and the append-only lock-record checks now also require the
Phase 13B lock record.

Phase 13D note: Phase 13D — Operator Workflow View Expansion (Governance /
Safety, Failure / Recovery) — advanced this guard again, under the same
narrow, explicitly authorized mechanical exception, so it tracks the Phase
13D current-state expectations. Phase 13C was locked, so Phase 13C is now the
last locked phase and Phase 13D is the current implementation candidate. The
guard now protects against a premature Phase 13D lock, a premature Phase 13
closure, and a premature Phase 13E (or later) start. Phase 13D legitimately
expands the placeholder Governance / Safety and Failure / Recovery views into
real read-only operator views, built against the locked Phase 13C
deterministic static export — so expanding those views is not forbidden; the
no-overclaim check is retained and re-anchored to Phase 13D: the
current-state docs must never claim Phase 13D is backend-connected, uses live
data, implements mutations (the recovery / review actions remain visibly
disabled), or is production-hosted / cloud-deployed. The guardrail concept is
unchanged and coverage is strengthened, not weakened — only the phase the
guard is anchored to moved forward, and the append-only lock-record checks
now also require the Phase 13C lock record.

Phase 13K note: Phase 13K — Demo Walkthrough Refresh / Governed Local Chain
Story Path — advanced this guard again, under the same narrow, explicitly
authorized mechanical exception, so it now tracks the Phase 13K current-state
expectations. Phase 13J — Operator GUI Polish / Demo-Local Alignment — was
locked, so Phase 13J is now the last locked phase and Phase 13K is the current
implementation candidate. Phase 13K is a demo / walkthrough / reviewer-story
refresh: it makes the existing system's story truthful, scannable, and
evidence-mapped, designates one canonical walkthrough surface, and reconciles
stale demo/portfolio docs; it adds NO runtime capability. The no-overclaim check
is re-anchored to Phase 13K and forbids claiming it added capability it does not
(new backend behavior, a new local bridge action, a generate_tts action, any
frontend TTS generation / Generate-audio control, an audio player, file /
directory / URL / credential inputs, a provider selection that changes runtime
behavior, browser durable storage, automatic reload / polling / WebSocket /
EventSource, cloud / distributed / full Local mode, RSS publishing, a real
provider integration, batch generation, or conflating mock output with real
provider audio, retry acceptance with success, or manual reload with live sync).
Phase 13K is the terminal planned subphase: there is no Phase 13L, and Phase 13
closure is a separate later decision. The guard now protects against a premature
Phase 13K lock, a premature Phase 13 closure, and a phantom Phase 13L start; the
future-phase fragment scan now reads `13l` (Phase 13K is the current candidate,
and the dotted `13i` / `13j` tokens — which the fragment splitter breaks on `.`
— are covered by the explicit substring list), the next-phase handoff check is
re-anchored to Phase 13 closure framing, and the append-only lock-record checks
now also require the Phase 13J lock record. The guardrail concept is unchanged
and coverage is strengthened, not weakened — only the phase the guard is
anchored to moved forward.

Phase 13L note: Phase 13L — Phase 13 Closure / Demo-Local Completion Lock —
advanced this guard again, under the same narrow, explicitly authorized
mechanical exception, so it now tracks the Phase 13L current-state
expectations. Phase 13K — Demo Walkthrough Refresh / Governed Local Chain Story
Path — was locked (GPT preliminary verification PASS, Gemini implementation
review SAFE TO LOCK, no required edits), so Phase 13K is now the last locked
phase and Phase 13L is the current implementation candidate. Phase 13L is a
closure / documentation round: it records Phase 13K as locked, prepares the
Phase 13 closure as a candidate, summarizes the Demo + Local proof track,
preserves the canonical demo walkthrough as the reviewer path, and writes an
architecture-first Phase 14 readiness handoff. It adds NO runtime capability
and changes no source, frontend, or dependency. The no-overclaim check is
re-anchored to Phase 13L and forbids claiming it added capability it does not
(backend behavior, a local bridge action, frontend TTS generation / audio
playback, a real provider integration, browser durable storage, polling / live
sync, cloud / distributed / full Local mode, RSS publishing, authentication,
cloud deployment, or any Phase 14 implementation). Like Phase 12D before it,
Phase 13L is a closure round that does NOT itself close Phase 13 — closing
Phase 13 remains a separate, explicit review/lock decision — so "phase 13 is
closed" stays forbidden until Phase 13L locks. The future-phase fragment scan
now reads `phase 14` (Phase 13L is the current candidate, Phase 13K … 13J are
legitimately locked, and the dotted sub-phase tokens are covered by the
explicit substring list); the guard now additionally protects against a
premature Phase 13L lock, a premature Phase 13 closure, a phantom Phase 13M,
and any claim that Phase 14 / 14A has started, is locked, or is implemented
(Phase 14A is only the next *proposed* architecture baseline, NOT STARTED). New
checks require Phase 13K to be recorded as locked and Phase 14 to be framed as
not started, and the append-only lock-record checks now also require the Phase
13K lock record. The guardrail concept is unchanged and coverage is
strengthened, not weakened — only the phase the guard is anchored to moved
forward.

Phase 14A.1 note: Phase 14A.1 — Local Live Proof Loop Before Cloud — advanced
this guard again, under the same narrow, explicitly authorized mechanical
exception, so it now tracks the Phase 14A.1 current-state expectations. Phase
13L — Phase 13 Closure / Demo-Local Completion Lock — was locked and, with it,
Phase 13 — Portfolio Website / Operator GUI — was formally CLOSED; Phase 13L is
now the last locked phase. Phase 14 — Live System / Cloud-Distributed — is now
STARTED, and Phase 14A.1 is the current implementation candidate (pending
review, NOT locked). Unlike the Phase 13L closure round, Phase 14A.1 is a real
implementation round: it adds a loopback-only local-live HTTP API
(src/storytime/local_live), a durable backend-owned proof-run harness that
persists real run/stage/event/artifact state to SQLite (surviving a server
restart), a `storytime local-live` command, and a frontend "Live Proof Loop"
surface. Because that backend behavior is now real, the no-overclaim check is
re-anchored: it no longer forbids claiming new backend/frontend behavior (that
is now true) and instead forbids the capabilities Phase 14A.1 deliberately does
NOT add — cloud/distributed mode, provider-backed TTS, frontend audio
generation, audio playback, RSS publishing, authentication, and cloud
deployment. The future-phase fragment scan now reads `phase 14b` (Phase 14 is
legitimately STARTED and Phase 14A.1 is the current candidate; the dotted
sub-phase tokens are covered by the explicit substring list); the guard now
protects against a premature Phase 14A.1 lock, a premature Phase 14 closure,
and any claim that the reserved Phase 14B.1+ bundle has started, is current, or
is locked (Phase 14B.1+ is NOT STARTED). New checks require Phase 13 to be
recorded as closed, Phase 13L as locked, and Phase 14 as started, and the
append-only lock-record checks now also require the Phase 13L lock record. The
guardrail concept is unchanged and coverage is strengthened, not weakened —
only the phase the guard is anchored to moved forward.

Phase 14B.1 note: Phase 14B.1 — Live Proof Loop Hardening / Operator Trust /
Cloud-Ready Boundary Preparation — advanced this guard again, under the same
narrow, explicitly authorized mechanical exception, so it now tracks the Phase
14B.1 current-state expectations. Phase 14A.1 — Local Live Proof Loop Before
Cloud — was LOCKED; Phase 14A.1 is now the last locked phase. Phase 14 remains
STARTED, and Phase 14B.1 is the current implementation candidate (pending
review, NOT locked). Phase 14B.1 is a real hardening round: it adds controlled,
deterministic, durable failure/recovery proof scenarios, operator-UX and
read-model/DTO hardening, Windows operator docs, and cloud-readiness docs. The
no-overclaim check is re-anchored to forbid claiming Phase 14B.1 added the
capability it deliberately does NOT add (cloud/distributed mode, provider-backed
TTS, frontend audio/TTS generation, audio playback, RSS publishing,
authentication, cloud deployment, or any Phase 14C.1+ work). The future-phase
fragment scan now reads `phase 14c` (Phase 14B.1 is the current candidate and
Phase 14A.1 is legitimately locked); the guard now protects against a premature
Phase 14B.1 lock, a premature Phase 14 closure, and any claim that the reserved
Phase 14C.1+ bundle has started, is current, or is locked (Phase 14C.1+ is NOT
STARTED). New checks require Phase 14A.1 to be recorded as locked and Phase
14C.1+ to be framed as not started, and the append-only lock-record checks now
also require the Phase 14A.1 lock record. The guardrail concept is unchanged and
coverage is strengthened, not weakened — only the phase the guard is anchored to
moved forward.

Phase 14C.1 note: Phase 14C.1 — Local Durable Queue / Worker Shape Proof —
advanced this guard again, under the same narrow, explicitly authorized
mechanical exception, so it now tracks the Phase 14C.1 current-state
expectations. Phase 14B.1 — Live Proof Loop Hardening / Operator Trust — was
LOCKED; Phase 14B.1 is now the last locked phase. Phase 14 remains STARTED, and
Phase 14C.1 is the current implementation candidate (pending review, NOT
locked). Phase 14C.1 is a real implementation round: it adds a LOCAL durable
work-queue port with a SQLite adapter, a bounded local worker that drains it,
and a request path that enqueues a durable work item instead of executing
inline — separating request acceptance from execution while remaining strictly
local and restart-durable. The no-overclaim check is re-anchored to forbid
claiming Phase 14C.1 implemented the capability it deliberately does NOT add (a
cloud/distributed system, a cloud queue / external broker / hosted execution /
production distributed orchestration, provider-backed TTS, frontend audio/TTS
generation, audio playback, RSS publishing, authentication, cloud deployment, or
any Phase 14C.2+/14D/14E work); those overclaim entries are positive-claim
phrases so honest negated wording cannot match. The future-phase fragment scan
now reads `phase 14d` (Phase 14C.1 is the current candidate and Phase 14C.2 is
the next reserved sub-phase, both legitimately named); the guard now protects
against a premature Phase 14C.1 lock, a premature Phase 14 closure, and any
claim that the reserved Phase 14C.2 / 14D / 14E phases have started, are current,
or are locked (they are NOT STARTED). New checks require Phase 14B.1 to be
recorded as locked and Phase 14D+ to be framed as not started, and the
append-only lock-record checks now also require the Phase 14B.1 lock record. The
guardrail concept is unchanged and coverage is strengthened, not weakened — only
the phase the guard is anchored to moved forward.

Phase 14C.2 note: Phase 14C.2 — Contracts-as-Built / Cloud-Distributed Seam
Baseline — advanced this guard again under the same narrow, explicitly
authorized mechanical exception, so it now tracks the Phase 14C.2 current-state
expectations. Phase 14C.1 — Local Durable Queue / Worker Shape Proof — was
LOCKED (using storytime-phase14c1-stale-partial-recovery-cleanup.tar.gz); Phase
14C.1 is now the last locked phase. Phase 14 remains STARTED, and Phase 14C.2 is
the current implementation candidate (pending review, NOT locked). Phase 14C.2
is a DOCS / CONTRACTS / GUARDRAIL round: it documents — in
docs/phase14-contracts-as-built.md — the seams Phase 14C.1 actually built (the
request-acceptance, queue-port, SQLite-adapter, worker-execution, stale-claim
and stale-partial recovery, read-model/DTO safety, and frontend boundary
contracts) and defines the cloud/distributed seam baseline for future phases
WITHOUT implementing any of it. The no-overclaim check is re-anchored to forbid
claiming Phase 14C.2 implemented a cloud/distributed system, a cloud queue /
external broker / object storage / hosted execution, an auth boundary, a
retry/recovery lineage, exactly-once distributed execution, provider-backed TTS,
frontend audio, or RSS publishing; those overclaim entries are positive-claim
phrases so honest negated wording cannot match. The future-phase fragment scan
still reads `phase 14d` (Phase 14C.2 is the current candidate and Phase 14C.3 is
the next reserved sub-phase, both legitimately named); the guard now protects
against a premature Phase 14C.2 lock, a premature Phase 14 closure, and any claim
that the reserved Phase 14C.3 / 14D / 14E phases have started, are current, or
are locked (they are NOT STARTED). New checks require Phase 14C.1 to be recorded
as locked, and the append-only lock-record checks now also require the Phase
14C.1 lock record. The guardrail concept is unchanged and coverage is
strengthened, not weakened — only the phase the guard is anchored to moved
forward.

Phase 14C.3 note: Phase 14C.3 — Object Storage Boundary / Artifact Store
Adapter — advanced this guard again under the same narrow, explicitly authorized
mechanical exception, so it now tracks the Phase 14C.3 current-state
expectations. Phase 14C.2 — Contracts-as-Built / Cloud-Distributed Seam
Baseline — was LOCKED (using
storytime-phase14c2-contracts-as-built-cloud-distributed-seam-baseline.tar.gz);
Phase 14C.2 is now the last locked phase. Phase 14 remains STARTED, and Phase
14C.3 is the current implementation candidate (pending review, NOT locked).
Phase 14C.3 is a backend artifact-boundary round: it puts artifact handling
behind a backend-owned ArtifactStore port with a single LOCAL filesystem
adapter (LocalFilesystemArtifactStore), validating logical keys (rejecting
absolute paths, .. traversal, backslash separators, and symlink escapes),
keeping artifacts under a configured root, and exposing only safe artifact
evidence so the browser never learns filesystem paths or storage credentials. It
adds no cloud/object store, no S3/MinIO adapter, no signed URLs, no public
artifact serving, no auth, no retry/recovery lineage, no observability
deepening, and no dependency; queue/worker execution semantics are unchanged.
The no-overclaim check is re-anchored to forbid claiming Phase 14C.3 implemented
S3/MinIO, cloud storage, signed URLs, public artifact serving, or any later
capability; those overclaim entries are positive-claim phrases so honest negated
wording cannot match. The future-phase fragment scan still reads `phase 14d`
(Phase 14C.3 is the current candidate and Phase 14C.4 is the next reserved
sub-phase, both legitimately named); the guard now protects against a premature
Phase 14C.3 lock, a premature Phase 14 closure, and any claim that the reserved
Phase 14C.4 / 14D / 14E phases have started, are current, or are locked (they
are NOT STARTED). New checks require Phase 14C.2 to be recorded as locked, and
the append-only lock-record checks now also require the Phase 14C.2 lock record.
The guardrail concept is unchanged and coverage is strengthened, not weakened —
only the phase the guard is anchored to moved forward.

Phase 14C.5.1 note: Phase 14C.5.1 — Durable Recovery Control Plane Boundary —
advanced this guard again under the same narrow, explicitly authorized mechanical
exception, so it now tracks the Phase 14C.5.1 current-state expectations. Phase
14C.4 — Minimal Observability Boundary for Queue/Worker — was LOCKED (using
storytime-phase14c4-minimal-observability-boundary-queue-worker.tar.gz, SHA-256
12b951e0a9b6b17f5c73aacf0d055b257bd4a715908f7f5078d401eae2a66d3b); Phase 14C.4 is
now the last locked phase, and its observer events are explanatory only — never
the durable recovery-lineage source of truth. Phase 14 remains STARTED, and Phase
14C.5.1 is the current implementation candidate (pending review, NOT locked).
Phase 14C.5.1 adds the smallest durable, backend-owned recovery control plane: a
durable recovery_action lineage table (source of truth), a backend-owned recovery
eligibility policy, duplicate-prevention and a bounded attempt limit, a recovery
read-model projection, local SQLite concurrency guardrails, and a cloud-queue
mapping CONTRACT document. It deliberately absorbs the previously planned local
recovery-control-plane scope from Phase 14C.5 through Phase 14C.10; those numbers
are historical planning labels only and are NOT separate active phases. The
no-overclaim check is re-anchored to forbid claiming Phase 14C.5.1 implemented a
cloud queue, an external broker (Redis/NATS/SQS/Temporal/Celery), a distributed
worker, a dead-letter queue, automatic retries, exponential backoff, a retry
scheduler, cloud leases, distributed locks, or any later capability; those
overclaim entries are positive-claim phrases so honest negated wording cannot
match. The future-phase fragment scan still reads `phase 14d` (Phase 14C.5.1 is
the current candidate and Phase 14D is the next reserved arc); the guard now
protects against a premature Phase 14C.5.1 lock, a premature Phase 14 closure, and
any claim that the reserved Phase 14D / 14E arcs have started, are current, or are
locked (they are NOT STARTED). New checks require Phase 14C.4 to be recorded as
locked, and the append-only lock-record checks now also require the Phase 14C.4
lock record. The guardrail concept is unchanged and coverage is strengthened, not
weakened — only the phase the guard is anchored to moved forward.

Phase 14C.4 note: Phase 14C.4 — Minimal Observability Boundary for
Queue/Worker — advanced this guard again under the same narrow, explicitly
authorized mechanical exception, so it now tracks the Phase 14C.4 current-state
expectations. Phase 14C.3 — Object Storage Boundary / Artifact Store Adapter —
was LOCKED (using
storytime-phase14c3-1-contracts-doc-state-wording-cleanup.tar.gz); Phase 14C.3
is now the last locked phase. Phase 14 remains STARTED, and Phase 14C.4 is the
current implementation candidate (pending review, NOT locked). Phase 14C.4 adds
a small backend-owned, in-process observability boundary for the local
queue/worker lifecycle: safe, vendor-neutral event names
(work.enqueued/claimed/started, stage.started/completed, artifact.recorded,
work.completed/failed) and safe fields (existing local identifiers, timestamps,
status), emitted fail-soft at the existing lifecycle points without changing
queue/worker semantics. It is ephemeral/in-process by default (no new database
table, broker, or stream) and exposes nothing new to the browser. The
no-overclaim check is re-anchored to forbid claiming Phase 14C.4 implemented an
OpenTelemetry SDK, a collector, a Prometheus endpoint, dashboards, vendor
exporters, alerting, SLOs, sampling, distributed tracing, cloud telemetry, or
any later capability; those overclaim entries are positive-claim phrases so
honest negated wording cannot match. The future-phase fragment scan still reads
`phase 14d` (Phase 14C.4 is the current candidate and Phase 14C.5 is the next
reserved sub-phase, both legitimately named); the guard now protects against a
premature Phase 14C.4 lock, a premature Phase 14 closure, and any claim that the
reserved Phase 14C.5 / 14D / 14E phases have started, are current, or are locked
(they are NOT STARTED). New checks require Phase 14C.3 to be recorded as locked,
and the append-only lock-record checks now also require the Phase 14C.3 lock
record. The guardrail concept is unchanged and coverage is strengthened, not
weakened — only the phase the guard is anchored to moved forward.
advanced this guard again, under the same narrow, explicitly authorized
mechanical exception, so it now tracks the Phase 13J current-state expectations.
Phase 13I — Governed Local TTS Proof / Audio Artifact Boundary — was locked,
so Phase 13I is now the last locked phase and Phase 13J is the current
implementation candidate. Phase 13J is a frontend/operator-GUI polish phase: it
makes the existing system more cohesive, scannable, and visually credible, and
adds READ-ONLY GUI understanding of the locked Phase 13I governed TTS proof
(status / boundary / artifact-manifest-audit / cost-estimate explanation). The
polish and the read-only TTS understanding are legitimate and NOT forbidden; the
no-overclaim check is re-anchored to Phase 13J and forbids claiming it added
capability it does not: new backend behavior, a new local bridge action, a
generate_tts action, any frontend TTS generation / Generate-audio control, an
audio player, file / directory / URL / credential inputs, a provider selection
that changes runtime behavior, browser durable storage, automatic reload /
polling / WebSocket / EventSource, cloud / distributed / full Local mode, RSS
publishing, a real provider integration, batch generation, or conflating mock
output with real provider audio, retry acceptance with success, or manual reload
with live sync. The guard now protects against a premature Phase 13J lock, a
premature Phase 13 closure, and a premature Phase 13K start; the future-phase
fragment scan now reads `13k` (Phase 13J is the current candidate, and the
dotted `13h.3` / `13i` tokens — which the fragment splitter breaks on `.` — are
covered by the explicit substring list), and the append-only lock-record checks
now also require the Phase 13I lock record. The guardrail concept is unchanged
and coverage is strengthened, not weakened — only the phase the guard is
anchored to moved forward.

Phase 13I note: Phase 13I — Governed Local TTS Proof / Audio Artifact Boundary —
advanced this guard again, under the same narrow, explicitly authorized
mechanical exception, so it now tracks the Phase 13I current-state expectations.
Phase 13H.3 — Manual Static Export Reload / Read-Model Replacement Boundary —
was locked, so Phase 13H.3 is now the last locked phase and Phase 13I is the
current implementation candidate. This is also a forward roadmap re-sequencing:
Phase 13I is now Governed Local TTS Proof, Phase 13J is Operator GUI Polish /
Demo-Local Alignment, and Phase 13K is Demo Walkthrough Refresh; the older note
that 13I would be Operator GUI Polish remains historical and is not rewritten.
Phase 13I is a narrow backend/local-chain proof: an approved fixture driven
through a governance/cost guard and the deterministic mock TTS provider to an
atomic local audio artifact, with a manifest, audit events, and
observability-safe metadata — standing with no credentials and no network. The
governed mock proof is legitimate and NOT forbidden; the no-overclaim check is
re-anchored to Phase 13I and forbids claiming it went further: a real provider
as default / required / called by tests, multiple real providers, a frontend
TTS button or browser-triggered generation, a new local bridge action /
POST /tts / POST /generate / generate_tts / bridge-served audio, network in
tests, batch generation, a full audio-production pipeline, RSS publishing, audio
post-processing or a playback UI, cloud / distributed / full Local mode, browser
durable storage or browser-held credentials, arbitrary text / file / URL
ingestion, or raw text in telemetry. The guard now protects against a premature
Phase 13I lock, a premature Phase 13 closure, and a premature Phase 13J / 13K
start; the future-phase fragment scan now reads `13j | 13k` (Phase 13I is the
current candidate, and the dotted `13h.2` / `13h.3` tokens — which the fragment
splitter breaks on `.` — are covered by the explicit substring list), and the
append-only lock-record checks now also require the Phase 13H.3 lock record. The
guardrail concept is unchanged and coverage is strengthened, not weakened — only
the phase the guard is anchored to moved forward.

Phase 13H.3 note: Phase 13H.3 — Manual Static Export Reload / Read-Model
Replacement Boundary — advanced this guard again, under the same narrow,
explicitly authorized mechanical exception, so it now tracks the Phase 13H.3
current-state expectations. Phase 13H.2 — Frontend Boundary Cleanup / Local
Bridge Component Hardening — was locked, so Phase 13H.2 is now the last locked
phase and Phase 13H.3 is the current implementation candidate. Phase 13H.3
adds exactly one narrow feature: a manual, operator-triggered static export
reload that fetches the committed export, validates it all-or-nothing, and
replaces ONLY the transient in-memory React read model, retaining the previous
snapshot on failure. The manual reload / read-model replacement is therefore
legitimate and is NOT flagged; the no-overclaim check is re-anchored to Phase
13H.3 and instead forbids claiming Phase 13H.3 went further — automatic sync /
polling / live refresh, a new backend or bridge export endpoint, reloading
from the bridge, more action types / a generic action runner, arbitrary
command / SQL / filesystem execution, FULL / real Local mode, Cloud/Distributed
mode, browser durable storage, provider integrations, authentication / user
accounts, conflating acceptance with success, or claiming a reload proves a
retry succeeded. The guard now protects against a premature Phase 13H.3 lock, a
premature Phase 13 closure, and a premature Phase 13I / 13J start; the
future-phase fragment scan still reads `13i | 13j` (the dotted `13h.2` /
`13h.3` tokens — which the fragment splitter breaks on `.` — are covered by the
explicit forbidden-substring lists and line-scan handoff checks that now anchor
on `13i`, alongside line-scan checks that Phase 13H.1 and Phase 13H.2 are
recorded locked). The guardrail concept is unchanged and coverage is
strengthened, not weakened — only the phase the guard is anchored to moved
forward, and the append-only lock-record checks now also require the Phase
13H.2 lock record.

Phase 13H.2 note: Phase 13H.2 — Frontend Boundary Cleanup / Local Bridge
Component Hardening — advanced this guard again, under the same narrow,
explicitly authorized mechanical exception, so it now tracks the Phase 13H.2
current-state expectations. Phase 13H.1 — Controlled Retry Submission from
Frontend — was locked, so Phase 13H.1 is now the last locked phase and Phase
13H.2 is the current implementation candidate. Phase 13H.2 is a BORING
cleanup / hardening round: it corrects stale Phase 13H.1-era comments and
docstrings in the read-only local-bridge surface, clarifies the component
boundary between the GET-only client and the single controlled submission
path that already landed in locked Phase 13H.1, and adds NO new feature. So
nothing new is delivered to overclaim; the no-overclaim check is re-anchored
to Phase 13H.2 and forbids claiming Phase 13H.2 added more action types / a
generic action runner, arbitrary command / SQL / filesystem execution, an
implemented export refresh or reload, read-model replacement / mutation,
FULL / real Local mode, Cloud/Distributed mode, browser durable storage,
provider integrations, authentication / user accounts, or conflating
acceptance with success. The manual static export reload / read-model
replacement remains deferred to the not-started Phase 13H.3. The guard now
protects against a premature Phase 13H.2 lock, a premature Phase 13 closure,
and a premature Phase 13H.3 (or later) start; the future-phase fragment scan
still reads `13i | 13j` (the dotted `13h.2` / `13h.3` tokens — which the
fragment splitter breaks on `.` — are covered by the explicit
forbidden-substring lists and a line-scan handoff check that now anchors on
`13h.3`, alongside a line-scan check that Phase 13H.1 is recorded locked). The
guardrail concept is unchanged and coverage is strengthened, not weakened —
only the phase the guard is anchored to moved forward, and the append-only
lock-record checks now also require the Phase 13H.1 lock record.

Phase 13H.1 note: Phase 13H.1 — Controlled Retry Submission from Frontend —
advanced this guard again, under the same narrow, explicitly authorized
mechanical exception, so it now tracks the Phase 13H.1 current-state
expectations. Phase 13H — Frontend Bridge Observability & Action Lifecycle
Readiness — was locked after its copy-cleanup pass, so Phase 13H is now the last
locked phase and Phase 13H.1 is the current implementation candidate. Phase
13H.1 is the first *frontend mutation boundary*: it legitimately adds exactly
ONE controlled, browser-initiated action — a single POST /actions submitting the
one allowlisted action retry_failed_stage to the loopback bridge (the backend
already accepts it and already answers the loopback-only CORS OPTIONS preflight
from Phase 13G, so no backend change is required), with acceptance explicitly
distinguished from success. So submitting one controlled retry request is no
longer forbidden; the no-overclaim check is re-anchored to Phase 13H.1 and now
forbids only the out-of-scope claims: additional action types / a generic action
runner, arbitrary command / SQL / filesystem execution, an implemented export
refresh, read-model replacement / mutation, FULL / real Local mode,
Cloud/Distributed mode, browser durable storage, provider integrations,
authentication / user accounts, and conflating acceptance with success. The
guard now protects against a premature Phase 13H.1 lock, a premature Phase 13
closure, and a premature Phase 13H.2 (or later) start; the future-phase fragment
scan still reads `13i | 13j` (the dotted `13h.1` / `13h.2` tokens — which the
fragment splitter breaks on `.` — are covered by the explicit
forbidden-substring lists and a line-scan handoff check that now anchors on
`13h.2`). The guardrail concept is unchanged and coverage is strengthened, not
weakened — only the phase the guard is anchored to moved forward, and the
append-only lock-record checks now also require the Phase 13H lock record.

Phase 13H note: Phase 13H — Frontend Bridge Observability & Action Lifecycle
Readiness — advanced this guard again, under the same narrow, explicitly
authorized mechanical exception, so it now tracks the Phase 13H current-state
expectations. Phase 13G and the Phase 13G.1 archive-hygiene cleanup were
locked, so Phase 13G is now the last locked phase and Phase 13H is the current
implementation candidate. Phase 13H is the first *frontend network boundary*:
it legitimately adds read-only observability of the locked Phase 13G local
bridge — loopback-only native-fetch GETs to health / ready / queue /
action-status, a status panel, a queue snapshot panel, and a read-only
action-lifecycle panel that models the future submission UI without enabling
it. So adding read-only frontend bridge observability and action-lifecycle
readiness is no longer forbidden; the no-overclaim check is re-anchored to
Phase 13H and now forbids only the out-of-scope claims: a frontend that
executes / submits / POSTs an action, browser-initiated retry, an export
refresh, read-model replacement / mutation, FULL / real Local mode,
Cloud/Distributed mode, browser durable storage, and provider integrations /
publishing. The guard now protects against a premature Phase 13H lock, a
premature Phase 13 closure, and a premature Phase 13H.1 (or later) start; the
future-phase fragment scan now reads `13i | 13j` (Phase 13H is the current
candidate, and the dotted `13h.1` token — which the fragment splitter breaks
on `.` — is covered by the explicit forbidden-substring list and a line-scan
handoff check). The guardrail concept is unchanged and coverage is
strengthened, not weakened — only the phase the guard is anchored to moved
forward, and the append-only lock-record checks now also require the Phase 13G
lock record.

Phase 13G note: Phase 13G — Local Bridge Contract Synchronization &
Controlled Async Retry — advanced this guard again, under the same narrow,
explicitly authorized mechanical exception, so it now tracks the Phase 13G
current-state expectations. Phase 13F was locked, so Phase 13F is now the
last locked phase and Phase 13G is the current implementation candidate.
Phase 13G is the first *runtime* local-bridge sub-round: it legitimately
implements a minimal, gated, loopback-only standard-library bridge — runtime
DTO validation synchronized to the Phase 13F fixtures, a command-pattern
router, a single-concurrency observable in-memory queue / worker, and exactly
one controlled real action (retry_failed_stage) that runs only against an
explicitly-configured / temporary workspace via the existing governed Phase
10D re-run abstraction. So — unlike the Phase 13F architecture-only check —
implementing a local bridge, a server, an async in-memory queue, a single
worker, runtime DTOs, and controlled retry execution is no longer forbidden;
the no-overclaim check is re-anchored to Phase 13G and now forbids only the
out-of-scope claims: FULL / real Local mode, Cloud/Distributed mode, provider
integrations / storage providers, frontend bridge wiring, browser durable
storage (localStorage / sessionStorage / IndexedDB), a persistent / external
queue (Redis / Celery / cloud queue), a multi-worker / worker-fleet /
autoscaling executor, and execution against a real user workspace. The guard
now protects against a premature Phase 13G lock, a premature Phase 13 closure,
and a premature Phase 13H (or later) start; the future-phase fragment scan now
reads `13h | 13i`. The guardrail concept is unchanged and coverage is
strengthened, not weakened — only the phase the guard is anchored to moved
forward, and the append-only lock-record checks now also require the Phase
13F lock record.

Phase 13F note: Phase 13F — Local Bridge Architecture & Contract
Baseline — advanced this guard again, under the same narrow, explicitly
authorized mechanical exception, so it tracks the Phase 13F
current-state expectations. Phase 13E was locked, so Phase 13E is now
the last locked phase and Phase 13F is the current implementation
candidate. Phase 13F is a documentation-and-static-fixture
architecture-baseline sub-round of Phase 13 — like Phase 13A was for
the operator GUI, Phase 13F is the architectural lock before any
Python local-bridge implementation is allowed. It adds eleven new
architecture / contract docs (local bridge architecture, externalized
state architecture, browser storage policy, local-mode workspace
layout, storage-targets architecture, action-execution boundary,
local-action DTO spec, local-action audit spec, local-mode storage
contract, local-action queue observability, and the Phase 13F
readiness doc), a small set of non-runtime JSON example fixtures
under docs/examples/, and one new Python test
(tests/test_local_mode_contract_examples.py) that validates those
example fixtures are well-formed and contain the required fields
using plain Python (no JSON-schema dependency). Phase 13F implements
NO runtime code: no local bridge, no server, no async queue, no queue
workers, no queue metrics / exporters, no OpenTelemetry
instrumentation, no storage providers, no runtime schema validation,
no router / history, no browser storage, no real Local mode, no
Cloud/Distributed mode, and no mutation execution. The browser
remains non-durable. The guard now protects against a premature
Phase 13F lock, a premature Phase 13 closure, and a premature Phase
13G (or later) start. Because Phase 13F is architecture / static
documentation only, the no-overclaim check is retained and
re-anchored to Phase 13F: the current-state docs must never claim
Phase 13F implements a local bridge, implements / runs a server,
implements an async queue, implements queue workers, implements queue
metrics or exporters, implements OpenTelemetry instrumentation,
implements storage providers, implements real Local mode, implements
Cloud/Distributed mode, executes operator actions / mutations,
implements DTOs in runtime code, implements browser durable storage,
or implements localStorage / sessionStorage / IndexedDB. Because the
"Phase 13F" label contains no period, the "current phase not claimed
locked" check still uses direct substring scanning rather than
fragment splitting, both for symmetry with the Phase 13D.1 / 13D.2 /
13E implementations and so the legitimate "phase 13d.1 is locked",
"phase 13d.2 is locked", and "phase 13e is locked" claims continue to
pass. The future-phase fragment scan now reads `13g | 13h`. The
guardrail concept is unchanged and coverage is strengthened, not
weakened — only the phase the guard is anchored to moved forward, and
the append-only lock-record checks now also require the Phase 13E
lock record.

Phase 13E note (historical — Phase 13E is LOCKED; see the Phase 13F
note above): Phase 13E — Demo-Mode Action Preview / Operator Intent
Boundary — advanced this guard, under the same narrow, explicitly
authorized mechanical exception, so it tracked the Phase 13E
current-state expectations. Phase 13D.2 was locked, so Phase 13D.2 was
the last locked phase and Phase 13E was the current implementation
candidate. Phase 13E is a demo-mode, non-consequential, no-mutation
sub-round of Phase 13 — it added a static Demo-mode Action Preview
system (`frontend/src/data/actionPreviewAdapter.ts` plus
`frontend/src/components/ActionPreviewPanel.tsx` and its CSS Module)
that lets the operator GUI preview what a real operator action would
look like under future Local mode or Cloud/Distributed mode, without
ever executing one. The previews are integrated alongside the existing
visibly-disabled action affordances (`DisabledFutureActionCard` is
unchanged: still a real `<button disabled={true}>` with no `onClick`);
the panel is opened by a separate, clearly-labelled "Preview action
plan" affordance, never by activating the disabled button itself.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DOCS = _REPO_ROOT / "docs"

# Phase 15B — Cloud Boundary Readiness — is LOCKED and is the last LOCKED
# phase. Phase 15A (Cloud Runtime Skeleton) and Phase 14D remain LOCKED (prior
# locked phases). Phase 14E was intentionally bypassed for this transition and
# has NOT started. Phase 15 — Cloud / Distributed Runtime — remains STARTED;
# Phase 15C — Minimal Cloud Demo Deployment / Portfolio Readiness — has now
# STARTED as the current implementation candidate (pending review, NOT locked);
# Phase 15D, Phase 15E, and Phase 15F have NOT started.
_LAST_LOCKED_PHASE = "phase 15b"

# The living current-state documents whose phase claims must stay honest.
_CURRENT_STATE_DOCS: tuple[Path, ...] = (
    _REPO_ROOT / "LLM_DIRECTOR.md",
    _DOCS / "handoff-state.md",
    _DOCS / "roadmap.md",
)

# The append-only history documents that must never lose a lock record.
_APPEND_ONLY_DOCS: tuple[Path, ...] = (
    _DOCS / "canonical-state.md",
    _DOCS / "phase-history.md",
)

# Substrings that would only appear if the current state had drifted: a
# premature Phase 14D lock, a premature Phase 14 closure, or a phantom
# reserved Phase 14E / Phase 15 bundle being claimed as started, current, or
# locked. Matched case-insensitively. (Phase 13 is CLOSED and Phase
# 14A.1/14B.1/14C.1/14C.2/14C.3/14C.4/14C.5.1 are LOCKED now, so "phase 13 is
# closed" / "phase 14c.5.1 is locked" are NOT forbidden. Phase 14 is
# legitimately STARTED and Phase 14D is the legitimate current implementation
# candidate, so "phase 14 has started" / "phase 14d is the current" are NOT
# forbidden — only a premature Phase 14D *lock*, a Phase 14 *closure*, or a
# Phase 14E / Phase 15 *start/lock* is. Those reserved future phases have NOT
# started.)
_FORBIDDEN_FUTURE_CLAIMS: tuple[str, ...] = (
    # Phase 14D is now LOCKED, so a "phase 14d is locked" record is legitimate
    # and is NOT forbidden. Phase 14 has started but must not be claimed
    # closed/complete (a major-phase closure is a separate, not-yet-taken step).
    "phase 14 is closed",
    "phase 14 — closed",
    "phase 14 is complete",
    "phase 14 has closed",
    "phase 14 is locked",
    "phase 14 closure is complete",
    # Phase 14E was intentionally bypassed and has NOT started. Phase 15 — the
    # Cloud / Distributed Runtime arc — has STARTED; Phase 15A and Phase 15B
    # are LOCKED and Phase 15C has now STARTED as the current candidate, so
    # "phase 15 has started", "phase 15a is locked", "phase 15b is locked", and
    # "phase 15c has started" are legitimate; a premature Phase 15 *closure* or
    # *lock* (the parent arc is not closed/locked), a premature Phase 15C
    # *lock*, or any Phase 15D–15F *start/lock* still is forbidden.
    "phase 14e is locked",
    "phase 14e has started",
    "phase 14e is the current",
    "phase 15 is locked",
    "phase 15 is closed",
    "phase 15c is locked",
    "phase 15d has started",
    "phase 15d is locked",
    "phase 15e has started",
    "phase 15e is locked",
    "phase 15f has started",
    "phase 15f is locked",
)

# Substrings that would only appear if a current-state doc OVERCLAIMED what
# Phase 14D delivers. Phase 14D — Cloud / Distributed Architecture Baseline
# from Proven Local Contracts — is a documentation / mapping round: it maps the
# proven LOCAL contracts (request acceptance, the queue port, the worker, the
# ArtifactStore port, the recovery control plane, observation, the read-model)
# to their FUTURE cloud/distributed equivalents on paper; it implements no
# cloud behavior, no broker, no Redis/NATS/SQS/Temporal/Celery, no
# Kubernetes/Terraform, no object/cloud storage, no distributed worker, no
# auth, no provider TTS, no audio, no RSS, and no new dependency. The entries
# below stay positive-claim phrases so honest negated wording ("no external
# broker", "no object storage", "implements no cloud behavior") cannot match.
# (Legacy note: Phase 14C.1 — Local Durable Queue / Worker Shape Proof — IS a
# real implementation round: it legitimately adds a LOCAL durable work queue
# (port + SQLite adapter), a local worker that drains it, and a request path
# that enqueues instead of executing inline. Describing that local queue/worker
# shape is NOT an overclaim and is not flagged here. What IS forbidden is
# claiming Phase 14D (or the project at this point) implemented the capability
# it deliberately does NOT add: a CLOUD or DISTRIBUTED system, a cloud queue /
# external broker / hosted execution / production distributed orchestration,
# provider-backed TTS, frontend audio/TTS generation, audio playback, RSS
# publishing, authentication, cloud deployment, or any Phase 14E / Phase 15
# work.) Entries are positive-claim phrases so honest negated wording ("this is
# not a cloud queue", "no external broker", "Phase 14E is not started") cannot
# match them.
_FORBIDDEN_OVERCLAIM_CLAIMS: tuple[str, ...] = (
    "phase 14d implements cloud mode",
    "phase 14d implements distributed mode",
    "phase 14d implements cloud/distributed mode",
    "phase 14d deploys to the cloud",
    "phase 14d adds cloud deployment",
    "phase 14d implements kubernetes",
    "phase 14d implements terraform",
    "phase 14d implements an external broker",
    "phase 14d implements a cloud queue",
    "phase 14d implements object storage",
    "phase 14d implements an object store",
    "phase 14d implements a distributed worker",
    "phase 14d adds frontend tts generation",
    "phase 14d implements frontend tts generation",
    "phase 14d generates audio",
    "phase 14d adds audio playback",
    "phase 14d adds an audio player",
    "phase 14d integrates a real provider",
    "phase 14d enables the real provider",
    "phase 14d implements a real provider",
    "phase 14d implements provider-backed tts",
    "phase 14d adds a credential input",
    "phase 14d publishes rss",
    "phase 14d implements rss publishing",
    "phase 14d adds authentication",
    "phase 14d implements authentication",
    "phase 14d starts phase 14e",
    "phase 14d begins phase 14e",
    "phase 14d starts phase 15",
    "phase 14d implements phase 15",
    # Phase 14C.1 cloud/distributed overclaims — the queue/worker is LOCAL only.
    # Positive-claim phrasing so honest "this is not a cloud queue" / "no
    # external broker" / "not a distributed system" cannot match.
    "runs as a distributed system",
    "is now a distributed system",
    "implemented a distributed system",
    "implements a distributed system",
    "uses a cloud queue",
    "uses a cloud broker",
    "uses an external broker",
    "supports cloud workers",
    "uses cloud workers",
    "implemented hosted execution",
    "now supports hosted execution",
    "has implemented hosted execution",
    "now has production distributed orchestration",
    "implements cloud execution",
    "runs in the cloud",
    # Section-10 capability-implemented overclaims (all deferred work):
    "cloud mode implemented",
    "cloud deployment added",
    "kubernetes deployment added",
    "provider-backed tts implemented",
    "frontend tts generation implemented",
    "rss publishing implemented",
    "distributed queue implemented",
    "cloud queue implemented",
    "object storage implemented",
    "object-storage adapter implemented",
    "artifact store implemented",
    "external broker implemented",
    "authentication implemented",
    "auth boundary implemented",
    "exactly-once distributed execution",
    "distributed exactly-once execution",
    "s3 adapter implemented",
    "implements the s3 api",
    "uses the s3 api",
    "minio adapter implemented",
    "uses minio",
    "cloud storage implemented",
    "cloud object store implemented",
    "generates signed urls",
    "returns a signed url",
    "serves artifacts publicly",
    "public artifact serving enabled",
    "opentelemetry sdk instrumentation",
    "implements opentelemetry",
    "exposes a prometheus endpoint",
    "prometheus endpoint implemented",
    "grafana dashboard implemented",
    "ships a dashboard",
    "vendor exporters implemented",
    "implements distributed tracing",
    "alerting implemented",
    "slos implemented",
    "cloud telemetry implemented",
    "implements a collector",
    "implements cloud retry",
    "cloud retry orchestration implemented",
    "implements a distributed worker",
    "distributed workers implemented",
    "external broker implemented",
    "implements redis",
    "implements nats",
    "implements sqs",
    "implements temporal",
    "implements celery",
    "dead-letter queue implemented",
    "implements a dead-letter queue",
    "automatic retries implemented",
    "implements automatic retries",
    "exponential backoff implemented",
    "retry scheduler implemented",
    "implements a retry scheduler",
    "implements cloud leases",
    "implements distributed locks",
    "implements a cloud queue",
    "cloud queue implemented",
    # Honest-framing overclaims preserved from prior rounds:
    "mock output is real provider audio",
    "mock is real provider audio",
    "the mock output is real audio",
    "retry acceptance equals success",
    "retry accepted equals success",
    "acceptance is success",
    "acceptance means success",
    "reload is live sync",
    "reload is a live sync",
    "manual reload is live sync",
)

# Words that mark a phase as currently active. Used by the negation-aware
# sentence scan below.
_CURRENT_STATUS_CUES: tuple[str, ...] = (
    "locked",
    "in progress",
    "underway",
    "current phase",
    "current subphase",
    "is the current",
    "begun",
    "is complete",
    "completed",
)

# Cues that mark a sentence as explicitly *not* claiming current status — a
# negation, or language that frames the phase as future / planned. If any of
# these appears in a fragment, the fragment cannot be a current-status claim.
_NEGATION_CUES: tuple[str, ...] = (
    "not ",
    "n't",
    "never",
    "without",
    "no ",
    "yet to",
    "have not",
    "has not",
    "do not",
    "does not",
    "did not",
    "remains",
    "future",
    "later",
    "intended",
    "planned",
    "plan",
    "decompos",
    "upcoming",
    "next",
)

# Fragments split on sentence and clause punctuation, on commas, on table-cell
# pipes, and on em / en dashes — these documents use dashes and commas to
# separate clauses ("Phase 11B — Title — is locked, and is the source for
# Phase 11C"), so a claim about one phase must not be smeared into a claim
# about an adjacent one.
_FRAGMENT_SPLIT = re.compile(r"[.!?;,\n|\u2014\u2013]")


def _read(path: Path) -> str:
    """Return a document's text, asserting it exists and is non-empty."""
    assert path.is_file(), f"expected state doc is missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert text.strip(), f"state doc is unexpectedly empty: {path}"
    return text


def _fragments_mentioning(text: str, label_pattern: str) -> list[str]:
    """Return lowercased fragments of *text* that mention *label_pattern*.

    The text is split into clause-sized fragments on sentence and clause
    punctuation and on table-cell pipes, so a claim about one phase is not
    smeared across a claim about another.
    """
    label = re.compile(label_pattern, re.IGNORECASE)
    found: list[str] = []
    for fragment in _FRAGMENT_SPLIT.split(text):
        if label.search(fragment):
            found.append(fragment.lower())
    return found


def _claims_current_status(fragment: str) -> bool:
    """True if *fragment* asserts active status with no negating language."""
    if any(cue in fragment for cue in _NEGATION_CUES):
        return False
    return any(cue in fragment for cue in _CURRENT_STATUS_CUES)


@pytest.mark.parametrize("doc", _CURRENT_STATE_DOCS, ids=lambda p: p.name)
class TestStatePhaseDiscipline:
    """The living state docs must describe the current phase honestly."""

    def test_doc_records_phase_14d_locked(self, doc: Path) -> None:
        """Each current-state doc records Phase 14D as locked (the last locked
        phase).

        Phase 14D — Cloud / Distributed Architecture Baseline from Proven Local
        Contracts — was the implementation candidate and is now LOCKED. Scans
        line-by-line for the literal '14d' token co-located with 'locked' (the
        legitimate lock record), mirroring the handoff-state lock-record checks.
        """
        lowered = _read(doc).lower()
        lines_with = [ln for ln in lowered.splitlines() if "14d" in ln]
        assert lines_with, f"{doc.name} does not mention Phase 14D"
        assert any("locked" in ln for ln in lines_with), (
            f"{doc.name} no longer records Phase 14D as locked"
        )

    def test_last_locked_phase_is_recorded(self, doc: Path) -> None:
        """Phase 15B is now named as the last locked phase."""
        assert _LAST_LOCKED_PHASE in _read(doc).lower(), (
            f"{doc.name} no longer mentions {_LAST_LOCKED_PHASE.title()}"
        )

    def test_doc_records_phase_15a_locked(self, doc: Path) -> None:
        """Each current-state doc records Phase 15A as locked.

        Phase 15A — Cloud Runtime Skeleton — was the implementation candidate
        and is now LOCKED. Scans line-by-line for the literal '15a' token
        co-located with 'locked' (the legitimate lock record), mirroring the
        Phase 14D lock-record check above.
        """
        lowered = _read(doc).lower()
        lines_with = [ln for ln in lowered.splitlines() if "15a" in ln]
        assert lines_with, f"{doc.name} does not mention Phase 15A"
        assert any("locked" in ln for ln in lines_with), (
            f"{doc.name} no longer records Phase 15A as locked"
        )

    def test_doc_records_phase_15b_locked(self, doc: Path) -> None:
        """Each current-state doc records Phase 15B as locked (the last locked
        phase).

        Phase 15B — Cloud Boundary Readiness — was the implementation candidate
        and is now LOCKED. Scans line-by-line for the literal '15b' token
        co-located with 'locked', mirroring the Phase 15A lock-record check
        above.
        """
        lowered = _read(doc).lower()
        lines_with = [ln for ln in lowered.splitlines() if "15b" in ln]
        assert lines_with, f"{doc.name} does not mention Phase 15B"
        assert any("locked" in ln for ln in lines_with), (
            f"{doc.name} no longer records Phase 15B as locked"
        )

    def test_no_forbidden_future_phase_claim(self, doc: Path) -> None:
        """No contiguous phrase claims a premature Phase 14 closure or an
        active/locked Phase 14E / Phase 15. (Phase 14D is legitimately LOCKED,
        so a Phase 14D lock record is allowed.)"""
        lowered = _read(doc).lower()
        for claim in _FORBIDDEN_FUTURE_CLAIMS:
            assert claim not in lowered, (
                f"{doc.name} contains a forbidden future-phase claim: {claim!r}"
            )

    def test_no_overclaim(self, doc: Path) -> None:
        """No contiguous phrase overclaims what Phase 14D delivers. Phase 14D is
        an as-built mapping / documentation round: it maps the proven LOCAL
        contracts to their FUTURE cloud/distributed equivalents on paper,
        records Phase 14C.5.1 as locked, and recommends (does not start) a
        Phase 15 cloud-runtime decomposition. It adds NO runtime capability and
        changes no source, frontend, or dependency. The mapping documentation
        itself is legitimate and is NOT flagged here. What is forbidden is
        describing Phase 14D (or the project at this point) as having
        implemented capability it has not: a cloud/distributed system, an
        external broker or cloud queue, object/cloud storage, a distributed
        worker, frontend TTS generation, audio playback, a real provider
        integration, RSS publishing, authentication, cloud deployment, or any
        Phase 14E / Phase 15 implementation."""
        lowered = _read(doc).lower()
        for claim in _FORBIDDEN_OVERCLAIM_CLAIMS:
            assert claim not in lowered, (
                f"{doc.name} contains a forbidden overclaim about Phase 13L: "
                f"{claim!r}"
            )

    def test_future_phases_not_claimed_current(self, doc: Path) -> None:
        """No fragment claims the reserved Phase 14E / Phase 15B–15E arcs are
        current or locked.

        Phase 14 is STARTED, Phase 14D is LOCKED, Phase 15 has STARTED with
        Phase 15A and Phase 15B LOCKED, and Phase 15C has now STARTED as the
        current implementation candidate — so bare ``phase 15``, ``phase 15a``,
        ``phase 15b``, and ``phase 15c`` are not scanned here as future (a
        premature Phase 15 closure/lock of the parent arc and a premature Phase
        15C lock are guarded by the explicit forbidden-substring list instead).
        Phase 14E (intentionally bypassed) and Phase 15D through Phase 15F are
        the reserved future arcs that have NOT started, so a fragment
        mentioning any of them must never assert active/locked status without a
        negation/future cue.
        """
        text = _read(doc)
        for label in (
            r"phase\s+14e",
            r"phase\s+15d",
            r"phase\s+15e",
            r"phase\s+15f",
        ):
            for fragment in _fragments_mentioning(text, label):
                assert not _claims_current_status(fragment), (
                    f"{doc.name} appears to claim a future phase is active: "
                    f"{fragment.strip()!r}"
                )


class TestHandoffStateCurrentStatus:
    """Targeted checks on the authoritative current-status document."""

    def test_handoff_state_records_phase_10_closed(self) -> None:
        """handoff-state.md still records Phase 10 as closed."""
        lowered = _read(_DOCS / "handoff-state.md").lower()
        assert "phase 10" in lowered and "closed" in lowered, (
            "handoff-state.md no longer records Phase 10 as closed"
        )

    def test_handoff_state_records_phase_11_closed(self) -> None:
        """handoff-state.md records Phase 11 as closed (closed in Phase 12A)."""
        lowered = _read(_DOCS / "handoff-state.md").lower()
        assert "phase 11" in lowered and "closed" in lowered, (
            "handoff-state.md no longer records Phase 11 as closed"
        )

    def test_handoff_state_records_phase_12_closed(self) -> None:
        """handoff-state.md records Phase 12 as closed (closed in Phase 13A)."""
        lowered = _read(_DOCS / "handoff-state.md").lower()
        assert "phase 12" in lowered, "handoff-state.md never mentions Phase 12"
        assert "closed" in lowered, (
            "handoff-state.md no longer records Phase 12 as closed"
        )

    def test_handoff_state_records_phase_13b_locked(self) -> None:
        """handoff-state.md records Phase 13B as locked (locked in Phase 13C)."""
        lowered = _read(_DOCS / "handoff-state.md").lower()
        assert "phase 13b" in lowered, (
            "handoff-state.md never mentions Phase 13B"
        )
        assert "locked" in lowered, (
            "handoff-state.md no longer records Phase 13B as locked"
        )

    def test_handoff_state_records_phase_13c_locked(self) -> None:
        """handoff-state.md records Phase 13C as locked (locked in Phase 13D)."""
        lowered = _read(_DOCS / "handoff-state.md").lower()
        assert "phase 13c" in lowered, (
            "handoff-state.md never mentions Phase 13C"
        )
        assert "locked" in lowered, (
            "handoff-state.md no longer records Phase 13C as locked"
        )

    def test_handoff_state_records_phase_13d_locked(self) -> None:
        """handoff-state.md records Phase 13D as locked (locked in Phase 13D.1)."""
        lowered = _read(_DOCS / "handoff-state.md").lower()
        assert "phase 13d" in lowered, (
            "handoff-state.md never mentions Phase 13D"
        )
        assert "locked" in lowered, (
            "handoff-state.md no longer records Phase 13D as locked"
        )

    def test_handoff_state_records_phase_13d1_locked(self) -> None:
        """handoff-state.md records Phase 13D.1 as locked (locked in Phase 13D.2)."""
        lowered = _read(_DOCS / "handoff-state.md").lower()
        assert "phase 13d.1" in lowered, (
            "handoff-state.md never mentions Phase 13D.1"
        )
        assert "locked" in lowered, (
            "handoff-state.md no longer records Phase 13D.1 as locked"
        )

    def test_handoff_state_records_phase_13d2_locked(self) -> None:
        """handoff-state.md records Phase 13D.2 as locked (locked in Phase 13E)."""
        lowered = _read(_DOCS / "handoff-state.md").lower()
        assert "phase 13d.2" in lowered, (
            "handoff-state.md never mentions Phase 13D.2"
        )
        assert "locked" in lowered, (
            "handoff-state.md no longer records Phase 13D.2 as locked"
        )

    def test_handoff_state_records_phase_13e_locked(self) -> None:
        """handoff-state.md records Phase 13E as locked (locked in Phase 13F)."""
        lowered = _read(_DOCS / "handoff-state.md").lower()
        assert "phase 13e" in lowered, (
            "handoff-state.md never mentions Phase 13E"
        )
        assert "locked" in lowered, (
            "handoff-state.md no longer records Phase 13E as locked"
        )

    def test_handoff_state_records_phase_13f_locked(self) -> None:
        """handoff-state.md records Phase 13F as locked (locked in Phase 13G)."""
        lowered = _read(_DOCS / "handoff-state.md").lower()
        assert "phase 13f" in lowered, (
            "handoff-state.md never mentions Phase 13F"
        )
        assert "locked" in lowered, (
            "handoff-state.md no longer records Phase 13F as locked"
        )

    def test_handoff_state_records_phase_13g_locked(self) -> None:
        """handoff-state.md records Phase 13G (and 13G.1) as locked (in 13H)."""
        lowered = _read(_DOCS / "handoff-state.md").lower()
        assert "phase 13g" in lowered, (
            "handoff-state.md never mentions Phase 13G"
        )
        assert "locked" in lowered, (
            "handoff-state.md no longer records Phase 13G as locked"
        )

    def test_handoff_state_records_phase_13h_locked(self) -> None:
        """handoff-state.md records Phase 13H as locked (locked in Phase 13H.1)."""
        lowered = _read(_DOCS / "handoff-state.md").lower()
        assert "phase 13h" in lowered, (
            "handoff-state.md never mentions Phase 13H"
        )
        assert "locked" in lowered, (
            "handoff-state.md no longer records Phase 13H as locked"
        )

    def test_handoff_state_records_phase_13h1_locked(self) -> None:
        """handoff-state.md records Phase 13H.1 as locked.

        Phase 13H.1 — Controlled Retry Submission from Frontend — is a locked
        historical record. The fragment splitter breaks on '.', so this scans
        line-by-line for the literal '13h.1' token co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "13h.1" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 13H.1"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 13H.1 as locked"
        )

    def test_handoff_state_records_phase_13h2_locked(self) -> None:
        """handoff-state.md records Phase 13H.2 as locked.

        Phase 13H.2 — Frontend Boundary Cleanup / Local Bridge Component
        Hardening — is a locked historical record. The fragment splitter breaks
        on '.', so this scans line-by-line for the literal '13h.2' token
        co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "13h.2" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 13H.2"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 13H.2 as locked"
        )

    def test_handoff_state_records_phase_13h3_locked(self) -> None:
        """handoff-state.md records Phase 13H.3 as locked (the last locked phase).

        Phase 13H.3 — Manual Static Export Reload / Read-Model Replacement
        Boundary — was locked before Phase 13I (this governed TTS proof round)
        began, so it must now appear as a locked record. The fragment splitter
        breaks on '.', so this scans line-by-line for the literal '13h.3' token
        co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "13h.3" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 13H.3"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 13H.3 as locked"
        )

    def test_handoff_state_records_phase_13i_locked(self) -> None:
        """handoff-state.md records Phase 13I as locked (the last locked phase).

        Phase 13I — Governed Local TTS Proof / Audio Artifact Boundary — was
        locked before Phase 13J (this operator-GUI polish round) began, so it
        must now appear as a locked record. The fragment splitter breaks on '.',
        so this scans line-by-line for the literal '13i' token co-located with
        'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "13i" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 13I"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 13I as locked"
        )

    def test_handoff_state_records_phase_13j_locked(self) -> None:
        """handoff-state.md records Phase 13J as locked (the last locked phase).

        Phase 13J — Operator GUI Polish / Demo-Local Alignment — was locked
        before Phase 13K (this demo-walkthrough-refresh round) began, so it must
        now appear as a locked record. The fragment splitter breaks on '.', so
        this scans line-by-line for the literal '13j' token co-located with
        'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "13j" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 13J"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 13J as locked"
        )

    def test_handoff_state_records_phase_13k_locked(self) -> None:
        """handoff-state.md records Phase 13K as locked (the last locked phase).

        Phase 13K — Demo Walkthrough Refresh / Governed Local Chain Story Path —
        was locked before Phase 13L (this Phase 13 closure round) began, so it
        must now appear as a locked record. The fragment splitter breaks on '.',
        so this scans line-by-line for the literal '13k' token co-located with
        'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "13k" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 13K"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 13K as locked"
        )

    def test_handoff_state_records_phase_13l_locked(self) -> None:
        """handoff-state.md records Phase 13L as locked (the last locked phase).

        Phase 13L — Phase 13 Closure / Demo-Local Completion Lock — was locked
        before Phase 14A.1 (this local-live proof-loop round) began, so it must
        now appear as a locked record. The fragment splitter breaks on '.', so
        this scans line-by-line for the literal '13l' token co-located with
        'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "13l" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 13L"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 13L as locked"
        )

    def test_handoff_state_records_phase_13_closed(self) -> None:
        """handoff-state.md records Phase 13 as formally closed.

        Re-anchored for Phase 14A.1: Phase 13L locked and, with it, Phase 13 was
        formally CLOSED. handoff-state.md must now record that closure
        positively. This scans line-by-line for a 'phase 13' line co-located
        with a 'closed' token.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "phase 13" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 13"
        assert any("closed" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 13 as closed"
        )

    def test_handoff_state_records_phase_14_started(self) -> None:
        """handoff-state.md records Phase 14 as started.

        Phase 14 — Live System / Cloud-Distributed — is now STARTED, with Phase
        14A.1 as the current implementation candidate. handoff-state.md must
        name Phase 14 and record it as started.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "phase 14" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 14"
        assert any("started" in ln for ln in lines_with), (
            "handoff-state.md does not record Phase 14 as started"
        )

    def test_handoff_state_records_phase_14a1_locked(self) -> None:
        """handoff-state.md records Phase 14A.1 as locked (the last locked phase).

        Phase 14A.1 — Local Live Proof Loop Before Cloud — was locked before
        Phase 14B.1 (this hardening round) began, so it must now appear as a
        locked record. This scans line-by-line for the literal '14a.1' token
        co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "14a.1" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 14A.1"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 14A.1 as locked"
        )

    def test_handoff_state_records_phase_14b1_locked(self) -> None:
        """handoff-state.md records Phase 14B.1 as locked (the last locked phase).

        Phase 14B.1 — Live Proof Loop Hardening / Operator Trust — was locked
        before Phase 14C.1 (this queue/worker round) began, so it must now appear
        as a locked record. This scans line-by-line for the literal '14b.1'
        token co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "14b.1" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 14B.1"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 14B.1 as locked"
        )

    def test_handoff_state_records_phase_14c1_locked(self) -> None:
        """handoff-state.md records Phase 14C.1 as locked (the last locked phase).

        Phase 14C.1 — Local Durable Queue / Worker Shape Proof — was LOCKED
        before Phase 14C.2 (this contracts-as-built round) began, so it must now
        appear as a locked record. This scans line-by-line for the literal
        '14c.1' token co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "14c.1" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 14C.1"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 14C.1 as locked"
        )

    def test_handoff_state_records_phase_14c2_locked(self) -> None:
        """handoff-state.md records Phase 14C.2 as locked (the last locked phase).

        Phase 14C.2 — Contracts-as-Built / Cloud-Distributed Seam Baseline — was
        LOCKED before Phase 14C.3 (this object-storage round) began, so it must
        now appear as a locked record. Scans line-by-line for the literal
        '14c.2' token co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "14c.2" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 14C.2"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 14C.2 as locked"
        )

    def test_handoff_state_records_phase_14c3_locked(self) -> None:
        """handoff-state.md records Phase 14C.3 as locked (the last locked phase).

        Phase 14C.3 — Object Storage Boundary / Artifact Store Adapter — was
        LOCKED before Phase 14C.4 (this observability round) began, so it must
        now appear as a locked record. Scans line-by-line for the literal
        '14c.3' token co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "14c.3" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 14C.3"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 14C.3 as locked"
        )

    def test_handoff_state_records_phase_14c4_locked(self) -> None:
        """handoff-state.md records Phase 14C.4 as locked (the last locked phase).

        Phase 14C.4 — Minimal Observability Boundary for Queue/Worker — was
        LOCKED before Phase 14C.5.1 (this durable recovery control-plane round)
        began, so it must now appear as a locked record. Scans line-by-line for
        the literal '14c.4' token co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "14c.4" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 14C.4"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 14C.4 as locked"
        )

    def test_handoff_state_records_phase_14c5_1_locked(self) -> None:
        """handoff-state.md records Phase 14C.5.1 as locked (the last locked phase).

        Phase 14C.5.1 — Durable Recovery Control Plane Boundary — was the
        implementation candidate and is now LOCKED, before Phase 14D (this
        as-built cloud/distributed mapping round) began, so it must now appear
        as a locked record. Scans line-by-line for the literal '14c.5.1' token
        co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "14c.5.1" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 14C.5.1"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 14C.5.1 as locked"
        )

    def test_handoff_state_records_phase_14d_locked(self) -> None:
        """handoff-state.md records Phase 14D as locked (the last locked phase).

        Phase 14D — Cloud / Distributed Architecture Baseline from Proven Local
        Contracts — was the implementation candidate and is now LOCKED, so it
        must now appear as a locked record. Scans line-by-line for the literal
        '14d' token co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "14d" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 14D"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 14D as locked"
        )

    def test_handoff_state_records_phase_15a_locked(self) -> None:
        """handoff-state.md records Phase 15A as locked.

        Phase 15A — Cloud Runtime Skeleton — was the implementation candidate
        and is now LOCKED, so it must appear as a locked record. Scans
        line-by-line for the literal '15a' token co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "15a" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 15A"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 15A as locked"
        )

    def test_handoff_state_records_phase_15b_locked(self) -> None:
        """handoff-state.md records Phase 15B as locked (the last locked phase).

        Phase 15B — Cloud Boundary Readiness — was the implementation candidate
        and is now LOCKED, so it must appear as a locked record. Scans
        line-by-line for the literal '15b' token co-located with 'locked'.
        """
        lowered = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in lowered.splitlines() if "15b" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 15B"
        assert any("locked" in ln for ln in lines_with), (
            "handoff-state.md no longer records Phase 15B as locked"
        )

    def test_handoff_state_frames_phase_14e_not_started(self) -> None:
        """handoff-state.md frames the reserved Phase 14E+ arc as not started.

        Phase 14E+ — the reserved future local-release-candidate / cloud arc —
        has not started. Every handoff-state line that mentions Phase 14E must
        carry a negation / future / planned cue (so none asserts Phase 14E is
        active or locked). Phase 14D is the legitimate current candidate and
        Phase 15 is a recommended (not started) future arc; those are framed in
        prose and guarded by the forbidden-future literal list.
        """
        text = _read(_DOCS / "handoff-state.md").lower()
        lines_with = [ln for ln in text.splitlines() if "phase 14e" in ln]
        assert lines_with, "handoff-state.md never mentions Phase 14E"
        assert all(
            any(cue in ln for cue in _NEGATION_CUES)
            for ln in lines_with
        ), "handoff-state.md has a Phase 14E line without a not-started/future cue"


class TestAppendOnlyHistory:
    """The append-only history docs must retain every historical lock record."""

    def test_canonical_state_retains_phase_10_closure_record(self) -> None:
        """canonical-state.md still records the Phase 10 closure."""
        lowered = _read(_DOCS / "canonical-state.md").lower()
        assert "phase 10g" in lowered, (
            "canonical-state.md lost the Phase 10G record"
        )
        assert "phase 10" in lowered and "closed" in lowered, (
            "canonical-state.md lost the Phase 10 closure record"
        )

    @pytest.mark.parametrize(
        "marker",
        [
            "post-phase-10 historical state reconciliation",
            "phase 11a",
            "phase 11b",
            "phase 11c",
            "phase 11d",
            "phase 12a",
            "phase 12b",
            "phase 12c",
            "phase 12d",
            "phase 13a",
            "phase 13b",
            "phase 13c",
            "phase 13d",
            "phase 13d.1",
            "phase 13d.2",
            "phase 13e",
            "phase 13f",
            "phase 13g",
            "phase 13h",
            "phase 13h.1",
            "phase 13h.2",
            "phase 13h.3",
            "phase 13i",
            "phase 13j",
            "phase 13k",
            "phase 13l",
            "phase 14a.1",
            "phase 14b.1",
            "phase 14c.1",
            "phase 14c.2",
            "phase 14c.3",
            "phase 14c.4",
            "phase 14c.5.1",
        ],
    )
    def test_canonical_state_retains_earlier_lock_records(
        self, marker: str
    ) -> None:
        """Each earlier locked work item is still recorded in canonical-state."""
        lowered = _read(_DOCS / "canonical-state.md").lower()
        assert marker in lowered, (
            f"canonical-state.md lost the {marker!r} record"
        )

    @pytest.mark.parametrize(
        "marker",
        [
            "phase 10g",
            "post-phase-10 historical state reconciliation",
            "phase 11a",
            "phase 11b",
            "phase 11c",
            "phase 11d",
            "phase 12a",
            "phase 12b",
            "phase 12c",
            "phase 12d",
            "phase 13a",
            "phase 13b",
            "phase 13c",
            "phase 13d",
            "phase 13d.1",
            "phase 13d.2",
            "phase 13e",
            "phase 13f",
            "phase 13g",
            "phase 13h",
            "phase 13h.1",
            "phase 13h.2",
            "phase 13h.3",
            "phase 13i",
            "phase 13j",
            "phase 13k",
            "phase 13l",
            "phase 14a.1",
            "phase 14b.1",
            "phase 14c.1",
            "phase 14c.2",
            "phase 14c.3",
            "phase 14c.4",
            "phase 14c.5.1",
        ],
    )
    def test_phase_history_retains_historical_records(
        self, marker: str
    ) -> None:
        """phase-history.md still records every earlier locked phase / item."""
        lowered = _read(_DOCS / "phase-history.md").lower()
        assert marker in lowered, (
            f"phase-history.md lost the {marker!r} record"
        )

    @pytest.mark.parametrize("doc", _APPEND_ONLY_DOCS, ids=lambda p: p.name)
    def test_append_only_doc_records_phase_14d(self, doc: Path) -> None:
        """The append-only history records the locked Phase 14D round."""
        assert "phase 14d" in _read(doc).lower(), (
            f"{doc.name} has no Phase 14D entry"
        )

    @pytest.mark.parametrize("doc", _APPEND_ONLY_DOCS, ids=lambda p: p.name)
    def test_append_only_doc_records_phase_15a(self, doc: Path) -> None:
        """The append-only history records the now-locked Phase 15A round.

        Phase 15A — Cloud Runtime Skeleton — was the implementation candidate
        and is now LOCKED. The append-only docs must carry a literal
        'phase 15a' marker so the round is durably recorded, mirroring the
        Phase 14D retention check above.
        """
        assert "phase 15a" in _read(doc).lower(), (
            f"{doc.name} has no Phase 15A entry"
        )

    @pytest.mark.parametrize("doc", _APPEND_ONLY_DOCS, ids=lambda p: p.name)
    def test_append_only_doc_records_phase_15b(self, doc: Path) -> None:
        """The append-only history records the now-locked Phase 15B round.

        Phase 15B — Cloud Boundary Readiness — was the implementation candidate
        and is now LOCKED. The append-only docs must carry a literal
        'phase 15b' marker so the round is durably recorded, mirroring the
        Phase 15A retention check above.
        """
        assert "phase 15b" in _read(doc).lower(), (
            f"{doc.name} has no Phase 15B entry"
        )

    @pytest.mark.parametrize("doc", _APPEND_ONLY_DOCS, ids=lambda p: p.name)
    def test_append_only_doc_records_phase_15c(self, doc: Path) -> None:
        """The append-only history records the Phase 15C candidate round.

        Phase 15C — Minimal Cloud Demo Deployment / Portfolio Readiness — is
        the current implementation candidate (pending review, NOT locked). The
        append-only docs must carry a literal 'phase 15c' marker so the round
        is durably recorded even before it is locked, mirroring the Phase 15B
        retention check above.
        """
        assert "phase 15c" in _read(doc).lower(), (
            f"{doc.name} has no Phase 15C entry"
        )
