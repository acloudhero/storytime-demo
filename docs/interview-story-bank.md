# StoryTime — Interview Story Bank
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


Reusable interview stories and answer frames built from the StoryTime project,
oriented toward **Solutions Engineer, observability, and cloud-native** roles.
Each entry gives a structured frame you can adapt to the specific question, a
worked example answer, and the concrete evidence that backs it.

This document adds no product behaviour. It packages, as interview material,
the system that Phases 0–11 built and hardened. Every example answer stays
inside what the project actually does — if a claim here is not backed by a
test, a config file, a source module, or another document, it does not belong
here. The map from claim to evidence is `docs/portfolio-evidence-index.md`.

Companion Phase 12C documents: `docs/portfolio-demo-narrative.md` (the
narrative spine), `docs/demo-talk-track.md` (the spoken walkthrough). Earlier:
`docs/solutions-engineer-narrative.md`, `docs/interview-talking-points.md`,
`docs/se-interview-evidence-matrix.md`.

**How to use it.** Read the frame, not the script. Interviewers can tell a
memorised paragraph from a real one; the worked answers below are there to
show *shape and honesty*, not to be recited. Lead with the structure, land on
the concrete evidence, and stay honest about scope — an answer that names a
limitation is stronger than one that does not.

A note on honesty that applies to every answer: StoryTime is a **portfolio
proving ground**, not a product shipped to users. It has no users, no SLA, no
cloud deployment, and no commercial-vendor integration. Say so. The discipline
of not overclaiming is itself the thing a Solutions Engineer is being assessed
on.

---

## 1. "Tell me about a technical project you built."

**Frame:** *Context → what makes it different → one concrete detail → honest
scope.* Resist listing features. Name the *subject* of the project, give one
detail that proves depth, and close by naming what it is not.

**Worked answer:**

> "I built StoryTime — a local-first, observability-native content-to-audio
> pipeline. It turns approved public-domain text into podcast audio, an RSS
> feed, and a traceable record of every run, and it runs entirely on one
> machine from the command line.
>
> But the podcast pipeline is the vehicle. The subject is engineering
> discipline. The thing I'm proudest of is that the boundaries are enforced,
> not just intended: all OpenTelemetry imports are confined to one adapter
> module, and that's checked by both an import-linter contract and an
> AST-scanning test. There's also a test that fails the build if a dashboard
> charts a metric the code doesn't actually emit.
>
> It's deliberately not a production product — no users, no SLA, no cloud. It's
> a controlled environment where I could practise observability, reliability,
> and governance reasoning and make every piece of it checkable."

**Evidence:** the five-stage pipeline (`src/storytime/pipeline/`), the
telemetry-confinement import-linter contract and AST test
(`tests/test_import_boundaries.py`, `tests/test_telemetry_*`), the
metric-honesty test (`tests/test_dashboards.py`), `docs/portfolio-overview.md`.

---

## 2. "How did you design for reliability?"

**Frame:** *Define reliability for this system → the design choice → the
enforcement → the failure-handling story.* Reliability here is not uptime;
it is "the system survives a crash and an operator can always tell what
happened."

**Worked answer:**

> "For StoryTime, reliability meant three things: state survives a crash,
> failure is legible, and recovery is safe.
>
> State survives because every stage persists to SQLite in WAL mode and to
> hash-verified artifact envelopes *before* anything else happens — including
> before telemetry. A run can be resumed from persisted state; there's a real
> W3C trace link from a resumed run back to its pre-pause trace.
>
> Failure is legible because it's structured state, not a stack trace. A failed
> run carries an `error_kind` code and shows up in a deterministic triage
> queue with a next action. I inventoried the highest-risk failure paths in a
> regression risk register and mapped each to the tests that protect it.
>
> Recovery is safe because there's exactly one mutation command, `rerun`, it
> supports a `--dry-run` to confirm safety before changing anything, the
> mutation is a single bounded status reset, and every real mutation writes an
> audit event. Governance is never bypassed on the recovery path."

**Evidence:** the SQLite state store and `event_log`
(`src/storytime/state/`), resume/rehydration (`tests/test_rehydration.py`,
`tests/test_resume_cli.py`), `docs/regression-risk-register.md`,
`docs/failure-mode-test-matrix.md`, `docs/operator-failure-response.md`,
the `rerun` command and its tests (`tests/test_operator_rerun.py`).

---

## 3. "How did you think about observability?"

**Frame:** *Observability as a design property → telemetry is a view, not the
truth → honesty enforcement → vendor-neutrality.* This is the central SE
question; give it the most depth.

**Worked answer:**

> "I treated observability as a design property, not a layer added at the end.
> StoryTime emits real OpenTelemetry — one `pipeline.run` span per run with
> child stage spans, and a closed set of eight purposeful, low-cardinality
> metrics. `pipeline_run_id` is deliberately *not* a metric label, so metric
> cardinality stays bounded — the ULID is the correlation key in traces and
> logs instead.
>
> The principle I held to is that telemetry is a *view*, never the source of
> truth. Persistence to SQLite happens before telemetry is emitted, and with
> the default no-op adapter the pipeline behaves identically with no telemetry
> at all — observability can fail without the product failing.
>
> And I made honesty enforceable. There's a test that fails the build if a
> dashboard charts a metric the code doesn't emit — the dashboards, which are
> provisioned as code, can't outrun the data. The whole OpenTelemetry surface
> is confined to one adapter module, checked by a linter and an AST test.
>
> Because it emits standard OTLP to a local Collector, fan-out to a commercial
> backend would be a configuration change, not a rewrite. I don't integrate
> any vendor and I don't claim to — but I can show the architecture that makes
> it a config change."

**Evidence:** `docs/telemetry-map.md`, the span/metric model
(`src/storytime/adapters/telemetry/`), `tests/test_telemetry_otel.py` and
`tests/test_telemetry_phase5.py`, the metric-honesty test
(`tests/test_dashboards.py`), `config/otel-collector.yaml`,
`docs/observability-demo.md`.

---

## 4. "How do you explain technical value to non-technical stakeholders?"

**Frame:** *Translate the system into an outcome the stakeholder cares about →
use the artifact a non-coder can read → check understanding.* For an SE this
is a core competency, not a soft skill.

**Worked answer:**

> "I start from the outcome, not the architecture. For StoryTime, the
> non-technical version is: 'It's a workflow you can trust — at any point you
> can tell what happened, why, and what to do next.' That's a sentence a
> stakeholder can hold onto.
>
> Then I show them the artifact that doesn't require code to read: the static
> HTML operator report. It has a stage timeline, a plain-language failure
> summary, and a next-action section. A non-technical person can look at a
> failed run's report and understand the situation without me translating a
> log.
>
> I deliberately built a portfolio layer for exactly this — an overview, a
> narrative, a public-copy document with short, medium, and long descriptions —
> so the explanation scales to the audience. And I check understanding by
> asking them to tell *me* what a given run did; if they can, the explanation
> worked."

**Evidence:** the static operator report (`src/storytime/reporting/`,
`docs/operator-report.md`), `docs/portfolio-overview.md`,
`docs/portfolio-public-copy.md`, the three-length talk track
(`docs/demo-talk-track.md`).

---

## 5. "What tradeoffs did you make?"

**Frame:** *Name a real tradeoff → both sides honestly → why you chose as you
did → what it cost.* A non-answer ("no real tradeoffs") signals shallow work;
pick one and own both sides.

**Worked answers — pick one to fit the question:**

> **Telemetry strictly as a view.** "The easy path is to let observability and
> persistence interleave — emit as you go. I chose to persist to SQLite before
> emitting any telemetry, and to confine all OpenTelemetry to one adapter
> module. That cost discipline and a little ceremony. What it bought is the
> property that telemetry can fail entirely and the pipeline is unaffected — I
> decided that property was worth the cost."

> **In-process contracts for a single-process system.** "StoryTime runs in one
> process, so I could have used a shared mutable context object and saved
> code. Instead the stages communicate only through serializable DTOs and
> hash-verified artifact envelopes, and no stage calls another. That's more
> ceremony than the system strictly needs *today* — the payoff is that the
> architecture would survive being pulled apart into a distributed pipeline
> without redesign."

> **Local-first over a hosted demo.** "A hosted demo is more impressive at a
> glance. I chose local-first: one machine, no cloud account, no network
> required. The cost is there's no live URL to show. The benefit is that the
> trust surface is tiny and any reviewer can reproduce the *exact* behaviour I
> see — which, for a portfolio project, is worth more than a URL."

**Evidence:** the telemetry boundary (`tests/test_telemetry_noop.py`,
`tests/test_import_boundaries.py`), the contract model
(`src/storytime/pipeline/`, `tests/test_phase3_boundaries.py`),
`docs/known-limitations.md`, the `demo/` fixtures and the Phase 11B
fresh-clone verification (`docs/operator-reproducibility-checklist.md`).

---

## 6. "What would you improve next?"

**Frame:** *Name a real gap → why it matters → how you'd approach it
responsibly → tie it to the roadmap.* Show that "next" is considered, not
hand-waved.

**Worked answer:**

> "The honest gap is that StoryTime has no graphical interface. The CLI and
> the static report are honest and inspectable, but they're not *tactile* —
> you can't see the system's state at a glance. That matters because an
> operator internalises a system faster through a visual interaction layer.
>
> So the next phase — Phase 13 in the roadmap — is a decoupled operator
> console. The thing I'd be careful about is *not* starting by building a
> React app. I'd start by defining a stable operator-console contract: what
> data the GUI needs, which actions are read-only versus mutating, and how the
> same UI behaves whether the backend is local files, a local API, or a future
> cloud API. The first GUI version would be read-only; safe mutation controls
> would come only after the contract is stable.
>
> That's already scoped in `docs/GUI_vision.md` and the roadmap as planned,
> not-started work — I deliberately kept it out of the current phase so the
> portfolio packaging closed cleanly first."

**Evidence:** `docs/GUI_vision.md`, the Phase 13 roadmap note in
`docs/roadmap.md`, `docs/known-limitations.md`.

---

## 7. "How does this demonstrate customer-facing technical credibility?"

**Frame:** *What an SE actually does → which StoryTime properties map to it →
the honesty point as a credibility signal.* Connect the project to the day-to-
day of the role.

**Worked answer:**

> "A Solutions Engineer has to do four things credibly: reason about telemetry
> honestly, explain a vendor-neutral architecture, make reliability concrete,
> and translate technical value to a stakeholder. StoryTime is a worked
> example of all four.
>
> On telemetry: it shows OpenTelemetry used as a first-class design input,
> with an enforced rule that the dashboards never outrun the data. On
> architecture: it's built so that fan-out to a commercial OTLP backend is a
> configuration change — that's exactly the recommendation an SE makes to a
> customer, demonstrated rather than described. On reliability: failure is
> structured state with a documented operator response and tested invariants.
> On translation: there's a portfolio layer and a static report a
> non-technical stakeholder can read.
>
> But the strongest credibility signal is the discipline of *not* overclaiming.
> I don't claim a vendor integration I don't have, a legal determination the
> governance gate doesn't make, or a production deployment that doesn't exist —
> and there are tests and an append-only history that keep me honest. An SE who
> overclaims loses a customer's trust. A project that's precise about its own
> limits is the better evidence that I won't."

**Evidence:** `docs/se-interview-evidence-matrix.md`,
`docs/observability-governance-talking-points.md`, the legal-hallucination
scanner (`tests/test_legal_hallucination_gate.py`),
`docs/known-limitations.md`, the append-only `docs/canonical-state.md` and
`docs/phase-history.md`.

---

## Cross-cutting honesty checklist

Before using any answer above in a real interview, confirm it still holds:

- It describes what StoryTime *actually does* — no feature is invented.
- It does **not** claim users, an SLA, a production deployment, or cloud
  hosting.
- It does **not** claim integration with any named commercial observability
  vendor — only OpenTelemetry / OTLP compatibility.
- It does **not** describe the governance gate as making a legal or
  rights-clearance decision.
- Every concrete claim can be pointed at a file via
  `docs/portfolio-evidence-index.md`.
- It names at least one limitation rather than presenting the project as
  complete.

This document is part of Phase 12C — Portfolio Demo Narrative / Public
Presentation Kit. Phase 12C is a documentation-only portfolio packaging phase;
it changes no product, runtime, API, CLI, or telemetry behaviour.
