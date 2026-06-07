# Deployment — Blue/Green Option A

> **Lean and demo-shaped.** This is the *first* blue/green-capable deployment
> path for StoryTime, deliberately scoped to **Option A**: the simplest
> credible shape that gives honest blue/green *designation*, *environment
> separation*, *state boundaries*, and *telemetry attribution* — and nothing
> more. It is **not** production blue/green, **not** high-availability, **not**
> multi-tenant, and **not** an automated traffic cutover. Those belong to a
> later Option B / Phase 7B and are listed under "What Option B adds" below.

## 1. Deployment target decision

**Decision: the Option A deployment unit is an uncontainerized `storytime`
process configured for one slot — not a container, not a pod.**

StoryTime is local-first by charter, and the Architecture Baseline (§16)
ARCH-LOCK on `docker-compose.observability.yml` is explicit that the
*application* is not containerized — Docker exists only for the local
observability stack (Collector / Jaeger / Prometheus / Grafana). Phase 7A
honours that locked decision. The "cloud-shaped" property we add is not a
container image; it is a **clean separation of deployment identity from code**:
a slot, an environment, a state root, a feed root, a port, and telemetry
resource attribution — all environment-driven, all overridable, none hard-coded.

A "deployment" in Option A is therefore: *run the `storytime` CLI with a slot
environment loaded.* Two slots (`blue`, `green`) are two such processes on one
host, each with its own SQLite state database, its own feed directory, and its
own loopback port. This is the simplest path that is genuinely blue/green and
does not overbuild toward the final architecture.

**Explicitly not chosen, and why:**

- **No Dockerfile for the app.** Containerizing the application would
  contradict Architecture Baseline §16 and is not needed for a credible Option
  A demo. Whether Option B containerizes the app is a real open question — it
  is recorded as a Phase 7B item and a risk for mediator review, not decided
  here.
- **No Kubernetes.** Not proven necessary; explicitly out of Phase 7A scope.
- **No Terraform / IaC.** Nothing to provision — there is no cloud resource.
- **No load balancer / reverse proxy.** Option A has no automated traffic
  switch (see §6).

## 2. What Phase 7A added

| Piece | What it is |
|-------|-----------|
| `STORYTIME_DEPLOYMENT_SLOT` | Slot identity (`blue` / `green` / unset). Validated as a safe path segment. |
| `STORYTIME_ENVIRONMENT` | Free-form environment label (`local` / `demo` / `staging` / ...). |
| Slot-scoped state roots | With a slot set, `runs/` and `feed/` default to `runs/<slot>` and `feed/<slot>`. |
| `config/deploy/blue.env`, `config/deploy/green.env` | Per-slot environment files. No secrets. |
| `scripts/run-slot.sh` | Lean launcher: loads a slot env file and runs `storytime` in it. |
| `storytime doctor` banner | Prints the resolved deployment identity and state/feed roots. |
| Telemetry resource attribution | `deployment.environment` and `deployment.slot` on the OTel `Resource` (the Phase 5 fields are now actively driven by a real slot). |

No business logic, stage, runner, telemetry instrument, dashboard, or feed
format changed.

## 3. How to run local blue

```sh
scripts/run-slot.sh blue doctor
scripts/run-slot.sh blue run --manifest sources/the-raven.json --auto-approve
scripts/run-slot.sh blue serve            # serves feed/blue on port 8000
```

`config/deploy/blue.env` sets `STORYTIME_DEPLOYMENT_SLOT=blue`, so:

- the state database is `runs/blue/state.db`,
- per-run working directories are `runs/blue/<pipeline_run_id>/`,
- the published feed is `feed/blue/feed.xml`,
- the loopback feed server binds `127.0.0.1:8000`.

Equivalently, without the launcher:

```sh
set -a; . config/deploy/blue.env; set +a
uv run storytime doctor
```

## 4. How to run local green

```sh
scripts/run-slot.sh green doctor
scripts/run-slot.sh green run --manifest sources/the-raven.json --auto-approve
scripts/run-slot.sh green serve           # serves feed/green on port 8001
```

`config/deploy/green.env` sets `STORYTIME_DEPLOYMENT_SLOT=green`, giving
`runs/green/state.db`, `feed/green/feed.xml`, and loopback port `8001`. Blue
and green can run **at the same time** on one host: different state roots,
different feed roots, different ports — nothing is shared.

## 5. How to identify each slot in telemetry

When `STORYTIME_TELEMETRY=otel`, every span and metric carries the OTel
`Resource` attributes:

| Resource attribute | Blue | Green |
|--------------------|------|-------|
| `service.name` | `storytime` | `storytime` |
| `service.version` | the package version | the package version |
| `deployment.environment` | `local` (or whatever `STORYTIME_ENVIRONMENT` is) | same |
| `deployment.slot` | `blue` | `green` |

In Jaeger, filter spans by the `deployment.slot` resource attribute to see one
slot's traces. In Grafana/Prometheus the same attribute is available for
per-slot breakdowns. `deployment.slot` is a **resource** attribute, set once
from immutable config — it is never a per-span or per-metric label, so it adds
no cardinality. `storytime doctor` prints the same identity locally so an
operator can confirm a slot before running anything.

## 6. How to "switch" between slots — honest semantics

**Option A has no automated traffic switch.** This is the deliberate boundary
of Option A, and the runbook and this document state it plainly rather than
implying a cutover that does not exist.

What a blue/green "switch" means in Option A:

- Each slot serves its own feed on its own loopback port (`blue` → 8000,
  `green` → 8001). A podcast client / demo viewer is pointed at whichever port
  is the *active* slot.
- "Cutting over" is an **operator action**: bring the new slot up, verify it
  (`storytime doctor`, run a pipeline, check `feed/<slot>/feed.xml`), then point
  consumers at the new slot's port. "Rolling back" is pointing them back.
- Because state roots are fully separated, a switch or rollback **never**
  migrates or mutates the other slot's data. The idle slot is untouched and
  remains a valid rollback target.
- There is no shared database, so there is no split-brain risk and no schema
  coordination between slots in Option A.

That is the whole, honest mechanism: parallel slots, separated state, an
operator decision about which port is "live." Anything more — a proxy, a single
front-door URL, health-gated automatic promotion — is Option B.

> **Option B (Phase 7B) is now implemented.** A stable local front door and a
> persisted active-slot pointer with a scripted switch / rollback are added in
> `docs/deployment-bluegreen-option-b.md`. The Option A model below is the
> foundation it builds on and is unchanged.

## 7. Limitations of Option A

- **No automated traffic cutover or health-gated promotion.** Switching is a
  manual operator step (§6).
- **Single host.** Both slots run on one machine; there is no cross-host
  distribution and no HA.
- **No front door.** Consumers address a slot by its port directly; there is
  no stable single URL that hides the active slot.
- **No app container / image artifact.** The deployment unit is a process; it
  is not a versioned, pullable image (see §1).
- **No production auth, no multi-tenant isolation, no active alerting.**
  Unchanged from earlier phases and explicitly out of Phase 7A scope.
- **Shared host resources.** Blue and green share CPU, disk, and the (optional)
  single local observability stack; they are isolated in *state*, not in
  *resources*.
- **Slot is not auto-created beyond blue/green.** `config/deploy/` ships
  `blue.env` and `green.env`; another slot needs its own env file.

## 8. What Option B adds later (deferred, not built here)

Option B / Phase 7B is where enterprise blue/green mechanics belong. Phase 7A
deliberately preserves the upgrade path to it:

- A real cutover mechanism — reverse proxy or single front-door URL with
  health-gated, possibly automated promotion and one-command rollback.
- A decision on whether the app is containerized and shipped as a versioned
  image (the open question from §1).
- Multi-host / HA topology if ever warranted.
- Production-grade auth and, if multi-tenant, real tenant isolation.
- Active alerting and an error-budget / burn-rate policy (today there is
  none — see `docs/slo-sli.md`).
- Vendor telemetry fan-out, if a hosted backend is ever adopted.

None of the above is implemented in Phase 7A. The Phase 7A surface — slot
identity, environment, separated state roots, telemetry resource attribution —
is exactly the seam Option B builds on, so adopting Option B does not require
unwinding Option A.

## 9. Constraints preserved

Phase 7A keeps every earlier guarantee intact:

- **Local-first behaviour** — no slot is required; with no slot set the layout
  is `runs/` and `feed/` exactly as before.
- **`NoopTelemetry` is the default**; `OTelTelemetry` is opt-in; the
  OpenTelemetry import boundary is unchanged (one adapter module).
- **SQLite + `event_log` + artifacts remain the source of truth**;
  `pipeline_run_id` remains the durable correlation key.
- **The test suite needs no Docker and no cloud**; slot resolution is pure
  configuration logic.
- Phase 6 dashboards, the demo harness, and the feed format are untouched.

See `docs/runbook.md` §5 for the operator-facing blue/green procedures and
`docs/telemetry-map.md` for the resource-attribution detail.
