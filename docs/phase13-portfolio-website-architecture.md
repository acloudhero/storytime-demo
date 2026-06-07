# StoryTime — Phase 13 Portfolio Website / Operator GUI Architecture

The architecture baseline for Phase 13. It defines what the StoryTime portfolio
website and operator GUI should become by the end of Phase 13, who it is for,
how its public-presentation role and its operator role coexist, and how the
frontend stays decoupled from whichever backend it runs against.

**Phase 13A is documentation only.** This document, and the four companion
Phase 13A documents, design the frontend; they do **not** implement it. No
frontend application, scaffold, framework choice, or runtime code is created in
Phase 13A. See "What Phase 13A does not implement" below and
`docs/frontend-backend-contract.md`, `docs/phase13-roadmap.md`,
`docs/portfolio-website-content-model.md`, and
`docs/operator-gui-view-model.md`.

The roadmap-preserved Phase 13 vision (`docs/GUI_vision.md` and the Phase 13
note in `docs/roadmap.md`, both created during the Phase 12B.2 cleanup)
recorded the user's requirement and an early sketch. Phase 13A turns that
preserved vision into an architecture; where this document and the earlier
sketch differ, this document is the Phase 13A architecture of record.

## Phase 13 purpose

Phase 13 builds StoryTime's first graphical interface. It is the project's
first GUI track — every prior phase delivered CLI, library, configuration, or
documentation surfaces, plus the generated static HTML operator report. The
end result of Phase 13 is a **portfolio website that is also the first operator
GUI layer**.

Phase 13 exists for two reasons that point in the same direction:

1. **StoryTime needs to be legible to outside reviewers without running it.** A
   hiring manager, a Solutions-Engineer interviewer, or an observability
   reviewer should be able to understand what StoryTime is, how it is built,
   and why its observability and governance choices matter — by reading a
   website, not by cloning a repository and standing up a backend.

2. **StoryTime needs to be legible to its own operator.** The operator's
   primary way of interacting with software is a graphical interface; a purely
   CLI-and-documents system is hard to fully visualize and internalize. The GUI
   is the missing human interaction layer for *understanding* and, in later
   subphases, *operating* the system.

The GUI is therefore **not cosmetic**. It is not a coat of paint over the CLI.
It is the human interaction layer through which both an outside reviewer and
the operator come to understand the system. A reviewer who reads the website
should leave understanding the pipeline, the observability story, and the
governance posture; an operator who opens the GUI should be able to *see* a
pipeline run the way they currently can only reconstruct it from CLI output and
the static report.

Phase 13 is decomposed into subphases (13A-13G) so the architecture is settled
before any code is written and so frontend implementation cannot leak into a
planning round. See `docs/phase13-roadmap.md`.

## End-state portfolio website vision

By the end of Phase 13, the portfolio website should be a small, local-first
web property that does the following for an outside reviewer:

- **Explains what StoryTime is** in plain language - a local-first,
  observability-native content-to-audio pipeline - and is honest that it is a
  portfolio-grade engineering artifact, not a deployed product.
- **Presents the architecture** - the five-stage pipeline, SQLite plus on-disk
  artifact envelopes as the source of truth, OpenTelemetry as an optional view,
  the mechanically enforced import boundaries, and the multi-model RoundTable
  / Phase Closure Protocol process.
- **Shows the observability story** - what telemetry StoryTime emits, why the
  Collector-owned fan-out model matters, and what the dashboards and SLO/SLI
  narrative demonstrate - without claiming a production deployment or a
  commercial-vendor integration.
- **Shows the governance and safety story** - the Trust Envelope, the
  fail-closed gate, the source-authorization-not-viewpoint stance, and the
  honest "this is not legal rights-clearance" boundary.
- **Provides a hiring-manager / reviewer path** - tiered review routes
  (a fast skim, a technical read, a deep architecture read) so a reviewer can
  spend five minutes or an hour and get a coherent picture either way.
- **Makes the project legible without requiring a backend** - a reviewer can
  understand StoryTime from the website alone, then optionally clone and run.

The website is content-first. It draws its material from the Phase 0-12
evidence the repository already contains (see
`docs/portfolio-website-content-model.md`); Phase 13 packages that evidence as
a website, it does not invent new claims.

## Operator GUI vision

By the end of Phase 13, the same web property should also be the first
**operator GUI layer**: a tactile, visual, browser-based way for the operator
to see and understand StoryTime runs.

The operator GUI should let the operator:

- See **pipeline runs** - a list of runs with their status and a sense of what
  needs attention.
- See a **pipeline run in detail** - the run's stages, where it is, where it
  failed if it failed, the governance decision, and links to its evidence.
- See the **stage timeline** of a run - ingest -> synthesize -> assemble ->
  publish with the approval gates, made visible as a sequence rather than
  reconstructed from log lines.
- See **episode artifacts** - what a completed run produced (audio, feed
  references) without exposing raw content or secrets.
- See the **failure / review queue** - the runs that are failed, blocked by
  governance, awaiting approval, or marked needs-review, and why.
- See **governance decisions** - the Trust Envelope decision for a run,
  presented with the same honesty rules the static report already obeys.
- See **observability evidence** - links and references into the existing
  observability surfaces (traces, dashboards) rather than re-implementing them.

The operator GUI is **read-only first**. Phase 13's early subphases give the
operator visibility and understanding with no mutation risk. Controlled
operator *actions* (retry, re-run, record a review decision) are deferred to a
later, explicitly gated subphase (Phase 13E) and, when they arrive, obey the
locked Architecture Baseline section 25 mutation rules. The operator GUI never
becomes a dangerous control panel before the data contract and the safety
boundaries are mature.

The most important operator screen is the **pipeline run detail** view: that
is where the system stops being an abstraction and becomes something the
operator can see, follow stage by stage, and reason about.

## Audiences and review paths

The website and operator GUI serve four audiences. The architecture must let
all four coexist without the website confusing one audience with another's
material.

| Audience | What they want | Primary surface |
|----------|----------------|-----------------|
| **Operator / user** | A tactile way to see and (later) operate runs | The operator GUI views |
| **Hiring manager** | A fast, honest sense of what the project demonstrates and whether to look closer | The public homepage and a 5-minute review path |
| **Technical reviewer** | The architecture, the boundaries, the evidence behind the claims | The architecture and evidence sections, a 15-minute path |
| **Observability reviewer** | The telemetry model, the governance posture, the SLO/SLI honesty | The observability and governance sections |

The two roles of the property - **public portfolio presentation** and
**operator GUI** - are kept legibly separate:

- The **public portfolio** sections are content the project presents about
  itself: narrative, architecture explanation, observability story, governance
  story, evidence index, timeline, limitations, roadmap. They are safe to show
  anyone and do not depend on any live run data.
- The **operator GUI** views show *run data* - runs, stages, failures,
  governance decisions read from the backend or a demo data set. They are the
  operator's working surface.

A reviewer should never mistake an operator working view for a portfolio
claim, and the operator should never have to read marketing copy to find a
failing run. The two roles share a visual shell and navigation but are
distinct sections, clearly labelled. The portfolio sections are the default
landing experience; the operator GUI is a clearly separate area of the same
site.

## Website information architecture

The public portfolio side of the property is organized into these top-level
sections. The detailed content for each is specified in
`docs/portfolio-website-content-model.md`.

- **Home** - a concise narrative of what StoryTime is and why it exists, with
  the tiered reviewer paths as the primary call to action.
- **Architecture** - the pipeline, the source-of-truth model, the import
  boundaries, and the RoundTable / Phase Closure Protocol process.
- **Observability** - what telemetry StoryTime emits, the Collector-owned
  fan-out model, the dashboards, and the SLO/SLI narrative.
- **Governance & safety** - the Trust Envelope, the fail-closed gate, and the
  honest non-goals (no legal rights-clearance, no content moderation).
- **Demo walkthrough** - what a run looks like end to end, suitable for a
  reviewer who will not run the backend.
- **Evidence / review packet** - the claim-to-evidence index and the
  Solutions-Engineer competency matrix, so any claim can be checked.
- **Project timeline** - the phase history, told as a story of disciplined
  iteration.
- **Technical depth** - deeper material for a reviewer who wants the full
  architecture.
- **Limitations** - honest boundaries and non-goals, stated plainly.
- **Roadmap** - what is intentionally not built yet, including the Phase 13
  GUI track itself.
- **Reviewer path / call to action** - how to read the repository, run the
  demo, and contact the author.

## Operator information architecture

The operator GUI side of the property is organized into these views. The
detailed view model for each - including empty, loading, and error states and
accessibility requirements - is specified in
`docs/operator-gui-view-model.md`.

- **Dashboard** - an at-a-glance summary: recent runs, what needs attention,
  overall system state.
- **Pipeline runs** - the list of all runs, filterable by status.
- **Pipeline run detail** - the single most important view: one run, its
  stages, its governance decision, its evidence links, and its current state.
- **Stage timeline** - the ingest -> synthesize -> assemble -> publish sequence
  with approval gates, shown as a timeline for one run.
- **Episode artifacts** - what a completed run produced, with no raw content
  or secrets exposed.
- **Failure queue** - the runs needing operator attention and why.
- **Governance / review** - the Trust Envelope decisions, shown with the
  section 25 honesty rules.
- **Observability evidence** - links and references into traces and
  dashboards.
- **Settings / config** - backend-connection mode (demo data, local, future
  cloud) and read-only display of relevant configuration.

All operator views are read-only in the early Phase 13 subphases. The view
model reserves space for future operator actions but disables them until
Phase 13E.

## Local-first and future-cloud compatibility

StoryTime is local-first. The website and operator GUI must not break that, and
must not assume a cloud deployment, while still being compatible with one if it
ever happens.

The architectural rule is the contract principle developed in
`docs/frontend-backend-contract.md`:

> **Backend owns truth. Frontend owns understanding.**

The frontend must not know, and must not care, whether StoryTime is running
local-first, in local containers, or behind a future cloud API. It knows only
that it reads a documented, stable contract - a set of read models - and
presents them. The contract can be served by:

- a **static JSON export** of run data (so the website works with no backend
  at all - the default for public hosting and for a reviewer);
- a **local API adapter** over the running local backend;
- a **file-backed adapter** that reads the local SQLite projections and
  artifact directory directly;
- a **future cloud API**, if one is ever built.

The same screens, the same data shapes, and the same view models work against
every one of these. Only the adapter changes. This is what keeps the website
honest about local-first (it can ship as static content) and simultaneously
ready for a future distributed evolution (the contract is the seam a cloud API
would implement).

Phase 13A defines the contract and the adapter strategy; it does not implement
any adapter. The first frontend subphases (13B/13C) build against a static /
demo-data adapter precisely so the frontend can exist before any backend API
does, and so the backend can evolve without breaking the frontend.

## What Phase 13A does not implement

Phase 13A is an architecture baseline. To keep the planning round from drifting
into implementation, Phase 13A explicitly does **not**:

- create a frontend application, or any `frontend/`, `web/`, `app/`, or
  `apps/frontend/` directory;
- create `package.json`, `vite.config.*`, or any Node / npm project file;
- write React, Vue, or any other component, route, or browser-runtime code;
- write HTML, CSS, or JavaScript application files, or add runtime assets;
- choose or install a frontend framework, bundler, or toolchain;
- implement a backend API, an operator-API server, or any data adapter;
- add authentication, multi-user accounts, or any cloud deployment;
- change `src/`, `pyproject.toml`, `uv.lock`, dependencies, the pipeline,
  `storytime rerun`, Trust Envelope enforcement, the CLI, telemetry, or Docker
  behaviour;
- generate screenshots, audio, video, or other binary presentation assets.

Phase 13A adds documentation only. The first frontend scaffold is Phase 13B's
work, and only after Phase 13A has been reviewed and locked. See
`docs/phase13-roadmap.md` for the subphase boundaries.

## Phase 13 success criteria

Phase 13 - across all its subphases - is successful when:

1. There is a working, local-first portfolio website that explains StoryTime
   to an outside reviewer without requiring them to run the backend.
2. The same web property functions as the first operator GUI: the operator can
   open it and see pipeline runs, run detail, stage timelines, failures,
   governance decisions, and observability evidence.
3. The frontend is decoupled from the backend by the documented contract - the
   same GUI works against a static export, a local adapter, and (if ever
   built) a cloud API, with only the adapter changing.
4. The operator GUI was read-only first, and any controlled operator actions
   were added only in the explicitly gated subphase, obeying the locked
   Architecture Baseline section 25 mutation rules.
5. The website is honest: it does not claim a production deployment, users, an
   SLA, cloud hosting, or a commercial-vendor integration, and it states its
   limitations plainly.
6. The portfolio presentation and the operator GUI coexist in one property
   without confusing each other's audiences.
7. Nothing in Phase 13 changed product behaviour to tell the story; the
   pipeline, governance, telemetry, and CLI behave exactly as the locked
   Phases 0-12 left them.

Phase 13A specifically is successful when the architecture, content model, view
model, frontend/backend contract, and subphase sequence in these five Phase 13A
documents are complete, internally consistent, honest about scope, and
detailed enough for a future implementation round to build the first frontend
scaffold (Phase 13B) without re-deciding the architecture.
