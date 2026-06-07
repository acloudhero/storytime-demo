# StoryTime — Frontend / Backend Contract

The decoupled contract between the future StoryTime frontend (the Phase 13
portfolio website and operator GUI) and the existing backend / local artifact
model. It exists so the frontend can be built, evolved, and hosted
independently of how StoryTime's backend is run.

**Phase 13A defines this contract; it does not implement it.** No API, no
adapter, no server, and no frontend code is created in Phase 13A. This document
is the specification a later subphase implements against. See
`docs/phase13-portfolio-website-architecture.md` and `docs/phase13-roadmap.md`.

## Contract principle: backend owns truth, frontend owns understanding

The single governing principle of the Phase 13 frontend is:

> **Backend owns truth. Frontend owns understanding.**

What this means concretely:

- **The backend owns truth.** SQLite, the on-disk artifact envelopes, and the
  durable Trust Envelope artifact remain the source of truth, exactly as the
  locked Architecture Baseline section 24 and section 25 require. The frontend
  never becomes a second source of truth, never holds authoritative state, and
  never persists run data of its own.
- **The frontend owns understanding.** The frontend's job is to make the
  backend's truth legible - to a reviewer and to the operator. It is a *view*.
  It reads a documented contract and presents it clearly; it adds
  comprehension, not authority.
- **The contract is the seam.** The frontend depends only on the documented
  read models and (later) action models in this document. It must never depend
  on the SQLite schema, on CLI output text, on internal Python types, on
  artifact-envelope internals, or on file layout. Those are backend internals
  and may change; the contract is the stable interface.

Because the frontend depends only on the contract, the same frontend works
whether the contract is served from a static JSON file, a local API, the local
files directly, or a future cloud API. The backend can be refactored freely as
long as the contract holds; the frontend can be rebuilt freely as long as it
consumes the contract.

## Read-only data model categories

These are the read models the frontend consumes. Phase 13A specifies them as
*categories and intent* - the shape of the information, not a frozen JSON
schema. A later subphase (13C) defines the concrete serialization. Every field
in every read model must be derivable from data StoryTime already records;
the contract introduces no new product data.

All read models obey the section 25 display rules: no raw story or narration
text, no transcripts, no secrets, no raw free-text error messages or raw
`blocked_reason` strings, no embedded telemetry payloads. Structured codes and
bounded summaries only.

### Project summary

A small, mostly static description of the StoryTime project itself: what it is,
the current phase state, the headline counts (how many runs exist, how many
need attention), and the high-level health of the system. This is the data
behind the dashboard header and the website home page. It is portfolio-facing
and run-data-light.

### Pipeline runs

The list of pipeline runs. For each run: a stable run identifier, a
human-readable label or source title, the run status, the governance decision
summary, the created/updated timestamps, and a flag for whether the run needs
operator attention. This is a bounded, paginated list - it must not assume a
small number of runs.

### Run detail

Everything about a single run that the run-detail view needs: the run
identifier, status, the ordered list of its stages with each stage's state,
the governance decision and its bounded context summary, the failure summary
if the run failed (structured `error_kind` code only, never the raw message),
the references to its artifacts, and the references to its observability
evidence. This is the richest read model and the backbone of the operator GUI.

### Stage timeline

The ordered sequence of a run's stages - ingest, synthesize, assemble, publish,
with the approval gates woven in - each with its state, its start/end
timestamps where known, and its relationship to the next stage. This is a
projection over the same data as run detail, shaped specifically for a timeline
visualization.

### Episode artifacts

For a run that produced output: what it produced. Audio artifact references
(path or download reference, duration, size), the published-episode metadata,
and the feed reference. No raw audio bytes are part of the contract - the model
carries references, and the backend or adapter decides whether a reference is
downloadable. No raw narration text.

### Governance decisions

The Trust Envelope decision for a run: the stable decision enum
(`APPROVED` / `REJECTED` / `BLOCKED` / `NEEDS_REVIEW`), the bounded
review-context summary (subject to the section 25 character cap), the source
category, and the standing "record of a human decision, not legal advice or
certification of copyright safety" disclaimer text. No raw `blocked_reason`
free text; no legal or compliance overclaiming vocabulary.

### Failure queue

The runs that need operator attention - failed, blocked by governance, marked
needs-review, or awaiting an approval decision - each with the structured
reason it needs attention and a pointer to which run-detail view, command, or
artifact to inspect next. This is the same semantic projection the existing
`storytime queue` command produces, shaped as a read model.

### Observability evidence

For a run: references and links into the existing observability surfaces - the
trace identifier or trace link, references to the relevant dashboards, the
correlation key (`pipeline_run_id`). Links and references only; the contract
never embeds telemetry data, never embeds dashboard JSON, and never puts
secrets in URLs.

### Validation / evidence status

A portfolio-facing read model: the state of the project's own evidence - which
phases are locked, the latest validation-gate results, the claim-to-evidence
index summary. This feeds the website's evidence/review-packet section. It is
about the *project*, not about a run.

## Future action categories

The operator GUI is read-only first. These action categories are part of the
contract's design so the read models and the UI reserve space for them, but
**no action is enabled before Phase 13E**, and every mutating action obeys the
locked Architecture Baseline section 25 mutation gate and governance rules.

- **Copy command** - surface the exact CLI command for an operation so the
  operator can run it themselves. This is the safest "action": it mutates
  nothing; it just hands the operator a command. It is the bridge between a
  read-only GUI and the existing CLI.
- **Open artifact / report** - open or download a run's artifact, or open the
  existing generated static HTML operator report. Read-only navigation, not a
  mutation.
- **Retry eligible run** - request a re-run of a failed, retry-eligible run.
  This is a true mutation; it maps to the existing governed `storytime rerun`
  semantics and is gated on Trust Envelope eligibility exactly as the CLI is.
- **Mark review decision** - record an operator approval / rejection / review
  decision for a run awaiting one. A true mutation; it maps to the existing
  governed approval semantics.
- **Regenerate report** - regenerate the static operator report. A bounded,
  idempotent action over existing state.

The first three of these (copy command, open artifact/report) are read-only or
near-read-only and could arrive earliest; the genuine mutations (retry, mark
review decision, regenerate report) are the explicitly gated Phase 13E work.

## Explicitly disabled in Phase 13A

Phase 13A defines the contract on paper. It explicitly does **not** deliver:

- **Mutation behavior** - no action in this document is implemented or wired;
  the operator GUI's first implemented subphases are read-only.
- **A backend API implementation** - no operator-API server, no endpoints, no
  request handlers. The contract is a specification, not running code.
- **Authentication** - no login, no accounts, no tokens, no session model.
  StoryTime is single-local-operator; authentication is out of scope for the
  whole of Phase 13 unless a future phase explicitly amends this.
- **Cloud deployment** - no hosting, no cloud API, no remote backend. The
  cloud adapter is a *future-compatibility design*, not a Phase 13 deliverable.
- **GUI runtime code** - no React/Vue/component/route code, no `package.json`,
  no bundler config, no HTML/CSS/JS application files.

## Data source options

The contract is deliberately source-agnostic. The same read models can be
delivered by any of the following adapters; the frontend cannot tell which is
in use, and choosing between them is a deployment decision, not a frontend
change.

- **Static JSON export.** A snapshot of the read models written to JSON files
  by an exporter (a later subphase, 13C). The frontend reads those files
  directly. This makes the portfolio website hostable as pure static content
  with no backend at all, and lets a reviewer see realistic data without
  running StoryTime. It is the default for public presentation and for the
  demo-data mode.
- **Local API adapter.** A small local read-only API over the running local
  StoryTime backend. The frontend calls it; it returns the contract read
  models. This is the mode for an operator working with live local runs.
- **File-backed adapter.** An adapter that reads the local SQLite projections
  and the on-disk artifact directory directly and assembles the read models,
  with no API process at all. This suits a local operator who does not want to
  run a separate API.
- **Future cloud API.** If StoryTime ever gains a hosted backend, a cloud API
  implements the same contract. No frontend change is required; only a new
  adapter and a backend-connection-mode setting.

A "backend mode" setting (demo-static / local-runtime / future-cloud) selects
the adapter. The screens, read models, and operator workflows are identical
across modes; only the adapter and the connection setting differ.

## Compatibility with future distributed / cloud-native evolution

Although StoryTime is and remains local-first, the contract is designed so a
future distributed or cloud-native evolution does not require rewriting the
frontend:

- The contract is **transport-agnostic.** Read models are described as data
  shapes, not as a specific HTTP API; a static file, a local API, and a cloud
  API are all valid carriers.
- The contract is **stateless from the frontend's side.** The frontend holds
  no authoritative state and assumes nothing about where the backend runs, so
  a multi-host or hosted backend changes only the adapter.
- The contract **carries identifiers, not internals.** Runs, stages, and
  artifacts are referenced by stable identifiers; the frontend never depends
  on file paths or schema layout, so the backend can move from a single local
  SQLite file to a distributed store without breaking the contract.
- The action model is **designed for governance at the backend.** Every future
  mutation maps to an existing governed backend operation; a cloud backend
  would enforce the same Trust Envelope and section 25 rules. The frontend
  never becomes the place where governance is decided.
- Authentication, multi-tenancy, and cloud deployment remain **out of scope and
  unauthorized**; if they are ever wanted they require their own phase and,
  where they touch the Architecture Baseline, their own amendment. This
  document does not authorize them - it only ensures the contract would not
  have to be thrown away if that future work were ever approved.

The result: the Phase 13 frontend can be built today against local-first,
static, demo data, and still be the same frontend if StoryTime ever grows a
cloud backend. That is the decoupling the contract principle exists to
guarantee.
