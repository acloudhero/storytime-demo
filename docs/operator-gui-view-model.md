# StoryTime — Operator GUI View Model

The first operator GUI view model: what each operator-facing view shows, what
it reads, and what it must not do — defined before any implementation. It is
the operator-facing companion to `docs/portfolio-website-content-model.md`
(which covers the public portfolio side of the same Phase 13 property).

**Phase 13A defines this view model; it does not build the GUI.** No views, no
components, no HTML, and no frontend code are created in Phase 13A. See
`docs/phase13-portfolio-website-architecture.md`,
`docs/frontend-backend-contract.md`, and `docs/phase13-roadmap.md`.

## Scope and principles

The operator GUI is the tactile, visual, browser-based way for the operator to
*see and understand* StoryTime runs. The view model below obeys these rules:

- **Read-only first.** Every view in the first implemented operator subphases
  (13D) is read-only. Action affordances may be visibly present but are
  disabled until the explicitly gated Phase 13E. See "Disabled / future
  actions".
- **Reads the contract, not the backend.** Every view consumes the read models
  in `docs/frontend-backend-contract.md`; no view depends on the SQLite schema,
  CLI output text, Python internals, or file layout.
- **Backend owns truth.** The GUI shows the backend's truth and never becomes a
  second source of truth. SQLite, the artifact envelopes, and the durable Trust
  Envelope remain authoritative (Architecture Baseline section 24 / section 25).
- **Section 25 display discipline.** No view shows raw story or narration text,
  transcripts, secrets, raw free-text error messages, or raw `blocked_reason`
  strings; governance is shown with the stable decision enum and the standing
  "record of a human decision, not legal advice" disclaimer, with no legal or
  compliance overclaiming.
- **Operator understanding, separate from backend mechanics.** The views
  present what a run *did* and what *needs attention*; they do not expose the
  internal mechanics of how the backend computed it.

## Dashboard view

**Shows.** An at-a-glance summary for the operator: how many runs exist, how
many need attention, the most recent runs and their status, and a clear "what
should I look at next" signal. It is the operator GUI's landing view.

**Reads.** The project-summary and failure-queue read models; a bounded slice
of the pipeline-runs read model.

**Must not.** Expose any mutation control; show raw content or secrets;
overwhelm the operator - it is a summary, with links into the detailed views.

## Pipeline runs view

**Shows.** The list of all pipeline runs: for each, the run label / source
title, status, governance decision summary, last-updated time, and a
needs-attention flag. Filterable by status; bounded and paginated so a large
run history does not break it.

**Reads.** The pipeline-runs read model.

**Must not.** Assume a small number of runs; show raw content; offer a
mutation control. Selecting a run navigates to the run detail view.

## Pipeline run detail view

**Shows.** The single most important operator view - one run made legible: the
run identifier and status; the ordered stages with each stage's state; the
governance decision and its bounded context summary; the failure summary if the
run failed (the structured `error_kind` code and operator-safe guidance, never
the raw error message); references to the run's artifacts; references to its
observability evidence; and, for the operator, a plain statement of what the
run's current state means and what (read-only) next step is available. This is
where the system stops being an abstraction and becomes something the operator
can follow.

**Reads.** The run-detail read model, plus the governance-decisions,
episode-artifacts, and observability-evidence read models for that run.

**Must not.** Show raw narration/story text or transcripts; show secrets or raw
`blocked_reason`; offer an enabled mutation control before Phase 13E;
overclaim governance.

## Stage timeline view

**Shows.** The ingest -> synthesize -> assemble -> publish sequence for one run,
with the operator approval gates woven in, presented as a timeline: each
stage's state, its start/end where known, and the gate outcomes. It makes the
*shape* of a run visible - where it progressed, where it paused at a gate,
where it stopped.

**Reads.** The stage-timeline read model.

**Must not.** Invent timing data the backend does not record; show raw content;
offer a mutation control. It is a projection of run detail, shaped for a
timeline.

## Episode artifacts view

**Shows.** For a run that produced output: what it produced - the audio
artifact reference (duration, size, a download/open reference), the
published-episode metadata, and the feed reference.

**Reads.** The episode-artifacts read model.

**Must not.** Embed raw audio bytes in the contract or the view; show raw
narration text; expose secrets. Opening or downloading an artifact is
read-only navigation, not a mutation.

## Failure queue view

**Shows.** The runs that need operator attention - failed, blocked by
governance, marked needs-review, or awaiting an approval decision - each with
the structured reason and a pointer to the run-detail view (and, read-only, the
exact CLI command) to act on it. It is the GUI equivalent of the existing
`storytime queue` command.

**Reads.** The failure-queue read model.

**Must not.** Offer an enabled retry / approve control before Phase 13E (the
queue surfaces *what* needs attention and *which command* to run; acting from
the GUI is gated); show raw error text; reorder or hide runs in a way that
loses an attention item.

## Governance / review view

**Shows.** The Trust Envelope decisions: per run, the stable decision enum
(`APPROVED` / `REJECTED` / `BLOCKED` / `NEEDS_REVIEW`), the bounded
review-context summary (within the section 25 character cap), the source
category, and the standing "record of a human decision, not legal advice or
certification of copyright safety" disclaimer.

**Reads.** The governance-decisions read model.

**Must not.** Use any legal or compliance overclaiming vocabulary; present
governance as content moderation; show the raw `blocked_reason` free text;
imply StoryTime performed a legal determination.

## Observability evidence view

**Shows.** For a run: references and links into the existing observability
surfaces - the trace identifier / trace link, references to the relevant
dashboards, and the `pipeline_run_id` correlation key. It connects a run to its
telemetry without re-implementing tracing or dashboards in the GUI.

**Reads.** The observability-evidence read model.

**Must not.** Embed telemetry payloads or dashboard JSON; put secrets in URLs;
claim a production observability deployment. Links and references only.

## Settings / config view

**Shows.** The backend-connection mode (demo-static / local-runtime /
future-cloud) and a read-only display of the relevant configuration the
operator should be able to see. It is where the operator understands *which
backend the GUI is talking to*.

**Reads.** The project-summary read model and the active adapter / connection
setting.

**Must not.** Expose secrets or credentials; allow editing backend behaviour;
offer a cloud-deployment control (cloud is a future-compatibility design, not a
Phase 13 capability).

## Disabled / future actions

The operator GUI is read-only first. The following actions are part of the
contract's design and the views reserve space for them, but they are
**disabled until Phase 13E**, and when enabled they obey the locked
Architecture Baseline section 25 mutation gate and Trust Envelope governance:

- **Copy command** - hand the operator the exact CLI command (mutates nothing;
  could arrive earliest).
- **Open artifact / report** - open a run's artifact or the static operator
  report (read-only navigation).
- **Retry eligible run** - request a governed re-run of a failed,
  retry-eligible run.
- **Mark review decision** - record an operator approval / rejection / review
  decision.
- **Regenerate report** - regenerate the static operator report.

Until Phase 13E, these affordances render as visibly disabled, so the operator
can see what will be possible without any mutation risk. No action bypasses
governance, and every genuine mutation maps to an existing governed backend
operation.

## Empty / error / loading states

Every view must define three non-happy states, because an operator GUI that
only handles full, correct data is not trustworthy:

- **Loading.** A clear, non-blocking loading indication while a read model is
  fetched. Data should appear progressively where a view has multiple
  read models rather than blocking the whole view.
- **Empty.** A plain, honest empty state - "no runs yet", "nothing needs
  attention", "this run produced no artifacts" - never a blank screen and never
  a fabricated placeholder run.
- **Error.** A clear error state when a read model cannot be loaded (adapter
  unavailable, malformed export, missing run): say what failed and what the
  operator can do, without exposing secrets, stack traces, or backend
  internals. An error in one read model must not blank the whole view if other
  read models loaded.

## Accessibility / readability requirements

The operator GUI is the human interaction layer; it must be usable, not just
present:

- **Readable by default.** Sufficient text contrast, legible default type
  sizes, and a layout that does not require horizontal scrolling on a normal
  screen.
- **Keyboard navigable.** Every view and every (eventual) control reachable and
  operable by keyboard, with a visible focus indicator.
- **Semantic and screen-reader friendly.** Meaningful headings and landmarks,
  meaningful labels on controls, and status conveyed by text and not by colour
  alone.
- **Status legible without colour.** Run status, governance decision, and
  attention flags carry a text label, not only a colour.
- **Honest, plain language.** Operator-facing copy is plain and non-hype;
  governance copy carries the section 25 disclaimer; nothing overclaims.
- **Calm, scannable density.** The dashboard and list views are scannable at a
  glance; the run-detail view can be dense but stays organized into clear
  sections.

These requirements are part of the Phase 13D acceptance criteria; a view that
renders data but fails them is not done.
