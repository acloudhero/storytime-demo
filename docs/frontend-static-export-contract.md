# StoryTime — Frontend Static Export Contract

The contract for the deterministic, read-only **static data export** that the
StoryTime frontend (the Phase 13 portfolio website and operator GUI shell)
consumes. Phase 13C defines and implements this contract.

It is the concrete, file-level realization of the principle in
`docs/frontend-backend-contract.md`:

> **Backend owns truth. Frontend owns understanding.**

The backend defines the *shape* of the export; the frontend mirrors it. Where
the earlier Phase 13B TypeScript mock types and this backend-native export
shape would disagree, the frontend yields and is updated to match the export.

## Purpose

The export gives the frontend realistic, structured data to render **without a
live backend**. It lets the portfolio site be hosted as pure static content
and lets a reviewer see the operator GUI shell with believable data. It is a
*data boundary*, not a live integration: producing and consuming the export
involves no server, no API, no network call, and no mutation.

## Source-of-truth boundary

- The **backend owns the truth.** The export is produced by backend Python
  (`storytime.operator_export`, surfaced as `storytime export-demo-ui`). The
  export *shape* is defined there.
- The **export file is a snapshot.** It is a static, committed artifact. It is
  not live and does not update on its own.
- The **frontend owns understanding.** The frontend reads the export through a
  single adapter module (`frontend/src/data/adapter.ts`) that maps the raw
  export into UI-ready view data. React components never read the raw export
  directly.
- The frontend never depends on backend internals — the SQLite schema, CLI
  output text, Python types, artifact-envelope internals, or file layout. It
  depends only on this documented export contract.

## Schema version

The export carries a top-level `schemaVersion` string (currently `"1.0"`).
A breaking change to the export shape must bump this version and be recorded
here. The frontend adapter and any future file-backed or local-API adapter can
read `schemaVersion` to detect drift.

## Deterministic export rule

The export is **deterministic**. The generator is built entirely from fixed
demo data: fixed ids, fixed ISO-8601 timestamps, fixed ordering. It uses no
`datetime.now()`, no `uuid`, no randomness, no environment-dependent path, and
no unordered iteration. The JSON is serialized with sorted keys, fixed
indentation, and a single trailing newline. **Running the export twice
produces byte-identical JSON.** A contract test
(`tests/test_operator_export.py`) asserts this and asserts that the committed
file equals a fresh render.

Regenerate the committed export with:

```bash
uv run storytime export-demo-ui
```

## Top-level JSON shape

```jsonc
{
  "schemaVersion": "1.0",
  "generatedBy": "storytime.operator_export",
  "exportKind": "phase13c_static_demo",
  "project":  { /* StoryTimeProjectSummary, including reviewerPaths */ },
  "runs":     [ /* PipelineRunDetail objects */ ],
  "failureQueue": [ /* FailureQueueItem objects */ ]
}
```

This refines the shape originally sketched in the Phase 13C prompt. The prompt
sketched `evidence`, `reviewerPaths`, and `disabledFutureActions` as separate
top-level arrays; the backend surfaces show those data relate **per run** (or
per project), so the export nests them where they belong rather than as
detached top-level lists:

- `reviewerPaths` lives inside `project` — they are project-level content.
- Each run in `runs` carries its own `governance`, ordered `stages`,
  `artifacts`, `observability` (with typed `EvidenceLink` objects),
  `allowedActions`, and `disabledActions` (the disabled/future actions).
- The runs-list summary (`PipelineRunSummary`) is **not** stored in the
  export. It is a pure projection of `runs` and is derived by the frontend
  adapter — understanding the frontend owns.

## What the export includes

- **Project summary** — name, tagline, description, current phase and status,
  what the project demonstrates, the honest "not" claims, and the tiered
  reviewer paths.
- **Pipeline runs** — for each run: id, label, status, timestamps, the ordered
  stage list (the stage-timeline data), the governance decision, an optional
  structured failure summary, artifact references, observability evidence
  links, a plain-language state explanation, the non-mutating allowed actions,
  and the disabled future actions.
- **Failure / review queue** — the runs needing operator attention, with a
  structured reason and a pointer to what to inspect next.

The data categories named in the Phase 13C prompt all appear: project summary,
pipeline runs, run detail, stage timeline (the per-run `stages`), governance
decisions, evidence links (`observability.links`), artifact/report links
(`artifacts`), validation/disabled-action status, disabled/future actions, and
placeholder readiness (the reviewer paths and the run state explanations frame
what later views will expand).

## What the export does not include

- No live or runtime data — it is a fixed demo snapshot.
- No raw story or narration text, no transcripts.
- No secrets, credentials, tokens, or personal data.
- No raw free-text error messages and no raw `blocked_reason` strings —
  failures are a structured `errorKind` code plus operator-safe guidance only.
- No embedded telemetry payloads or dashboard JSON — observability is
  references and links only.
- No mutation endpoints, no command-execution payloads on disabled actions.

## Data freshness limitations

The export is a **static snapshot**. It does not reflect live local state and
does not update unless `storytime export-demo-ui` is re-run. In Phase 13C the
content is a curated two-run demo dataset, not a projection of real runs. A
later subphase may add a file-backed adapter that assembles the same shape
from real local state; until then, "freshness" means "as of the last manual
export".

## Governance / safety display rules

The export obeys the Architecture Baseline section 25 display discipline:

- Governance decisions carry the stable status (`allowed`, `review_required`,
  `blocked`), a bounded display-safe `contextSummary`, a short structured
  `sourceCategory` code, and the standing non-legal-advice `disclaimer`.
- There is **no raw `blocked_reason`** free text anywhere in the export.
- No legal or compliance overclaiming vocabulary is used — governance records
  a human decision; it is not a certification of copyright safety.
- Disabled future actions stay disabled: they carry a `disabledReason`, the
  `enabledByPhase` that would enable them, and an `isMutation` flag, but no
  payload that could be invoked. They never imply mutation is available.

## How the export supports static portfolio hosting

The committed export lives at `frontend/src/data/storytime-demo-export.json`,
**inside the frontend source tree**. The frontend imports it statically
(a build-time `import`), so the built site bundles the data and needs no
`fetch`, no server, and no network. The static build therefore works from any
static host (GitHub Pages, Netlify, Vercel static export) or directly from the
local filesystem. This is why the export is committed under `src/data/` and
not under `public/` — `public/` would imply a runtime fetch.

## How this can evolve into file-backed or local-API adapters

The contract is transport-agnostic. The same JSON shape can later be produced
by:

- a **file-backed adapter** that reads local SQLite projections and on-disk
  artifacts and assembles this shape read-only, with no server; or
- a **local-API adapter** that serves this shape over a small local read-only
  API for an operator working with live local runs.

Because the frontend depends only on this contract and reads it through one
adapter module, switching the data source is an adapter change and a
`schemaVersion` check — not a frontend rewrite. A live or cloud backend, if it
were ever authorized, would implement the same contract. None of that is in
Phase 13C; Phase 13C delivers only the static export.

## How the frontend adapter consumes it

`frontend/src/data/adapter.ts` is the single seam:

1. it statically imports `storytime-demo-export.json`;
2. it types the import as the `StaticDemoExport` envelope from
   `frontend/src/types/storytime.ts`;
3. it exposes UI-ready values — `DEMO_PROJECT`, `DEMO_RUN_DETAILS`,
   `DEMO_FAILURE_QUEUE`, the derived `DEMO_RUN_SUMMARIES`, `findRunDetail`,
   and `EXPORT_META` (schema version and provenance).

React components import only from the adapter. If the export shape changes,
only the adapter (and the mirrored types) change; the components do not.
