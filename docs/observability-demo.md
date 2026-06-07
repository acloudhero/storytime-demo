# Observability Demo Walkthrough
<!-- CANONICAL-WALKTHROUGH-POINTER: docs/demo-walkthrough.md -->
> **Canonical demo path.** For the current, authoritative reviewer/demo
> walkthrough — the system modes and boundaries, the optional loopback
> local bridge, the one controlled retry (acceptance is not success), the
> manual snapshot reload (a read-model refresh, not a live sync), and the
> governed mock-first TTS proof (provider-backed audio remains deferred) —
> see [docs/demo-walkthrough.md](demo-walkthrough.md), the single source of
> truth and evidence map. This document is a secondary/historical narrative;
> where it differs, the canonical walkthrough wins.


An end-to-end walkthrough of StoryTime's local observability demo: bring up the
stack, generate real telemetry by running real pipeline scenarios, and read the
result in Grafana and Jaeger.

> **Demo-grade and local-only.** Everything here runs on one machine, loopback
> only. Nothing is network-exposed, nothing is deployed to a cloud, and there
> is no alerting. This walkthrough shows an *observability-native pipeline*, not
> a production service. See `docs/slo-sli.md` for what the telemetry can and
> cannot tell you.

Companion docs: `docs/dashboard-guide.md` (per-panel reading),
`docs/runbook.md` (operator procedures), `docs/slo-sli.md` (the SLI model),
`docs/telemetry-map.md` (the telemetry architecture).

## 0. Prerequisites

`uv run storytime doctor` reports all of these:

- Python ≥ 3.11 and `uv`.
- Docker + Compose — for the observability stack only; the StoryTime app itself
  is never containerized (Architecture Baseline §16).
- ffmpeg — required for the MP3 `assemble` stage, so for a full demo run.

## 1. What the stack is

`docker-compose.observability.yml` brings up five loopback-bound containers:

| Service | Role | Local URL |
|---------|------|-----------|
| OpenTelemetry Collector | receives OTLP from StoryTime; fans traces to Jaeger, metrics to Prometheus; tails the demo log file and routes logs to Loki | OTLP on 4317/4318 |
| Jaeger | trace storage + UI | http://127.0.0.1:16686 |
| Prometheus | metric storage; scrapes the collector | http://127.0.0.1:9090 |
| Loki | log storage (Phase 8B) | http://127.0.0.1:3100 |
| Grafana | dashboards over Prometheus + Jaeger; Explore over Loki | http://127.0.0.1:3000 |

The data paths:

- traces: `storytime` → OTLP/HTTP → Collector → Jaeger
- metrics: `storytime` → OTLP/HTTP → Collector → Prometheus
- logs (Phase 8B): demo log file → Collector `filelog` receiver → (standard
  OTLP/HTTP) → Loki

All three converge in Grafana. Logs reach the Collector as a **mounted file**,
never via Python OTLP log export (Architecture Baseline §23.9).

## 2. Bring up the stack

First create the local log directory, **then** start the stack:

```sh
mkdir -p logs    # preflight — see note below
docker compose -f docker-compose.observability.yml up -d
```

> **Preflight — create `./logs` first.** `docker-compose.observability.yml`
> bind-mounts `./logs` into the Collector for the `filelog` receiver. If the
> directory does not exist when `docker compose up` runs, Docker creates it
> for you — but on some systems as a **root-owned** directory, after which the
> local (non-root) `python -m storytime.demo --log-dir logs` cannot write
> `logs/storytime-demo.log` and Loki stays empty. Running `mkdir -p logs`
> first creates it owned by your user. `make observability-up` and `make demo`
> do this preflight automatically.

Grafana provisions itself from `config/grafana/` on startup — the Prometheus,
Jaeger, and Loki datasources and all six dashboards appear automatically in a
"StoryTime" folder, with no UI clicking and no login (anonymous admin is
enabled, safe only because every port is loopback-bound).

First run on a machine: `docker compose -f docker-compose.observability.yml
pull` fetches and verifies the pinned image tags (tracked as OI-3 for the
collector/Jaeger/Prometheus/Grafana images and OI-21 for the Loki image).

The `make` shortcuts wrap these steps with the preflight built in:

```sh
make observability-up      # mkdir -p logs, then docker compose up -d
make demo                  # mkdir -p logs, then the demo with --log-dir logs
make observability-down    # docker compose down
```

## 3. Generate telemetry — the demo harness

```sh
python -m storytime.demo --log-dir logs
```

`python -m storytime.demo` (module `storytime.demo`) runs **real** StoryTime
pipeline scenarios against a local workspace (`./demo-data` by default) with
the OpenTelemetry adapter enabled. It is a telemetry *generator*: it drives the
real pipeline entry points and lets the instrumented code emit genuine spans
and metrics. It never fabricates telemetry, and it only ever writes inside its
workspace directory.

`--log-dir logs` (Phase 8B) additionally writes a structured JSON-lines log
file (`logs/storytime-demo.log`) — one control-plane record per scenario plus
a run summary. `docker-compose.observability.yml` mounts `./logs` read-only
into the Collector, whose `filelog` receiver tails it and routes the lines to
Loki. Without `--log-dir` no log file is written.

Useful flags:

```sh
python -m storytime.demo --workspace /tmp/storytime-demo
python -m storytime.demo --scenario success --scenario text_rejection
python -m storytime.demo --telemetry noop      # run scenarios, emit nothing
python -m storytime.demo --log-dir logs        # also write logs for Loki
```

`--telemetry noop` runs the identical scenarios with telemetry off — the mode
the test suite uses, requiring no Docker.

> If you run with the default `otel` telemetry but the collector is **not** up,
> the demo prints transient `Connection refused` warnings and drops the
> telemetry. The pipeline still completes (export is non-blocking by design).
> For a useful demo, bring the stack up *first*.

## 4. The scenarios, and what to observe

The harness runs eight scenarios. Each one exercises a real pipeline path; the
table says what genuine telemetry it produces.

### 4.1 `success` — straight-through run

A run with no approval gates: `ingest → synthesize → assemble → publish`.

- **Dashboards:** *Pipeline Overview* — `Pipeline runs` and `Stages completed`
  increment; `Stages failed` and `Artifact validation failures` stay at zero.
  *Stage Duration* — one execution recorded per stage.
- **Trace:** in Jaeger, one `pipeline.run` span with four child
  `pipeline.stage.<name>` spans (`ingest`, `synthesize`, `assemble`,
  `publish`).

### 4.2 `text_approval` / `audio_approval` — pause, approve, resume

A run pauses at an approval gate, an operator approves, and the run resumes to
completion. `text_approval` uses the gate after `ingest`; `audio_approval` uses
the gate after `synthesize`.

- **Dashboards:** *Approval & Resume Behavior* — `Approvals recorded` and
  `Approved` increment; `Resume attempts` increments. *Run Timeline* — you will
  see an `awaiting_approval` terminal status as well as a `succeeded` one,
  because the pause and the resume are **two** measured invocations.
- **Trace:** **two** traces. The first ends at the gate (`awaiting_approval`).
  The resume is a *new* trace carrying a W3C `Link` back to the first — never
  one pretend-uninterrupted span across the human pause. Both traces share the
  same `pipeline.run_id` attribute.

### 4.3 `text_rejection` / `audio_rejection` — pause, reject

A run pauses at a gate and the operator rejects it. The rejection is terminal:
the run moves to `failed` at the moment the decision is recorded; there is no
resume (a failed run is not resumable).

- **Dashboards:** *Approval & Resume Behavior* — `Rejected` increments.
  *Failure & Rejection Behavior* — `Rejected approvals` increments, and
  `Rejection rate by gate` shows which gate. Note this is **not** a stage
  failure — `Stage failures` does not move. A rejection is the pipeline working
  correctly.
- **Trace:** one trace ending at the gate.

### 4.4 `bad_manifest` — rejected at pre-flight

A schema-invalid manifest is rejected before a run is ever created.

- **Dashboards:** little to no movement — no run was created, so no run/stage
  metrics. This scenario demonstrates that invalid input is refused early.
- **Trace:** none (no run started).

### 4.5 `artifact_validation_failure` — tampered artifact, refused on resume

The harness runs a gated run, **tampers with a persisted artifact payload** on
disk, then resumes. Rehydration hash-verifies every artifact it would reuse,
detects the mismatch, and the resumed run correctly **refuses** to continue
(`RehydrationError`).

- **Dashboards:** *Artifact Validation Failures* — `Total validation failures`
  goes to 1+, and `Validation failures by reason` shows `hash_mismatch`. This
  is the one scenario that deliberately makes that dashboard non-zero.
- **Trace:** the resume trace shows the rehydration failing rather than
  building on bad state.

### 4.6 `ffmpeg_missing` — honest skip

Reported as **skipped by design**. Removing ffmpeg from PATH process-wide is
unsafe to script, and a fake failing encoder would not be real telemetry. To
see a genuine ffmpeg-missing failure, run the demo on a host without ffmpeg
installed.

## 5. Interpreting the dashboards

Open Grafana (http://127.0.0.1:3000) → "StoryTime" folder. After a full demo
run you should see, roughly:

- **Pipeline Overview** — runs and stage-completions climbed; a small number of
  stage failures and one artifact-validation failure (from the deliberate
  scenarios); approvals and resumes non-zero.
- **Stage Duration** — p50/p95 per stage; `assemble` (ffmpeg) is typically the
  slowest. Quantiles need several runs in the 5-minute window to stabilise.
- **Approval & Resume Behavior** — approvals split across `text`/`audio` gates
  and `approved`/`rejected` decisions; resume attempts non-zero.
- **Failure & Rejection Behavior** — rejections present (expected); stage
  failures low. The dashboard deliberately separates the two: a rejection is
  healthy, a stage failure is a defect.
- **Artifact Validation Failures** — one `hash_mismatch`, from the
  `artifact_validation_failure` scenario; otherwise zero.
- **Run Timeline** — run durations by terminal status; remember this measures
  active span time per invocation, not human-inclusive wall-clock.

`docs/dashboard-guide.md` covers every panel in detail.

## 6. Interpreting the traces

Open Jaeger (http://127.0.0.1:16686), service `storytime`:

- A simple run is one `pipeline.run` span with `pipeline.stage.<name>` children.
- A gated run that paused is a `pipeline.run` span ending `awaiting_approval`.
- A resume is a separate `pipeline.resume` span carrying a W3C `Link` to the
  pre-pause trace — follow the link to see the whole story across the pause.
- Every span carries `pipeline.run_id`; search by it to find all traces for one
  run. A failed stage span carries `error.kind` and a path-redacted
  `error.message`.

This is the **dashboard → trace → SQLite** drill-down: the dashboard shows
aggregate health, the trace shows one run's causal story, and SQLite (queried
by `pipeline_run_id`) is the authoritative record. See `docs/slo-sli.md` §6.

## 6b. Interpreting the logs (Phase 8B)

If you ran the demo with `--log-dir logs`, the demo log lines are in Loki.
Open Grafana (http://127.0.0.1:3000) → **Explore** → the **Loki** datasource:

- Query `{service_name="storytime"}` to see every demo log line.
- Each line is one JSON object: a `demo.scenario` record (scenario name,
  `pipeline.run_id`, expected vs actual status) or a `demo.summary` record.
- Filter by level — failed scenarios are logged at `error`.

The log lines carry control-plane metadata only (scenario, run id, status) —
never story text, narration, or RSS payloads (Architecture Baseline §23.8).
Logs are the demo's *narrative* surface; traces are its *causal* surface;
SQLite remains the authoritative record. Phase 8B adds no logs dashboard — log
exploration is done in Grafana Explore against Loki.

## 6c. Optional vendor export (Phase 8C)

Everything above is local-only. Phase 8C adds optional, disabled-by-default
export to external backends (Dynatrace, New Relic) through the Collector. It is
off unless you explicitly add one vendor override compose file:

```sh
docker compose -f docker-compose.observability.yml \
               -f docker-compose.vendor.dynatrace.yml up -d
```

(or `-f docker-compose.vendor.newrelic.yml` for New Relic). The two vendor
overrides are mutually exclusive — bring the stack up with at most one. Without
any override the stack stays exactly as described in this walkthrough and makes
no vendor network call. To enable a vendor profile, see
`docs/vendor-export-profiles.md` — it covers the secrets file, the per-vendor
settings, and the drop-not-crash resiliency.

## 7. Known limitations

- **No serving, TTS, or RSS metrics.** The dashboards cover pipeline execution
  only. Phase 6S serving and the TTS/RSS domains have no instruments, so there
  are deliberately no dashboards for them (see `docs/slo-sli.md` §4).
- **Logs come from the demo harness.** Phase 8B routes the demo harness's
  structured log file to Loki; the StoryTime application core still has no
  parallel logging system (Architecture Baseline §23.9). Without `--log-dir`
  no log file is written and Loki stays empty.
- **Counters are process-lifetime.** Restarting StoryTime, or a fresh
  Prometheus, resets the baseline.
- **Quantile/rate panels need traffic.** A single run is not enough for a
  stable p95; run the demo a few times.
- **`otel` mode is noisy without a collector.** Transient connection-refused
  warnings are expected and harmless when the stack is down.
- **Image tags are pinned but were unverified** in the build environment
  (OI-3 for the collector/Jaeger/Prometheus/Grafana images, OI-21 for Loki) —
  `docker compose ... pull` verifies them.
- **No alerting, no cloud, no production claim.** This is a demonstration of
  observability-native design, nothing more.

## 8. Tear down

```sh
docker compose -f docker-compose.observability.yml down
```

The demo workspace (`./demo-data`) is just files — delete it when finished. The
StoryTime SQLite state under `runs/` is independent of the observability stack
and is never required for the demo to be torn down cleanly.
