> **Phase 15C — Minimal Cloud Demo Deployment / Portfolio Readiness (current implementation candidate; pending review; NOT locked).** Phase 15A — Cloud Runtime Skeleton — and Phase 15B — Cloud Boundary Readiness — are LOCKED. Phase 15 — Cloud / Distributed Runtime — remains STARTED, and **Phase 15C is STARTED as the current implementation candidate**: a public, cloud-hosted *static* operator demo of the local-first, observability-native pipeline and its cloud-readiness seams. It adds a static deployment path, narrow display-only frontend safety changes, demo docs and a talk track, and an overclaim guard; it adds no backend, no cloud service, no external broker, no object-storage adapter, no auth, no provider telemetry export, no provider TTS, no RSS, and no dependency. Phase 14E remains NOT STARTED and was not opened (intentionally bypassed). Phase 15D, Phase 15E, and Phase 15F remain NOT STARTED.

# Phase 15C — Minimal Cloud Demo Deployment / Portfolio Readiness

This phase gives StoryTime a public, shareable demo surface without pretending
the backend is in the cloud. It deploys the existing static, read-only operator
console to a static host, makes the two backend-dependent views honest and safe
for public use, and ships a tight interview talk track. The mission is *credible
demo fast, without dishonest claims or architectural damage*.

The single required disclaimer, shown in the UI and repeated in `DEMO.md`:

> This is a cloud-hosted static operator demo of a local-first, observability-native pipeline and its cloud-readiness seams.

---

## 1. What the demo is

- A cloud-hosted **static** build of the StoryTime operator console (React +
  Vite), served as plain files from a static host.
- **Read-only** and **demo-data-backed**: every view reads from the committed
  snapshot at `frontend/src/data/storytime-demo-export.json`. No view fetches a
  backend on the public demo.
- An honest portfolio artifact: it shows runtime roles, the four cloud-readiness
  seams, operator status, failure explainability, and the boundary between what
  is local-first today and what is deferred to later cloud phases.

## 2. What the demo is not

- It is **not** a hosted SaaS product, and there is no cloud backend behind it.
- No backend is running behind the public demo; nothing is deployed to the
  cloud except static files.
- No distributed worker is running; no cloud queue, no object-storage backend,
  no authentication, and no provider telemetry export exist. Those remain
  deferred to later phases (15D+).
- The demo does not mutate anything and exposes no public write endpoint.

## 3. Static-demo safety model

The build ships with `STATIC_DEMO_MODE` enabled (`frontend/src/data/demoMode.ts`).
Two views — **Local Bridge** and **Live Proof Loop** — are designed to talk to a
backend you run on your own machine over an HTTP loopback origin (127.0.0.1 /
localhost). On the public static demo they are gated by a clear local-only
notice (`StaticDemoNotice`) instead of mounting the live components, so:

- the public demo makes **no** network call to a backend;
- a visitor never sees a generic, broken network error; and
- the live loopback code is tree-shaken out of the public bundle entirely.

A developer who wants the live local experience runs the backend locally and
sets `STATIC_DEMO_MODE` to `false`. Every other view is static and unchanged.

## 4. How to build locally

```bash
cd frontend
npm ci
npm run typecheck
npm run build
```

The static site is emitted to `frontend/dist`. Vite uses `base: "./"` (relative
asset paths), so the build also works opened from the local filesystem or from
a host subpath. To preview locally: `npm run preview`.

## 5. How to deploy (primary: GitHub Pages)

A GitHub Pages workflow is committed at `.github/workflows/pages.yml`. It runs on
push to `main` (or via manual dispatch), installs with `npm ci`, type-checks,
builds, and publishes `frontend/dist` to Pages. No secret, serverless function,
or backend service is used.

Steps:

1. Push the repository to GitHub (public).
2. In the repository settings, set **Pages → Build and deployment → Source** to
   **GitHub Actions**.
3. Push to `main` (or run the workflow manually). The workflow's deploy step
   prints the public `page_url`.

Because `base` is relative, the project-pages subpath URL works without
rewrites.

### Fallback hosts (manual, documentation only)

If GitHub Pages causes friction, the same `frontend/dist` can be published as a
static site on Netlify, Vercel, or Cloudflare Pages — build command
`npm --prefix frontend ci && npm --prefix frontend run build`, publish directory
`frontend/dist`, with no functions, no redirects to a backend, and no secrets.
Only the GitHub Pages config is committed; the others are manual alternatives.

## 6. How to verify no backend / cloud claims are made

- `uv run pytest` runs `tests/test_phase15c_static_demo_claims.py`, which checks
  the required disclaimer is present (verbatim) in the frontend source and this
  doc, that the backend-dependent views are gated, that no forbidden overclaim
  phrase appears in the public-facing demo copy, and that the phase state is
  recorded honestly (15C candidate / NOT locked; 15A and 15B LOCKED; 14E and
  15D+ NOT STARTED).
- After `npm run build`, the public bundle contains the disclaimer but not the
  loopback action helpers (they are tree-shaken out under `STATIC_DEMO_MODE`).

## 7. Two-minute interview talk track (verbatim, audio-friendly)

> StoryTime is a local-first, observability-native pipeline. I proved the local
> behavior first, then separated runtime roles into api, worker, and combined
> modes. After that, I defined explicit readiness boundaries for queue and
> worker execution, artifact storage, observability export, and
> recovery/idempotency. The public demo is a cloud-hosted static operator
> console that shows the system state and those boundaries honestly. It is not a
> hosted product, and it says so. The next phase moves backend runtime execution
> into the cloud behind the same contracts without changing product behavior.
> The point is not just that AI helped build code. The point is that the system
> is built to make AI-assisted delivery trustworthy, observable, reviewable, and
> explainable.

## 8. Observability-native talking points (Dynatrace-style relevance)

- **Signal vs. source of truth:** observations are explanatory signals; durable
  backend state is the source of truth for queue, artifact, recovery, and run
  state. The demo shows this separation explicitly.
- **Runtime readiness:** roles (api / worker / combined) and pure-data
  health/readiness make the runtime shape inspectable before any cloud move.
- **Boundary readiness:** each of the four seams states what is locally active,
  what is deferred, and the invariants a cloud implementation must preserve
  (for example, single-delivery-effect claim semantics before any distributed
  worker).
- **Failure explainability and operator trust:** recovery is backend-decided and
  bounded; rejected actions stay visible; the operator can reason about what
  happened and why.
- **Migration discipline:** the same contracts carry forward, so cloud growth is
  reversible and gated rather than a rewrite.

## 9. Demo-to-backend mapping

| Demo view | What it shows | Backed by | Backend in cloud? |
| --- | --- | --- | --- |
| Overview / Run Detail / Governance / Failure / Evidence / Demo Walkthrough | Pipeline runs, governance, recovery, evidence | Committed static snapshot | N/A (static) |
| Local Bridge | Health, readiness, queue snapshot, guarded retry | Local backend (loopback) — gated to a notice on the public demo | Deferred (15D+) |
| Live Proof Loop | End-to-end proof run + run detail | Local backend (loopback) — gated to a notice on the public demo | Deferred (15D+) |

The static views map one-to-one to real local backend behavior locked in
earlier phases; the public demo presents a snapshot of that behavior, not a live
cloud system.

## 10. Next phases after 15C

Phase 15C buys a credible public link without architectural debt. The deeper
cloud path remains:

- **Phase 15D — Cloud Backend Runtime Skeleton** (NOT STARTED): move backend
  runtime behind the locked contracts.
- **Phase 15E — External Queue / Object Store Proof** (NOT STARTED): prove one
  seam against the Phase 15B invariants.
- **Phase 15F — Cloud Observability Export Proof** (NOT STARTED): map native
  domain events to an external telemetry backend without back-propagating vendor
  naming.

Phase 14E remains intentionally bypassed and NOT STARTED. Phase 15C is the
current candidate and is NOT locked; 15D, 15E, and 15F remain NOT STARTED.

## 11. Explicit statement — no cloud backend implemented

Phase 15C deploys static files only. It adds no backend execution, no serverless
function, no external broker, no object-storage backend, no authentication, no
provider telemetry export, no provider TTS, and no RSS publishing, and it
introduces no dependency. The running product remains the local-first,
observability-native, single-process proof locked through Phase 15B; the public
demo is a truthful static window onto it and its cloud-readiness seams.
