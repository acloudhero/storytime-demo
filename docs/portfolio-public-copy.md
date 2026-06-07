# StoryTime — Portfolio Public Copy
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


*Phase 12B — Portfolio Evidence Pack / Reviewer Assets. This document holds
public-facing copy about StoryTime — for a portfolio site, a profile, or a
short written introduction — in a disciplined, non-hype Solutions-Engineer
voice. Every statement here is backed by `docs/portfolio-evidence-index.md`.
The copy deliberately avoids superlatives, buzzword inflation, and any claim
the repository cannot support. Use the variant that fits the space you are
filling.*

A note on tone: this copy is written the way a careful Solutions Engineer
would describe their own work to a technical audience — concrete, measured,
and honest about scope. It claims engineering and operational discipline,
which the project demonstrates; it does not claim a production deployment,
users, or a commercial integration, which the project does not have.

---

## One-line description

A local-first, observability-native pipeline that turns approved public-domain
text into podcast-ready audio, with a traceable record of every run.

## Short description (profile / card length, ~40 words)

StoryTime is a local-first content-to-audio pipeline built as an
engineering portfolio project. It turns approved CC0 / public-domain text into
podcast audio and an RSS feed, instruments every run with OpenTelemetry, and
enforces fail-closed content governance — all runnable offline from one
command line.

## Medium description (~110 words)

StoryTime is a local-first, observability-native pipeline that converts
approved public-domain text into podcast-ready audio, an RSS feed, and an
auditable record of every run. It runs entirely on one machine from the
command line, with SQLite and content-hashed artifact envelopes as the source
of truth and OpenTelemetry as an optional view layered on top.

The podcast pipeline is the vehicle; the subject is engineering discipline.
StoryTime confines OpenTelemetry to a single adapter and enforces that
boundary in CI, ships six dashboards defined as code with a metric-honesty
test, runs fail-closed content governance, and keeps an append-only project
history. Six Docker-free quality gates protect every change. It is a portfolio
project, not a deployed product — and it says so plainly.

## Long description (~240 words)

StoryTime is a local-first, observability-native pipeline that turns approved
CC0 and US public-domain text into podcast-ready audio, an RSS feed, and a
traceable record of every run. It runs entirely on one machine, from the
command line, with no required network calls. SQLite and on-disk,
content-hashed artifact envelopes are the source of truth; OpenTelemetry is an
optional view over that truth, never a dependency of it.

The podcast pipeline is the vehicle. The real subject is engineering and
operational discipline:

- **Observability done deliberately.** OpenTelemetry is confined to one
  adapter module, and that boundary is enforced mechanically by an
  import-linter contract in CI. The system emits a small set of
  low-cardinality metrics and ships six dashboards defined as code, with a test
  that fails if a dashboard names a metric the code does not emit.
- **Fail-closed governance.** An unauthorized source does not proceed. The
  Trust Envelope records a human decision — it is a project control, not legal
  advice — and a dedicated test ensures the system never emits invented
  legal-certification language.
- **Auditable process.** The pipeline is five staged steps plus explicit
  approval gates; a failed run re-runs from the failed stage; project history
  is append-only; and six Docker-free quality gates protect every change.

StoryTime is a portfolio project — there are no users, no SLA, and no cloud
deployment, and its `known-limitations.md` states every boundary. What it
demonstrates is how to build a small system with the discipline of a larger
one.

## "What it demonstrates" — bullet form

- A clean, layered architecture with import boundaries enforced in CI, not
  just documented.
- OpenTelemetry instrumentation confined to a single adapter, with traces,
  low-cardinality metrics, and dashboards-as-code.
- Fail-closed content governance that records human decisions and does not
  overstate its own authority.
- Operator-experience thinking: a static read-only report, a failure / review
  queue, and re-run-from-failed-stage recovery.
- Reproducibility discipline: a pinned lockfile, a deterministic
  fixture-driven demo, and six Docker-free quality gates.
- Process discipline: a phased build with independent review and an
  append-only, test-guarded project history.

## "What it is not" — honest scope statement

Use this whenever the copy above might be read as more than it is.

StoryTime is a portfolio and demonstration project. It is **not** a deployed
product: there are no real users, no service-level agreement, and no cloud
hosting. It does **not** include multi-user authentication or live alerting.
The vendor Collector files are example configurations, not certified or
production integrations with any commercial observability provider. The
content governance layer records a human authorization decision and is **not**
legal advice and **not** a rights-clearance service. Generated audio is not
committed to the repository, and the text-to-speech path is mock-grade by
default. The authoritative, complete statement of scope and non-goals is
`docs/known-limitations.md`.

## Suggested credit line

Built as an individual engineering portfolio project using a structured,
multi-model review workflow with a human decision-maker. Every phase was
implemented, independently reviewed, critiqued, and only then accepted.

---

*Companion documents: `docs/portfolio-overview.md` (the plain-English
overview), `docs/portfolio-evidence-index.md` (claim-to-evidence map),
`docs/solutions-engineer-narrative.md` (interview-length pitches), and
`docs/known-limitations.md` (authoritative scope). If any statement in this
copy is ever questioned, the Evidence Index is where it is verified.*
