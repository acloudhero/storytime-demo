# Deployment — Blue/Green Option B (Front Door / Active-Slot Switching)

> **Higher-assurance, still local and demo-grade.** Option B builds directly on
> the locked Phase 7A Option A path. Phase 7A gave two parallel slots with
> separated state, feeds, and ports, but no single entry point — a consumer had
> to know *which port* was live. Option B (Phase 7B) adds a **stable local
> front door** and an **explicit, persisted active-slot pointer** with a
> **scripted switch and rollback**. It is **not** production zero-downtime
> deployment, **not** cloud, **not** Kubernetes, **not** app containerization,
> and **not** Phase 8 telemetry fan-out. See §8 for what stays deferred.

## 1. What Phase 7B adds

| Piece | What it is |
|-------|-----------|
| Front door (`storytime.frontdoor`) | A native Python, loopback-only reverse proxy. One stable port (default `127.0.0.1:8080`) in front of the blue/green slots. |
| Active-slot pointer (`config/deploy/active-slot`) | A one-token text file holding `blue` or `green` — the single source of truth for which slot the front door serves. |
| `scripts/run-frontdoor.sh` | Launcher: starts the front door from the repository root. |
| `scripts/switch-slot.sh` | Scripted switch: updates the active-slot pointer. Rollback is the same script targeting the previous slot. |
| `python -m storytime.frontdoor` | The underlying tool: `serve`, `switch <slot>`, `status` subcommands. |

No pipeline, runner, stage, telemetry instrument, dashboard, feed format, or
Phase 7A slot/state code changed. The front door is purely additive.

## 2. Front-door mechanism decision — native Python, not Caddy/nginx

**Decision: the front door is a native Python reverse proxy (standard library
only), not an external Caddy or nginx binary.**

The Phase 7B brief expressed a preference for an external proxy (Caddy
preferred). After inspecting the codebase this implementation chose the
explicitly sanctioned alternative — a native Python front door — because it is
the better fit for StoryTime's established properties:

- **Local-first, zero external dependencies.** StoryTime's charter and the
  whole deployment track are local-first; the test suite requires nothing
  external. An external proxy binary would make the front door
  untestable-by-default and non-functional on any machine without that binary.
  A native Python front door has **zero new dependencies** — `http.server` and
  `http.client` are standard library.
- **Fully testable in the normal suite.** Because the front door is Python, it
  is exercised end-to-end by ordinary `pytest` tests (real proxying, switch,
  rollback, Range relay, 502/503) with **no skip-by-default smoke tests** and
  no external binary.
- **Same engineering discipline as the rest of the code.** It lives in
  `src/storytime/frontdoor/` under the same ruff, mypy (strict), and
  import-linter contracts as everything else, and it imports no
  `opentelemetry`.
- **No heavy proxy runtime.** It honours the non-goal against Envoy/Kong-class
  dependencies — it is far lighter, not heavier.

The cost is that a reverse proxy is more code than a Caddyfile. That code is
small, bounded, standard-library-only, and the hardening it needs (loopback
bind, faithful Range relay, honest 502/503) is exactly the implementation
remit. The mechanism is loopback-only and demo-grade by design.

This is a deliberate, documented divergence from the brief's stated
preference. It is flagged for mediator review in the Phase 7B response
(§15) — a reviewer who wants the external-proxy path can still ask for it.

## 3. The front door

The front door binds **one stable loopback port** — default
`127.0.0.1:8080` — and on **every request** reads the active-slot pointer and
forwards to that slot's Phase 7A feed port (`blue` → `127.0.0.1:8000`,
`green` → `127.0.0.1:8001`, discovered from `config/deploy/<slot>.env`). It is
a faithful reverse proxy: it relays the upstream status, headers, and body,
including `Range` requests and `206 Partial Content` / `Content-Range`, so
podcast-client byte-range streaming works through it unchanged.

Start it from the repository root:

```sh
scripts/run-frontdoor.sh                 # binds 127.0.0.1:8080
scripts/run-frontdoor.sh --port 8080     # explicit port
```

A consumer / demo viewer always uses `http://127.0.0.1:8080/` and never needs
to know which slot is live. Bring the slots up with the Phase 7A launcher:

```sh
scripts/run-slot.sh blue  serve          # blue feed on 127.0.0.1:8000
scripts/run-slot.sh green serve          # green feed on 127.0.0.1:8001
scripts/run-frontdoor.sh                 # front door on 127.0.0.1:8080
```

**No external proxy binary is required.** The front door is native Python;
the only runtime requirement is Python + `uv`, already required to run
StoryTime at all. `run-frontdoor.sh` installs nothing and downloads nothing;
if `uv` is missing it fails clearly with exit code 2.

If the front door cannot reach the active slot's process it answers an honest
`502 Bad Gateway`; if the active-slot pointer is missing or invalid it answers
`503` — see §6.

## 4. The active-slot pointer — the single source of truth

`config/deploy/active-slot` is a plain-text file containing exactly one slot
name (`blue` or `green`, newline-terminated). It is the **single source of
truth** for the front door:

- The native front door reads it **on every request**, so a switch takes
  effect for the next request with **no proxy reload and no front-door
  restart**. There is no separate generated proxy config to drift out of sync.
- Only a **safe slot name** is ever accepted or written — the same
  `[a-z0-9][a-z0-9._-]*` rule `load_config` enforces for Phase 7A slots
  (`storytime.config.is_valid_slot_name`). A traversal-like value
  (`../green`), a value with whitespace, uppercase, slashes, or shell
  metacharacters is rejected at read time and at write time.
- It is **trivial to inspect**: `cat config/deploy/active-slot`.
- It **survives a restart** — it is just a file. Restarting the front door,
  or the whole host, resumes serving the same active slot.
- Writes are **atomic** (temp file + `os.replace`), so a reader can never see
  a torn pointer.

Inspect the current state any time:

```sh
python -m storytime.frontdoor status
```

This prints the pointer path, the active slot, and every configured slot's
endpoint, marking which one is active.

## 5. Switch and rollback

A **switch** points the front door at a different slot. Rollback is the *same*
mechanism targeting the previous slot — there is no separate rollback path.

```sh
scripts/switch-slot.sh green     # switch blue -> green
scripts/switch-slot.sh blue      # roll back  green -> blue
```

The switch logic (`storytime.frontdoor.switch.switch_active_slot`):

1. Accepts a target slot (`blue` / `green`).
2. Validates the target slot is a safe slot name.
3. Confirms the target slot is configured — it must have a usable
   `config/deploy/<slot>.env`.
4. Confirms the target slot's endpoint is plausible — the env file yields a
   loopback host and an integer port. "Plausible" means *configured*, not
   *live*: the switch does **not** require the target slot's feed process to
   be running. Switching to a not-yet-started candidate slot is legitimate; if
   the target is down the front door answers an honest `502` until it is
   started, which is a separate, visible operator step.
5. Reads the current pointer (recording the previous slot).
6. Writes the new slot to the pointer atomically.
7. Reports exactly what changed (`previous -> new (host:port)`).

It then **stops**. Because the native front door reads the pointer per
request, **no proxy reload is needed**. (If a future deployment used an
external proxy instead, that proxy would need its own reload step here — this
native front door deliberately removes that step.)

**Rollback semantics — stated honestly:**

- Rollback **changes routing only** — it repoints the front door at the
  previously preserved slot.
- Rollback **does not merge state** — blue and green keep separate
  `runs/<slot>` databases and `feed/<slot>` directories.
- Rollback **does not migrate data** between slots.
- Rollback **does not repair a failed slot** — it abandons the failed slot in
  place (preserved for inspection) and serves the known-good one.
- Rollback simply points consumers back to the slot that was already there.

## 6. Troubleshooting — active-slot / endpoint mismatch

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Front door returns `503`, body "no valid active slot" | `config/deploy/active-slot` is missing, empty, or holds an unsafe value | `python -m storytime.frontdoor status`; fix with `scripts/switch-slot.sh <slot>` |
| Front door returns `503`, body "no known feed endpoint" | The pointer names a slot with no `config/deploy/<slot>.env` | Switch to a configured slot, or add the missing slot env file |
| Front door returns `502` | The active slot's feed process is not running | Start it: `scripts/run-slot.sh <slot> serve`; confirm with `python -m storytime.frontdoor status` |
| `run-frontdoor.sh` exits 2, "uv not found" | `uv` is not on `PATH` | Install `uv`; there is no proxy binary to install |
| Switch rejected, "not configured" | Target slot has no deploy env file | Use `blue` / `green`, or add the slot's env file |

The front door **holds no pipeline data**. It is a stateless router: its only
state is the active-slot pointer. Restarting it loses nothing.

## 7. Telemetry — the front door is outside the telemetry path

Pipeline telemetry attribution is **unaffected** by the front door, by
construction:

- StoryTime's OpenTelemetry spans and metrics are emitted by the **pipeline
  process** — one per slot — carrying that slot's `deployment.slot` /
  `deployment.environment` on the OTel `Resource`.
- The front door fronts **feed-serving HTTP traffic** (`storytime serve`),
  which is not on the pipeline-telemetry path and emits no pipeline spans.
- A switch changes which slot's *feed* is served; it changes nothing about
  which slot's *pipeline* emitted which span. `deployment.slot` stays correct
  regardless of where the front door points.

The front door imports no `opentelemetry` (enforced by the import-linter
contract) and is intentionally not instrumented. Request-level proxy
telemetry — treating front-door accesses as spans — would be a separate future
phase. See `docs/telemetry-map.md`.

## 8. Limitations and what stays deferred

Option B is higher-assurance than Option A but still deliberately bounded:

- **Demo-grade, loopback-only.** No TLS, no auth — the front door binds
  `127.0.0.1` only and is for the local operator.
- **Operator-initiated.** The switch is *scripted* but not *automatic*: there
  is no health-gated or continuous promotion. That is intentional Option B1
  scope.
- **Single host, single front-door process.** No multi-host topology, no HA of
  the front door itself.
- **No app container / image.** The deployment unit remains an uncontainerized
  per-slot process (Architecture Baseline §16). Future containerization would
  require an explicit baseline amendment — see that section's Phase 7B note.
- **Deferred to later phases:** automated/health-gated promotion, production
  auth, multi-tenant isolation, active alerting and error-budget policy,
  vendor telemetry fan-out, and any cloud/Kubernetes/Terraform path.

## 9. Constraints preserved

Phase 7B keeps every earlier guarantee intact:

- **Local-first.** No slot and no front door are required; with neither, the
  layout and behaviour are exactly as before.
- **Phase 7A separation untouched.** `runs/blue` / `runs/green`,
  `feed/blue` / `feed/green`, and the `STORYTIME_RUNS_DIR` /
  `STORYTIME_FEED_DIR` override semantics are unchanged. The front door never
  merges or mutates slot state.
- **`NoopTelemetry` is the default**; `OTelTelemetry` is opt-in; the
  one-module OpenTelemetry import boundary is unchanged.
- **The test suite needs no Docker, no cloud, and no external proxy binary.**
- The Phase 6 dashboards, demo harness, and feed format are untouched.

See `docs/deployment-bluegreen-option-a.md` for the Phase 7A foundation,
`docs/runbook.md` §6 for the operator-facing front-door procedures, and
`docs/telemetry-map.md` for the telemetry-path detail.
