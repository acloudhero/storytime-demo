# StoryTime — Known Limitations

An honest account of what StoryTime does **not** do, and where its boundaries
are. Naming the limitations is deliberate: it shows scoping discipline, and it
keeps the project's claims trustworthy. Where a limitation is a considered
architecture decision rather than an unfinished edge, this document says so.

This document focuses on the Phase 10 operator-experience layer and the
project's overall posture. For the existing engineering non-goals see
`docs/portfolio-notes.md` Section 3; for governance limitations see
`docs/architecture-baseline.md` Section 24; for the deferred roadmap items see
`docs/roadmap.md` ("Deferred / not authorized").

---

## Product and deployment scope

### StoryTime is local-first, not a production SaaS dashboard

StoryTime runs on one machine, from the command line. It is not a hosted
product, has no users, no SLA, and no operational scale story. This is a
**charter decision**: local-first keeps the trust surface small (nothing leaves
the machine) and makes every scenario reproducible by a reviewer. The operator
report is a generated static HTML file, not a served dashboard.

### Phase 10 does not add multi-user authentication

There are no accounts, no roles, no login, and no per-user state. StoryTime is
designed around a **single local human operator**. Multi-user management is out
of scope by design — adding it would change the product into something the
charter explicitly does not target.

### Phase 10 does not add cloud deployment

Nothing in Phase 10 deploys to the cloud, and there is no image registry,
Kubernetes, or Terraform. The optional containerized blue/green path (Phase 7)
is local, single-host, and demo-grade. Cloud deployment is a deferred,
unauthorized roadmap item — it would require its own phase and, where it
touches the architecture baseline, an explicit amendment.

## Operator-experience layer

### Phase 10 does not add live polling or a real-time UI

The operator report is a *static snapshot*. It does not auto-refresh, poll, or
stream updates. To see new state, an operator regenerates the report with
`storytime report generate`. This is a **deliberate Phase 10A constraint**: a
static, regenerable artifact is inspectable, diffable, and offline-safe, with
no server and no websocket surface.

### The static report is read-only

The operator report contains no form, no button, and no control that changes
state. It shows what each run did and what governance recorded; it does not
act. If the report and the SQLite database ever disagree, the database is
authoritative — the report is a projection, not a second source of truth.

### Browser-based mutation controls are intentionally absent

There is no "retry" button, no "approve" button, and no "delete" control in the
report or any browser surface. Every state change goes through an explicit CLI
command. The single operator mutation surface is `storytime rerun`, a
command-line tool with an explicit eligibility check, a `--dry-run` preview, a
stable decision code, and an audit event. Keeping mutation in the CLI — and out
of the browser — is a deliberate architecture choice that keeps the report
honestly read-only and the mutation surface small and auditable.

### Re-run resumes from the failed stage only

`storytime rerun` re-runs a failed run from the stage it failed at. Re-running
from an arbitrary earlier stage — which would require invalidating
already-completed stages — is intentionally out of scope. The optional
`--from-stage` argument therefore only accepts the run's failed stage, as an
explicit operator confirmation. `rerun` also does not execute the pipeline
itself: it resets state and writes an audit record, and the operator runs
`storytime run --resume` explicitly.

### The failure queue is not a broker-backed queue

`storytime queue` is a read-only *semantic query* over existing SQLite state.
It is conceptually a dead-letter / review queue, but there is no message
broker, no background worker, no new queue storage, no new run lifecycle state,
and no `pop` / `dequeue` / `claim` / `ack` behaviour. It changes nothing. This
keeps the operator triage surface simple and dependency-free.

## Content, audio, and TTS

### Generated audio is not committed to the repository

The pipeline produces MP3 audio at the assemble stage, but generated audio is
runtime output under `runs/` and `feed/` — git-ignored and never committed.
The repository stays source- and text-focused. A reviewer regenerates audio by
running the pipeline locally.

### Demo fixtures are small local examples, not a content library

The `demo/` directory holds four original CC0 seed texts and six golden-path
fixture definitions. They exist to make a handful of scenarios reproducible —
they are not a catalogue of content, and the project is not a content library
or a publishing platform.

### TTS is mock-grade

Real high-quality text-to-speech is stubbed with a mock adapter. Audio quality
is not a current concern and is not measured. StoryTime is not a commercial
text-to-speech platform.

## Governance

### Governance checks are project controls, not legal advice

The Trust Envelope transcribes the **human operator's recorded licensing
decision** for a source. StoryTime performs no legal determination, does not
clear rights, and does not certify copyright safety. Every governance display
carries a standing "record of a human decision, not legal advice" disclaimer.
The governance layer is a fail-closed *project control*, not a
rights-clearance engine.

### Governance is source authorization, not content moderation

A `BLOCKED` decision is an *authorization* outcome — is this source allowed? —
not a judgement about the acceptability of the content's viewpoint. StoryTime
is not a content-moderation system.

### The needs-review demo scenario uses the operator approval gate

A governance Trust Envelope decision of `NEEDS_REVIEW` is a distinct state that
the normal local manifest path does not reach: the closed manifest schema
restricts the source licence to recognised values that map to an `APPROVED`
envelope. The demo's needs-review scenario therefore uses the **existing
operator text approval-gate semantics** — a run paused awaiting a human
decision — rather than inventing an unsupported way to manufacture a
`NEEDS_REVIEW` governance decision. The fixture definition
`demo/fixtures/04-needs-review-approval-gate.yaml` records this limitation
explicitly. This is honesty about a real boundary, not a gap.

## Observability

### No active alerting

There is no Alertmanager, no paging, and no on-call integration. An operator
*reads* the report, the queue, and (optionally) the dashboards; nothing pages.

### Observability is an optional view, and Docker-dependent

The OpenTelemetry traces/metrics stack (Collector, Prometheus, Loki, Jaeger,
Grafana) is optional and runs under Docker. With the default `noop` telemetry
adapter no telemetry is emitted and the pipeline behaves identically. The six
quality gates and the whole test suite are Docker-free. The architecture is
compatible with observability-native operations; it does not claim
instrumentation for any specific commercial observability vendor.

## Process and history

### Phase 10G is documentation and closure, not feature work

Phase 10G — the phase that produced this document — adds portfolio and demo
documentation and prepares Phase 10 for closure. It adds no product feature, no
UI, no server, no JavaScript, and no backend behaviour change. It is
documentation-first by design.

### Phase 10 is not closed until review

At the time this document was written, Phase 10G is an implementation
candidate, pending independent review. Phase 10 is not marked fully closed
until that review completes and the user locks it. See `docs/handoff-state.md`
for the authoritative current status.
