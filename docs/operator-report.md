# Operator Report

The **operator report** is a generated, static, local, read-only HTML view of
StoryTime's pipeline runs. It makes a StoryTime installation understandable,
operable, and demoable by a local operator — without a web server, a frontend
framework, or any cloud service. It is the Phase 10B implementation of the
locked Architecture Baseline Section 25 (the Phase 10A Operator Experience
Baseline).

## Generating the report

```bash
uv run storytime report generate
```

This writes the report into `operator-report/` in the current directory. To
choose another directory:

```bash
uv run storytime report generate --output /path/to/report-dir
```

`storytime report generate` reads the local SQLite state database and the
on-disk artifacts and writes a set of static HTML files plus one small local
CSS file. It starts no server and changes no state. Open the report by
pointing a browser at the generated `index.html` — no server is required, and
the report renders correctly with no network connection.

## Where the report is written

The default output directory is `operator-report/`. It is generated runtime
output — a *view* over `runs/`, never source — and is git-ignored and
docker-ignored, like `runs/` and `feed/`.

The generated files are:

| File | Contents |
|------|----------|
| `index.html` | Landing page: a read-only note, the disclaimer, and the latest-runs summary. |
| `runs.html` | The full run list — every recorded run. |
| `run-<run_id>.html` | One single-run detail page per run. |
| `style.css` | The single, local, minimal stylesheet. |

## What the report includes

The report is built from existing authoritative state only — the SQLite
`pipeline_run`, `stage_execution`, `stage_artifact`, `trust_envelope`, and
`published_episode` projections, plus the durable Trust Envelope artifact. It
never queries an observability backend.

Each run-detail page shows the bounded fields permitted by Section 25:

- `run_id`, run status, current stage, created/updated timestamps;
- the approval gates the run was configured with;
- per-stage names and statuses, and a structured failure category when a
  stage failed;
- the governance summary — the decision (`APPROVED` / `REJECTED` / `BLOCKED` /
  `NEEDS_REVIEW`), the licence type, the approver, the decision timestamp, a
  structured blocked/rejected reason if present, and a **bounded** review
  context summary;
- read-only artifact path references — stage-artifact envelope keys, the Trust
  Envelope artifact, the published audio path, and the shared RSS feed
  reference for a run that published;
- optional observability links, when configured.

## What the report intentionally excludes

The report is a bounded projection. It never shows — and the test suite proves
it never shows — any of:

- raw source story text, source body, generated narration text, or
  TTS/audio transcripts;
- secrets, tokens, API keys, or private content;
- full reviewer notes or long free-text governance notes (the durable Trust
  Envelope's `governance_notes` field is never projected into the report);
- full environment dumps, unbounded exception text, or stack traces;
- raw telemetry payloads or embedded dashboard data;
- any legal-clearance, copyright-safety, or compliance-certification claim.

Every governance page carries the standing disclaimer: *StoryTime records
human operator decisions and pipeline state. This report is not legal advice
or certification of copyright safety.* The report presents governance status
as a record of a human operator's decision — never as a legal certification.

## How governance display is bounded

The Trust Envelope's `review_context_summary` is the operator's short
governance rationale. The report displays it only **bounded**: it is capped at
500 characters (the length locked in Section 25.13). A longer summary is
safely truncated with a visible `[…truncated]` indicator — the unbounded
original never reaches the report. When a run has no summary, the report shows
a neutral placeholder. The free-text `governance_notes` field is never
displayed at all.

## How observability links behave

Observability links are **optional references only**. The report builds a
Jaeger trace link for a run only when:

1. a Jaeger base URL is configured via the `STORYTIME_JAEGER_BASE_URL`
   environment variable, **and**
2. the run has a recorded trace id.

The link is `<base>/<trace_id>` — a reference with no embedded dashboard data
and no credential or token in the URL. With nothing configured, the report
simply has no observability links and remains complete. The report never
queries Grafana, Jaeger, Prometheus, Loki, or any vendor backend.

## Determinism

Report generation is deterministic: given identical SQLite state, identical
artifacts, and an identical generation timestamp, the generated HTML is
byte-for-byte identical. The rendering core takes the timestamp as an injected
parameter; the CLI supplies the real current time, and the tests supply a
fixed timestamp so the report is snapshot-testable.

## What the report is not

The operator report is read-only. It contains no form, no button, no
state-changing link, and no JavaScript. It cannot approve, retry, reject,
rerun, delete, publish, or edit anything — those remain CLI/pipeline
operations. Adding any operator *action* surface is a separate, future,
explicitly-gated phase (Section 25.17).

It is also not a server: there is no web server, no persistent backend, no
frontend framework, no build pipeline, and no authentication. The report is a
set of inert local files.

## Known limitation

The SQLite projections record the published **audio** path per episode but do
not record a per-run RSS feed path — the RSS feed is a single shared
`feed/feed.xml`. For a run that published an episode, the report therefore
surfaces the audio path from the `published_episode` projection and references
the shared feed as `feed.xml`. A per-run feed path would require a schema
change, which Phase 10B deliberately does not make.

---

## Phase 10E refinements

Phase 10E improved the static operator report for clarity, usability, and demo readiness.

### New sections

**Executive Status Summary** — every run detail page now opens with a compact summary showing run status, governance decision, rerun eligibility, and the recommended next operator action.

**Rerun Eligibility / Action Guidance** — integrates Phase 10D rerun information. Shows whether the run is eligible for rerun, the stable decision code, an operator-facing explanation, and — when eligible — the plain-text commands to copy and run. Commands are always plain text in a `<pre>` block; the report contains no buttons, forms, or controls that execute commands or change state.

**Failure Summary** — when a run has failed, shows the failure stage, failure category, failure type, and operator guidance, classified by whether it is a technical failure, governance block, or operator rejection.

**Command Reference** — every run detail page ends with a short command reference showing the relevant CLI commands as plain text.

### Improved features

- Status badges with semantic colours across run list and detail pages.
- Attention summary on the index page (counts of failed and blocked runs).
- Improved governance warning block — visually distinct, near the top of every page, using the `governance-warning` CSS class with a coloured border and background.
- Embedded `<style>` block in every page for offline resilience; local `style.css` kept as external fallback.
- Responsive layout improvements for narrow screens.
- Improved section headings with bottom-border separators for scannability.

### What did not change

- The report remains a single generated static HTML output.
- No JavaScript. No external CSS. No CDN. No external assets of any kind.
- No browser-side mutation controls. No buttons, forms, or inputs.
- No backend behavior changed. No mutation semantics changed.
- The Phase 10D `storytime rerun` command is unchanged.
- The governance / Trust Envelope enforcement is unchanged.
- Database schema is unchanged. No new dependencies.
