# Operator Runbook

> **Demo-grade.** These are procedures for running and inspecting the local
> StoryTime observability demo. There is **no** alerting, no on-call rotation,
> and no production incident process — and this runbook does not pretend
> otherwise. It is the practical companion to `docs/observability-demo.md`
> (the walkthrough), `docs/dashboard-guide.md` (panel reading), and
> `docs/slo-sli.md` (the SLI model).

## 1. Prerequisites

| Tool | Why | Check |
|------|-----|-------|
| Python ≥ 3.11 | runs StoryTime | `uv run storytime doctor` |
| `uv` | dependency + venv management | `uv --version` |
| Docker + Compose | the observability stack only (never the app) | `docker compose version` |
| ffmpeg | MP3 assembly; optional for Phase 2, required for a full run | `uv run storytime doctor` |

`storytime doctor` reports each of these. The app runs uncontainerized on the
host; Docker is for Jaeger / Collector / Prometheus / Grafana only.

## 2. Routine procedures

### 2.1 Bring up the observability stack

```sh
mkdir -p logs    # preflight: the Collector bind-mounts ./logs (see note)
docker compose -f docker-compose.observability.yml up -d
```

> **Create `./logs` before `docker compose up`.** The compose file bind-mounts
> `./logs` into the Collector's `filelog` receiver. If the directory is absent,
> Docker may create it root-owned, and the non-root `python -m storytime.demo
> --log-dir logs` then cannot write its log file. `mkdir -p logs` first (or
> `make observability-up`, which does it for you) avoids this.

Grafana self-provisions datasources (Prometheus, Jaeger, Loki) and all six
dashboards from `config/grafana/`. First time on a machine, run
`docker compose -f docker-compose.observability.yml pull` to fetch and verify
the pinned image tags (tracked as OI-3, and OI-21 for the Loki image).

### 2.2 Generate telemetry

```sh
mkdir -p logs                                         # preflight (or: make demo)
python -m storytime.demo --log-dir logs               # all scenarios, otel + logs
python -m storytime.demo --telemetry noop             # same scenarios, no telemetry
python -m storytime.demo --scenario success           # one scenario
```

`--log-dir logs` writes the structured demo log the Collector routes to Loki;
without it no log file is written. `make demo` runs the first form with the
`./logs` preflight built in.

### 2.3 Optional — enable vendor export (Phase 8C)

Vendor export (Dynatrace / New Relic) is **disabled by default**. To enable it,
add exactly one vendor override compose file:

```sh
cp config/vendor.secret.env.example config/vendor.secret.env   # then edit it
docker compose -f docker-compose.observability.yml \
               -f docker-compose.vendor.dynatrace.yml up -d
```

(or `-f docker-compose.vendor.newrelic.yml` for New Relic). The two vendor
overrides are **mutually exclusive** — bring the stack up with at most one. The
override fans telemetry out to that vendor over standard OTLP/HTTP, in addition
to the local stack. `config/vendor.secret.env` is git-ignored — never commit
it. Bringing the stack up **without** a vendor override returns it to
local-only with no vendor exporter. A vendor outage never affects the local
stack or the app. Full detail: `docs/vendor-export-profiles.md`.

### 2.4 Tear down

```sh
docker compose -f docker-compose.observability.yml down
```

The demo workspace (`./demo-data`) is plain files; delete it freely.

### 2.4 Run the verification gates

```sh
uv sync --frozen --extra dev
uv run pytest -q
uv run ruff check .
uv run mypy
uv run lint-imports
uv run storytime doctor
```

## 3. Investigation procedures

The recurring move is **dashboard → trace → SQLite**: a dashboard says
*something* is wrong in aggregate; a trace says *which run*; SQLite is the
authoritative record. `pipeline_run_id` ties all three together.

### 3.1 Dashboards are empty

Symptom: Grafana panels show "No data".

1. Is the stack up? `docker compose -f docker-compose.observability.yml ps`.
2. Did the demo run with telemetry on? `--telemetry noop` emits nothing by
   design. Re-run `python -m storytime.demo` (default is `otel`).
3. Is Prometheus scraping the collector? Open http://127.0.0.1:9090/targets —
   the `storytime-otel-collector` target should be `UP`.
4. Give it time: `rate(...)` panels need data inside the 5-minute window.
5. Was the collector reachable when the demo ran? If the demo printed
   transient `Connection refused` warnings, telemetry was dropped — bring the
   stack up *first*, then re-run the demo.

### 3.2 A run failed (stage failure)

Symptom: "Failure & Rejection Behavior" → *Stage failures* is non-zero.

1. Confirm it is a real failure, not a rejection — rejections appear in
   *Rejected approvals*, not *Stage failures* (see `docs/dashboard-guide.md`
   §4). A rejection is expected behaviour.
2. Find the run: in Jaeger, open the failing `pipeline.stage.<name>` span; its
   `error.kind` and `error.message` attributes describe the failure (the
   message is path-redacted by the hygiene layer).
3. Note the `pipeline.run_id` from the span.
4. For the authoritative record, query SQLite by that `pipeline_run_id`: the
   `stage_execution` row's status, and the `event_log` rows, are the source of
   truth.
5. `uv run storytime doctor` — a missing ffmpeg is a common cause of an
   `assemble`-stage failure.

### 3.3 Artifact validation failure

Symptom: "Artifact Validation Failures" → *Total validation failures* non-zero.

1. If you just ran the demo's `artifact_validation_failure` scenario, this is
   **expected** — that scenario deliberately tampers with a payload to show
   `hash_mismatch`.
2. Otherwise: the `reason` label names the failed check
   (`hash_mismatch`, `envelope_missing`, `payload_missing`,
   `envelope_invalid`, `unsupported_version`, `non_relative_key`,
   `non_relative_payload`).
3. This means a persisted artifact under `runs/<run_id>/` does not match its
   recorded envelope — real on-disk corruption or a defect. A resumed run
   correctly **refuses** to build on it (`RehydrationError`); the run does not
   silently continue.
4. Investigate via the run's trace and its SQLite `stage_artifact` rows. The
   safe recovery for a demo is to start a fresh run; StoryTime does not
   auto-repair artifacts.

### 3.4 A run is stuck "awaiting approval"

This is **not** a fault — it is the approval gate working. The run has paused
and its process has exited cleanly.

```sh
storytime approve <run_id> --stage text  --decision approve   # or audio / reject
storytime run --resume <run_id>
```

A rejected run becomes `failed` and is not resumable — that is by design; start
a new run.

### 3.5 The stack is up but Grafana has no dashboards

Grafana provisioning is file-based. Confirm the compose mounts
`config/grafana/provisioning` and `config/grafana/dashboards` and that the
files are present. Provisioning is read at Grafana startup — restart the
Grafana container after editing provisioning files.

### 3.6 A run failed at the governance gate

If a run fails with error kind `SourceNotApproved` (at `ingest`) or
`GovernanceGateBlocked` (at `synthesize` or `publish`), the Phase 9B
fail-closed governance gate stopped it. This is **not** a fault — it is the
gate working as designed (`docs/architecture-baseline.md` §24.6).

Inspect the governance decision:

```sh
storytime status <run_id>     # shows the governance line: decision + licence
```

The durable Trust Envelope artifact records the full decision and the
operator's rationale:

```sh
cat runs/<run_id>/governance/trust-envelope.json
```

Common decisions and what they mean:

- `BLOCKED` — the source matched an entry in
  `config/governance/blocked-sources.yaml`. The `blocked_reason` names the
  matching pattern. If the block was a mistake, the operator edits that file;
  governance is source authorisation, never a content/topic judgement (§24.5).
- `NEEDS_REVIEW` — the manifest declared a licence StoryTime does not
  recognise as an approved category. A human operator must review the source
  and correct the manifest.
- A **missing or malformed** Trust Envelope also fails the gate closed. The
  durable artifact is the governance source of truth; if it cannot be read and
  verified, the run does not proceed. Re-run from `ingest` to regenerate it.

StoryTime records and enforces a human licensing decision — it does not make
one. It is not legal advice and not a rights-clearance platform (§24.2 / §24.13).

## 4. What this runbook deliberately does not cover

- **Alerting / paging.** There is none. Nobody is notified automatically; an
  operator looks at dashboards. Adding alerting is explicitly out of scope.
- **Production incidents, SEV levels, escalation.** Not applicable to a
  local-first demo.
- **Cloud or vendor-backend operations.** None of that exists; StoryTime is
  local-first. A lean *local* blue/green path (Option A) does exist — see §5
  below — but there is no cloud deployment and no automated traffic cutover.
- **Capacity / scaling.** StoryTime is single-process and local.

If telemetry itself is unavailable (collector down, Grafana down), the
pipeline is unaffected: SQLite remains the complete source of truth and runs
still succeed. Observability is a view, not a dependency — see
`docs/slo-sli.md` §5.

## 5. Blue/green deployment (Option A)

Phase 7A adds a lean, **local** blue/green path. It is demo-shaped: two
`storytime` processes — slots `blue` and `green` — on one host, each with its
own SQLite state, its own feed, and its own loopback port. There is no
container, no orchestrator, and **no automated traffic cutover**. Full design
and rationale: `docs/deployment-bluegreen-option-a.md`.

### 5.1 Run a slot

```sh
scripts/run-slot.sh blue  doctor
scripts/run-slot.sh green doctor
scripts/run-slot.sh blue  run --manifest sources/the-raven.json --auto-approve
scripts/run-slot.sh blue  serve     # serves feed/blue on 127.0.0.1:8000
scripts/run-slot.sh green serve     # serves feed/green on 127.0.0.1:8001
```

The launcher loads `config/deploy/<slot>.env`. Blue and green can run at the
same time: `runs/blue/` vs `runs/green/`, `feed/blue/` vs `feed/green/`,
ports 8000 vs 8001 — nothing is shared.

### 5.2 Confirm which slot you are on

`storytime doctor` opens with a deployment-identity banner: the environment,
the slot, and the exact state/feed roots the process will touch. Always check
it before acting on a slot. Under `STORYTIME_TELEMETRY=otel`, filter Jaeger by
the `deployment.slot` resource attribute to see one slot's traces.

### 5.3 Switch / roll back (operator action)

Option A has no automatic cutover. A "switch" is: bring the target slot up,
verify it (`doctor`, run a pipeline, check `feed/<slot>/feed.xml`), then point
consumers at that slot's port. A "rollback" is pointing them back. Because the
slots have fully separated state, a switch never touches the idle slot — it
stays a valid rollback target. There is no shared database and so no
split-brain risk in Option A.

### 5.4 Investigating a slot

The §3 procedures apply per slot — `pipeline_run_id` still ties dashboard →
trace → SQLite together, and the SQLite to query is that slot's
`runs/<slot>/state.db`. A run only ever exists in its own slot's database.

## 6. Blue/green front door (Option B / Phase 7B)

Phase 7B adds a **stable local front door** in front of the Option A slots: a
native Python, loopback-only reverse proxy on one fixed port (default
`127.0.0.1:8080`). Consumers always use that port; an **active-slot pointer**
(`config/deploy/active-slot`) decides which slot it routes to. The front door
holds **no pipeline data** — it is a stateless router; restarting it loses
nothing. Full design: `docs/deployment-bluegreen-option-b.md`.

### 6.1 Start the front door

```sh
scripts/run-slot.sh blue  serve     # blue feed on 127.0.0.1:8000
scripts/run-slot.sh green serve     # green feed on 127.0.0.1:8001
scripts/run-frontdoor.sh            # front door on 127.0.0.1:8080
```

No external proxy binary is needed — the front door is native Python. The
launcher installs nothing; if `uv` is missing it exits 2 with a clear message.

### 6.2 Check the active slot

```sh
python -m storytime.frontdoor status
```

Prints the pointer path, the active slot, and every configured slot's
endpoint, marking which is active.

### 6.3 Switch procedure

```sh
scripts/run-slot.sh green serve              # 1. bring the candidate slot up
python -m storytime.frontdoor status         # 2. confirm green is configured
scripts/switch-slot.sh green                  # 3. switch the front door
curl -s http://127.0.0.1:8080/ | head        # 4. verify traffic is on green
```

The running front door reads the pointer per request, so step 3 takes effect
immediately — **no proxy reload or restart**.

### 6.4 Rollback procedure

Rollback is the switch in reverse — the same command targeting the previous
slot:

```sh
scripts/switch-slot.sh blue                   # roll back green -> blue
```

Rollback changes **routing only**: it does not merge state, does not migrate
data, and does not repair the failed slot. It points consumers back to the
previously preserved slot. The abandoned slot stays in place for inspection.

### 6.5 Troubleshooting active-slot / endpoint mismatch

| Symptom | Cause | Action |
|---------|-------|--------|
| Front door `503` "no valid active slot" | pointer missing/empty/unsafe | `python -m storytime.frontdoor status`; `scripts/switch-slot.sh <slot>` |
| Front door `503` "no known feed endpoint" | pointer names a slot with no `config/deploy/<slot>.env` | switch to a configured slot, or add the env file |
| Front door `502` | the active slot's feed process is not running | `scripts/run-slot.sh <slot> serve` |
| `run-frontdoor.sh` exits 2 | `uv` not on `PATH` | install `uv` (no proxy binary to install) |
| switch rejected "not configured" | target slot has no deploy env file | use `blue` / `green`, or add the env file |

## 7. Optional containerized blue/green (Phase 7C.1 / 7D)

The blue/green slots can optionally run as local Docker containers instead of
bare-metal processes, under the locked Phase 7C / 7C.1 amendment. This is
**optional and demo-grade** — bare-metal (Section 5) remains the default, and
the verification gates (Section 2.4) need no Docker.

The front door (Section 6) and the active-slot pointer are unchanged: the
front door stays a host process and routing/switch/rollback work exactly as
before, whether the slots are bare-metal or containerized.

### 7.1 Start the containerized slots

```
docker compose -f docker-compose.app.yml config     # validate the compose file
docker compose -f docker-compose.app.yml build      # build storytime-app:local once
docker compose -f docker-compose.app.yml up -d       # start blue + green
docker compose -f docker-compose.app.yml ps          # both should be running
# blue feed on 127.0.0.1:8000, green on 127.0.0.1:8001 — same ports as Section 5
```

On a fresh Docker cache `docker compose -f docker-compose.app.yml up -d` works
on its own — it builds the shared image if it is missing, then starts both
slots. One service owns the image build and the other consumes it, so neither
`build` nor `up -d` needs per-service targeting. A `404` from a slot before a
feed is published is expected — it still proves the feed server is reachable.

Each slot has its own named volumes for SQLite state and feed; ports are
loopback-only. Run a pipeline inside a slot with
`docker compose -f docker-compose.app.yml run --rm storytime-blue run --manifest ...`.

### 7.2 State divergence (read before switching)

Blue and Green slots use strictly isolated state. Switching slots changes
which isolated timeline is served. Switching does not merge, migrate, copy, or
promote SQLite databases or historical run state. This is intentional for the
local/demo-grade blue/green model because rollback safety is prioritized over
automatic state convergence. The front door holds no pipeline data.

### 7.3 Resetting a slot (destructive)

> **Warning.** Removing a slot's named volume permanently deletes that slot's
> local history — SQLite state, run directories, feed/audio. There is no undo.

```
docker compose -f docker-compose.app.yml stop storytime-blue
docker volume rm storytime-app_storytime-blue-state storytime-app_storytime-blue-feed
docker compose -f docker-compose.app.yml up -d storytime-blue
```

### 7.4 Troubleshooting

| Symptom | Cause | Action |
|---------|-------|--------|
| Slot unreachable on `127.0.0.1:800x` | host networking unavailable (Docker Desktop) | run the slot bare-metal (Section 5) — always supported |
| `SQLITE_BUSY` / state corruption | SQLite state on a host bind mount | use the named volumes in `docker-compose.app.yml`; never bind-mount state |
| Slot has no history after recreate | named volume was removed (`down -v` or `volume rm`) | expected — that deletes the slot's timeline; see 7.3 |
| Permission denied writing state | volume ownership mismatch | the image pre-chowns `/app/runs` and `/app/feed`; rebuild the image |

Full design notes: `docs/deployment-containerized.md`.
