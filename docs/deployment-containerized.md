# Deployment — Optional Local App Containerization (Phase 7C.1 / 7D)

This document describes the **optional** containerized way to run StoryTime's
blue/green slots, delivered under the locked Phase 7C / 7C.1 Architecture
Baseline amendment.

> **Read this first.** Containerization is **optional**. Bare-metal local
> Python — `uv run storytime ...` and `scripts/run-slot.sh` — remains the
> **default and fully supported** way to run StoryTime. Docker is never
> required: the six quality gates (`uv sync --frozen --extra dev`,
> `uv run pytest -q`, `uv run ruff check .`, `uv run mypy`,
> `uv run lint-imports`, `uv run storytime doctor`) all pass with no Docker
> installed. This is a **single-host, demo-grade** capability — not production
> deployment.

## Scope — what this is and is not

This is: an optional way to run the existing blue and green slots as two local
containers from one image, each with isolated SQLite state and feed.

This is **not**, and this phase does not provide: cloud deployment; image
publishing to any registry (Docker Hub, ECR, GHCR, GCP Artifact Registry,
ACR); Kubernetes; Terraform; Helm; CI/CD image builds; production HA;
production zero-downtime deployment; production auth; multi-tenant behavior;
active alerting; or vendor telemetry fan-out. The image is built on your local
Docker daemon and stays there.

## Files

- `Dockerfile` — the StoryTime application image (pinned base, non-root user,
  installs the locked `uv.lock` dependency set, includes `ffmpeg`).
- `.dockerignore` — keeps `runs/`, `feed/`, `.env`, secret files, and caches
  out of the build context.
- `docker-compose.app.yml` — optional blue/green app-slot definition.

## Quick start

The image is built once and both slots run from it. Both of these work — the
first is the explicit happy path, the second works on a fresh Docker cache too:

```
# Happy path — optional; bare-metal still works
docker compose -f docker-compose.app.yml config    # validate the compose file
docker compose -f docker-compose.app.yml build     # build storytime-app:local once
docker compose -f docker-compose.app.yml up -d      # start blue + green
docker compose -f docker-compose.app.yml ps         # both services should be running
curl -i --max-time 5 http://127.0.0.1:8000/feed.xml   # blue slot
curl -i --max-time 5 http://127.0.0.1:8001/feed.xml   # green slot
```

```
# Fresh machine — no separate build step needed. `up -d` builds the image if
# it is missing, then starts both slots:
docker compose -f docker-compose.app.yml up -d
```

You do **not** need to build a single service first, and you do not need to
know any workaround — `docker compose build` and `docker compose up -d` both
work directly. This is because exactly one service (`storytime-blue`) owns the
image build; `storytime-green` consumes the same `storytime-app:local` image
and is marked `pull_policy: never` so it never tries to pull that local-only
tag from a registry. See *Build contract* below.

A `404 Not Found` from either slot is **expected and acceptable** before a feed
has been published — it still proves the StoryTime feed server is reachable
(check the response headers). Publish a feed first to get real content:

```
docker compose -f docker-compose.app.yml run --rm storytime-blue \
  run --manifest sources/the-raven.json --auto-approve

# Stop the slots (named volumes are kept — state survives):
docker compose -f docker-compose.app.yml down
```

### Build contract

One image, `storytime-app:local`, built by one service:

- `storytime-blue` is the **only** service with a `build:` section — it builds
  and exports `storytime-app:local`.
- `storytime-green` has **no** `build:` section — it runs the same image and
  is marked `pull_policy: never`.

Earlier both services declared `build:` and exported the same tag, so a
parallel `docker compose build` raced on the image export
(`image "storytime-app:local": already exists`). With a single builder there
is exactly one export and no race. On a fresh cache, `docker compose up -d`
runs blue's build (creating the image) before any container is created, and
`pull_policy: never` keeps green from attempting a doomed registry pull of the
local-only tag. Green's `depends_on` only orders container *startup* — it is
not what makes the image available.

The Phase 7B front door is unchanged and still runs on the host. Smoke path:

```
uv run python -m storytime.frontdoor serve            # front door on 127.0.0.1:8080
curl -i --max-time 5 http://127.0.0.1:8080/feed.xml   # routes to the active slot
uv run python -m storytime.frontdoor switch green     # switch active slot -> green
curl -i --max-time 5 http://127.0.0.1:8080/feed.xml   # now routed to green, no restart
uv run python -m storytime.frontdoor switch blue      # roll back -> blue
curl -i --max-time 5 http://127.0.0.1:8080/feed.xml
```

The front door re-reads `config/deploy/active-slot` per request, so a switch
takes effect with no restart. `scripts/run-frontdoor.sh` and
`scripts/switch-slot.sh` wrap the same commands.

## Loopback-only networking and the `network_mode: host` choice

Architecture Baseline §15 requires StoryTime to serve on loopback only;
`validate_bind_host()` rejects `0.0.0.0` in code and that locked check is not
weakened here. The app compose uses `network_mode: host` so that:

- the app binds `127.0.0.1` itself (from the slot env file), exactly as
  bare-metal — it binds `0.0.0.0` nowhere;
- with host networking the slot is reachable only on the host loopback
  (`127.0.0.1:8000` / `:8001`), so the host front door reaches it unchanged.

Bridge networking with published ports is deliberately **not** used: a
published port would require the in-container app to bind `0.0.0.0`, which the
locked §15 bind check forbids. Host networking keeps the loopback guarantee
literal and needs no code change.

**Caveat.** `network_mode: host` is native on Linux. On Docker Desktop
(macOS / Windows) it requires the host-networking feature of a recent Docker
Desktop; OrbStack supports it. If host networking is unavailable, run the
slots bare-metal instead — that path is always supported.

## SQLite state and named volumes

Each slot's SQLite state and feed live on **per-slot named Docker volumes**
(`storytime-blue-state`, `storytime-blue-feed`, `storytime-green-state`,
`storytime-green-feed`), never on a host bind mount.

This is a safety requirement, not a preference. SQLite WAL mode depends on
correct POSIX file locking and shared-memory `mmap`. Host bind mounts on
Docker Desktop / OrbStack pass through a virtualized file-sharing layer
(virtiofs / gRPC-FUSE) that does not reliably provide those semantics — using
one for the SQLite state risks corruption or data loss. Named volumes sit on
the Docker VM's native Linux filesystem, where locking and `mmap` are correct.
**Never bind-mount a slot's SQLite state directory from the host.** Read-only
bind mounts of non-WAL input material (e.g. a `sources/` directory) are fine
and are shown commented-out in the compose file.

### Volume lifecycle

Named volumes are independent of container lifecycle. `docker compose down`
(without `-v`), rebuilding the image, and recreating a slot container all
**keep** the volume — the slot's SQLite state and published feed survive.
Nothing durable lives in the container's writable layer.

### Resetting a slot (destructive)

> **Warning — destructive local operation.** Removing a slot's named volume
> permanently deletes that slot's local historical timeline: its SQLite state
> database, all per-run working directories, and its published feed/audio.
> There is no undo. Only do this when you intend to discard that slot's
> history.

```
docker compose -f docker-compose.app.yml stop storytime-blue
docker volume rm storytime-app_storytime-blue-state storytime-app_storytime-blue-feed
docker compose -f docker-compose.app.yml up -d storytime-blue   # fresh, empty slot
```

This is intentionally a documented manual procedure, not an automated reset
script.

## Blue/green state divergence

Blue and Green slots use strictly isolated state. Switching slots changes
which isolated timeline is served. Switching does not merge, migrate, copy, or
promote SQLite databases or historical run state. This is intentional for the
local/demo-grade blue/green model because rollback safety is prioritized over
automatic state convergence.

In practice: a switch (or rollback) re-points consumers at the *other* slot's
separate timeline of runs and published feed. The inactive slot is preserved
untouched as a warm rollback target — it is **not blocked**, only **not
routed**. If you want the candidate slot to mirror the live slot's history,
that is a manual, out-of-band action and is outside the scope of this phase.

## Switch and rollback are demo-grade

The Phase 7B front door, the host active-slot pointer
(`config/deploy/active-slot`), and the switch/rollback mechanism are
**unchanged** by containerization. Switch and rollback remain **pointer-based
and operator-initiated**. This is not production zero-downtime deployment and
makes no such claim — it is a single, scripted operator action against a
pointer.

## Telemetry identity

`service.instance.id` is pinned to a stable, slot-derived value
(`storytime-blue` / `storytime-green`), derived only from the deployment slot,
so it is identical whether a slot runs bare-metal or in a container. It is
never a container ID, PID, or hostname. No OpenTelemetry Docker/host/process
resource detector is used; the explicitly-constructed resource is
authoritative. The app owns telemetry identity; the OpenTelemetry Collector
owns routing. See `docs/telemetry-map.md`.

## Phase 8 (recorded, not implemented)

Vendor telemetry fan-out is **deferred to Phase 8** and is not implemented
here. The recorded direction: a local/open-source stack — OpenTelemetry
Collector, Prometheus, Loki, Jaeger, Grafana — and a vendor priority of
Dynatrace (primary), New Relic (secondary), Datadog (deferred). Phase 8 must
remain optional, disabled by default, and Collector-owned, and must add no
vendor SDK to StoryTime application code.

## Security and secrets

StoryTime has no secrets today. Any future runtime-injected credentials must
live in a git-ignored `*.local.env` / `*.secret.env` file (covered by
`.gitignore` and `.dockerignore`), must never be committed, and must never be
baked into an image. No registry login or push is used or documented.
