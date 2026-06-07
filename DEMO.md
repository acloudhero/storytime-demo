# StoryTime — Public Demo

> This is a cloud-hosted static operator demo of a local-first, observability-native pipeline and its cloud-readiness seams.

**Live demo:** _add your published URL here after the first deploy (e.g. your GitHub Pages `page_url`)._

StoryTime is a governed, observability-native pipeline that turns approved
public-domain text into podcast-ready audio, with an operator console for
runtime status, evidence, and cloud-readiness boundaries. This page is a
**static** build of that console — read-only, demo-data-backed, and honest about
what is and is not running.

## What this demo is

- A static, read-only operator console served as plain files.
- Backed entirely by a committed demo snapshot (`frontend/src/data/storytime-demo-export.json`).
- A truthful window onto runtime roles (api / worker / combined) and four
  cloud-readiness seams: queue/worker, artifact storage, observability export,
  and recovery/idempotency.

## What this demo is not

- It is not a hosted SaaS product, and no backend is running behind it.
- Nothing is deployed to the cloud except static files: no distributed worker is
  running, and no cloud queue, object-storage backend, authentication, or
  provider telemetry export exists. Those are deferred to later phases (15D+).
- The Local Bridge and Live Proof Loop views run only against a backend you
  start on your own machine (HTTP loopback). On this public demo they show a
  clear local-only notice instead of calling anything.

## Run it locally

```bash
cd frontend
npm ci
npm run typecheck
npm run build      # outputs frontend/dist
npm run preview    # serve the static build locally
```

## Deploy the static demo

A GitHub Pages workflow is committed at `.github/workflows/pages.yml`: push to
GitHub, set **Pages → Source → GitHub Actions**, and push to `main`. It builds
`frontend/` and publishes `frontend/dist` — no secrets, no functions, no
backend. The same `dist/` can alternatively be dropped on Netlify, Vercel, or
Cloudflare Pages as a static site (publish directory `frontend/dist`).

## Two-minute talk track

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

See `docs/phase15c-minimal-cloud-demo.md` for the full design, the
demo-to-backend mapping, observability-native talking points, and the next
cloud-backend phases.
