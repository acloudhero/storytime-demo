# StoryTime — Observability & Governance Talking Points

The technical story of StoryTime told in interview / portfolio language,
oriented toward a **Solutions Engineer** or observability-focused discussion.
Each talking point is short, quotable, and backed by something concrete in the
repository.

This document is honest about scope: it claims **observability-native
thinking** and an architecture **compatible with** OpenTelemetry-centred
operations. It does **not** claim instrumentation for, or integration with,
any specific commercial observability vendor — none is implemented, and saying
so would be overclaiming.

Companion documents: `docs/portfolio-narrative.md` (the full narrative),
`docs/portfolio-notes.md` (the existing engineering summary),
`docs/telemetry-map.md` and `docs/slo-sli.md` (the telemetry detail).

---

## 1. Observability-native, held to an honesty standard

> "StoryTime emits real OpenTelemetry traces and metrics — one `pipeline.run`
> span per run with child stage spans, and eight purposeful, low-cardinality
> metrics. And it enforces *metric honesty*: a test fails the build if a
> dashboard charts a metric the code does not actually emit."

The point for an interviewer: observability here is not bolted on for a demo.
It is a design property with an automated guardrail. The project has no
dashboard it cannot back with real data, and that absence is documented rather
than hidden. Backed by: `docs/telemetry-map.md`, `tests/test_dashboards.py`.

## 2. Telemetry is a view, not the source of truth

> "Persistence to SQLite happens *before* telemetry emission. With the default
> `noop` adapter, no telemetry is emitted and the pipeline behaves identically.
> Observability can fail without the pipeline failing."

This is the invariant that makes the system trustworthy: the durable record
(SQLite `event_log` plus hashed artifact envelopes plus the Trust Envelope) is
authoritative, and OpenTelemetry is a confined *view* over it — all
OpenTelemetry imports live in one adapter module, enforced by an import-linter
contract and an AST-scanning test.

## 3. Operator visibility — from machine telemetry to human triage

> "Phase 10 extends observability from *machine* telemetry to *operator*
> observability. The same source of truth is projected into a static HTML
> operator report and a command-line failure queue — so a human can answer
> 'what happened?' and 'what needs me?' without a dashboard server."

The report and the queue are the human-facing analogue of traces and metrics:
deterministic projections of authoritative state, designed for inspection.
Backed by: `docs/operator-report.md`, `docs/operator-queue.md`.

## 4. Failure triage as a first-class surface

> "`storytime queue` answers one question deterministically: which runs need
> an operator, why, and what to look at next. It is a read-only semantic query
> over SQLite — a dead-letter / review queue in concept, with no broker, no
> worker, and no hidden state."

Failure triage is not an afterthought reached through log-grepping; it is a
named surface with a stable contract. For each queued run it shows the
attention reason, a structured failure code, and the next command to run.

## 5. Auditability — an append-only record of every transition

> "Every meaningful state transition lands in an append-only `event_log`. A run
> that failed, was re-run, and then completed keeps its whole journey — the
> failure event, the re-run-requested event, and the recovered completion — on
> one record. Nothing is rewritten."

Auditability is demonstrated end-to-end by the demo's completed-after-rerun
scenario. The same discipline governs the project's own history: locked
decisions and round records are append-only.

## 6. Local-first reliability

> "The pipeline and the entire test suite run offline, on one machine, with no
> cloud account. The only outbound-network path that exists at all — telemetry
> export from the Collector — is disabled by default and never required."

Local-first is a reliability and trust story, not just a convenience: there is
no hosted dependency to fail, and the trust surface is the local filesystem.
It also makes the work *reproducible* — a reviewer sees exactly what the author
sees.

## 7. Governance and content safety — honest by construction

> "StoryTime has a real governance layer: a per-run Trust Envelope that records
> the *human operator's* licensing decision, and a fail-closed gate that
> hard-blocks before TTS and before RSS publishing unless the envelope is
> `APPROVED`. It performs no legal determination and is not a rights-clearance
> engine."

The honesty rules are the talking point: governance is **source
authorization**, not viewpoint moderation; every governance display carries a
"record of a human decision, not legal advice" disclaimer; and a static
scanner runs in the test suite to fail the build if legal-overclaiming
vocabulary appears outside the documents that legitimately define it. Backed
by: `docs/architecture-baseline.md` Section 24,
`tests/test_legal_hallucination_gate.py`.

## 8. Safe redaction discipline

> "The operator surfaces show structured fields only — a failure *code*, never
> the free-text error message; a governance decision *enum*, never the raw
> blocked-reason text. The report's field allowlist keeps raw story text,
> transcripts, and secrets out of generated output entirely."

Redaction is enforced, not assumed: the `review_context_summary` 500-character
cap is tested, the `rerun` output keys are a fixed allowlist, and the report's
no-raw-content rule has its own tests.

## 9. Bounded mutation via the rerun command

> "StoryTime has exactly one operator mutation surface: `storytime rerun`. It
> proves a re-run is safe before acting, performs one bounded mutation —
> resetting a failed run to the resumable state — writes one audit event, and
> hands control back to the operator. No retry loop, no scheduler, no daemon."

For an SRE / Solutions Engineer audience this is the strongest point: change is
deliberate, minimal, governed, and audited. `--dry-run` is a true preview;
ineligible runs are rejected with a stable decision code and a non-zero exit;
a governance block can never be bypassed by a re-run. Backed by:
`docs/operator-rerun.md`.

## 10. The static report as inspectable evidence

> "The operator report is a generated, static, read-only HTML artifact — no
> JavaScript, no server, no external assets. It opens offline, straight from
> the filesystem, and it is a faithful projection of the source of truth."

Because it is static and regenerable, the report is *evidence*: it can be
diffed, archived, and inspected without trusting a running service. It is a
control-free observability surface — it shows, it never acts.

## 11. Demo fixtures as reproducible scenarios

> "Six golden-path fixtures make the interesting scenarios reproducible — the
> happy path, a retryable technical failure, a governance block, an
> approval-gate pause, a re-run request, and a completed-after-rerun recovery.
> They drive the real pipeline; they do not fake a success path."

Reproducible scenarios turn "trust me" into "run it yourself" — the same
property good observability gives a production system, applied to a portfolio
demo. Backed by: `demo/fixtures/`, `docs/demo.md`.

## 12. Process discipline — phased delivery with independent review

> "StoryTime is built under a multi-model review process with an explicit Phase
> Closure Protocol: implementation output is reviewed, critiqued, cleaned up,
> and only then locked by explicit approval. The project carries its own
> portable, append-only memory so a cold session can resume safely."

The process is itself an observability story: the State Preservation Bundle is
instrumentation for the *project*, and a synchronization gate keeps it
consistent. Backed by: `LLM_DIRECTOR.md`, `docs/phase-closure-protocol.md`.

---

## How to frame the whole thing in 30 seconds

> "StoryTime is a local-first content-to-audio pipeline built to be observable
> and operable, honestly. SQLite is the source of truth; OpenTelemetry is a
> view over it. The operator experience is three layers — a static read-only
> report to *see*, a deterministic queue to *triage*, and one governed, audited
> command to *act* — wrapped around a fail-closed governance gate that records
> human decisions without claiming to be a legal authority. Every claim is
> backed by a test or a doc, and the architecture is compatible with
> observability-native operations without pretending to integrate a vendor it
> doesn't."

## What not to claim

To keep this discussion honest, do **not** say StoryTime:

- integrates with, or is instrumented for, any named commercial observability
  vendor — it emits standard OpenTelemetry to a local Collector only;
- has production alerting, paging, or an error-budget policy — it does not;
- is deployed, has users, or has operational scale — it is a local,
  single-operator project;
- performs legal determinations or clears rights — governance records a human
  decision and is not a legal authority.

Stating the boundaries is part of the credibility, not a weakness in it.
