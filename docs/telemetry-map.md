# Telemetry Map

OpenTelemetry is a **view** over local truth, never the source of truth. The
durable record of a run is SQLite (`event_log`, `pipeline_run`,
`stage_execution`, `stage_artifact`, `approval`) plus the artifact envelopes.
The durable correlation key is `pipeline_run_id`; `trace_id` is an *ephemeral
view identifier* and is never used as durable identity.

Deleting `storytime.adapters.telemetry.otel` and running on `NoopTelemetry`
leaves every functional test green. `NoopTelemetry` is the default adapter; a
default deployment never imports `opentelemetry` at all.

## Import boundary

`opentelemetry` is imported in exactly one module —
`storytime.adapters.telemetry.otel`. The import-linter contract "OpenTelemetry
is confined to the telemetry adapter" enforces this for every other module
(now including `storytime.config` and `storytime.doctor`), and
`tests/test_import_boundaries.py` AST-scans `src` as a second check. Handles
(`RunHandle`, `StageHandle`) carry only plain strings — a `traceparent`, a
`trace_id` — never a live `Span` or `SpanContext`.

## Span structure

A run is **one** span. A sequence opens it once and closes it once; every
stage is a child span.

- `pipeline.run` — one span per fresh run (`run_sequence`), or one span per
  standalone `execute_stage`.
- `pipeline.resume` — one span per resumed run (`resume_sequence`). It is a
  **new trace** carrying a W3C **Link** back to the pre-pause trace — never a
  pretend-uninterrupted span across an approval pause that may last days.
  - `pipeline.stage.<name>` — one child span per stage execution.

### Span attributes

| Attribute | On | Meaning |
|-----------|----|---------|
| `pipeline.run_id` | every span | durable correlation key (unbounded — spans only, never a metric label) |
| `pipeline.stage` | stage spans | stage name (closed set) |
| `pipeline.status` | run + stage spans | terminal status (`succeeded` / `failed` / `awaiting_approval`) |
| `pipeline.resume` | run spans | `true` for a resumed run, `false` otherwise |
| `artifact.kind` / `artifact.version` / `artifact.hash_present` | stage spans | stage-contributed via `StageResult.span_attributes` |
| `tts.adapter` / `audio.format` / `rss.item_count` | stage spans | stage-contributed via `StageResult.span_attributes` |
| `error.kind` / `error.message` | failed stage spans | `error.message` is sanitised (see Data hygiene) |

Resource attributes — `service.name`, `service.version`,
`deployment.environment`, `deployment.slot` — are set once on the OTel
`Resource` from immutable config. `deployment.slot` is omitted when empty.
Phase 7A (blue/green Option A) drives `deployment.environment` and
`deployment.slot` from a real per-slot deployment, so a `blue` and a `green`
process are told apart in Jaeger and Prometheus by resource attribute alone —
with no per-span or per-metric label, hence no added cardinality. See
`docs/deployment-bluegreen-option-a.md` §5.

## Traceparent propagation

After a stage's span is started, the runner stamps that span's own
`traceparent` into the `StageInput`, and the stage writes it into the
`trace_context` of every artifact envelope it produces. The next stage's
`StageInput.inbound_traceparent` is the previous stage's span traceparent.
Under `NoopTelemetry` every `traceparent` is `None` and the same code path
runs unchanged. The W3C string helpers live in
`storytime.adapters.telemetry.propagation` (OTel-free).

## Approval / resume linked traces

A run that pauses at an approval gate ends its process. When it resumes:

1. `build_resume_plan` reads `prior_traceparent` from the last completed
   stage's artifact envelope `trace_context`.
2. `resume_sequence` opens its `pipeline.resume` span with a W3C `Link` to
   that prior trace.
3. The `approval` row records both anchors: `inbound_trace_id` (the pre-gate
   trace, written by `apply_approval_decision`) and `outbound_trace_id` (the
   resumed run's trace, written once by the first resume that crosses the
   gate). `stage_execution.parent_trace_id` records the run-span → stage-span
   hierarchy.

This closes OI-2. Both non-approval continuation (regime 2) and the approval
boundary (regime 3) use the same honest model: **new trace + Link to prior**.

## Event → span-event mapping

Each `PipelineEvent` persisted to `event_log` is also added as a span event on
the active stage span (`TelemetryAdapter.on_event`). Persistence to SQLite
always happens **before** telemetry emission — telemetry never gates a write.

The Phase 9B governance gate adds one event type, `GovernanceEvaluated`,
emitted by the `ingest` stage when it derives a run's Trust Envelope. Its
payload carries only bounded status metadata — the governance `decision`, the
`license_type`, and the `source_ref` — and never the raw source text, the
operator's review summary, free-text notes, or any secret. This keeps the
governance event inside the same hygiene posture as every other event and
satisfies the Architecture Baseline §24.12 telemetry/privacy rule for
governance signals.

## Metrics

A small, closed instrument set (`storytime.adapters.telemetry.metrics`); an
unknown metric name is ignored so a typo cannot create an unbounded
instrument. Labels are deliberately low-cardinality; `pipeline_run_id` is
never a metric label.

| Metric | Kind | Labels |
|--------|------|--------|
| `pipeline_runs_total` | counter | `mode` (`run`/`resume`/`stage`) |
| `pipeline_stage_completed_total` | counter | `pipeline.stage` |
| `pipeline_stage_failed_total` | counter | `pipeline.stage` |
| `pipeline_approvals_total` | counter | `gate`, `decision` |
| `pipeline_resume_total` | counter | — |
| `pipeline_artifact_validation_failed_total` | counter | `reason` (closed set) |
| `pipeline_stage_duration_seconds` | histogram | `pipeline.stage` |
| `pipeline_run_duration_seconds` | histogram | `pipeline.status` |

## Data hygiene

`storytime.adapters.telemetry.hygiene` is the single sanitisation choke point:
it redacts absolute POSIX/Windows filesystem paths to `<path>` and bounds
every string to 256 characters. The OTel adapter routes `error.message`, all
span/stage attributes, and span-event payload values through it. Span-event
payloads are further restricted to a known-safe key set. Raw story text, full
manifests, and secrets are never put into events in the first place — hygiene
is the backstop, not the primary control.

## Structured logging

The StoryTime **application core** still has no parallel logging system:
`event_log` (durable) and spans (the view) remain the two authoritative
observability surfaces for the pipeline, and the runner, stages, and adapters
emit neither application log records nor Python OTLP logs. Adding in-app OTLP
log export was deliberately **not** done — Architecture Baseline §23.9 forbids
rewriting StoryTime's logging around direct OTLP log export in Phase 8.

Phase 8B adds **local log routing for the observability demo**, following the
§23.9 model "the application writes structured logs to stdout/files; local
infrastructure routes them." The observability **demo harness**
(`python -m storytime.demo --log-dir <dir>`) writes a structured JSON-lines
log file (`storytime.demo.logsink`) — one control-plane record per scenario
plus a run summary. This is plain structured *file* logging: no
`opentelemetry` import, no network call. The OpenTelemetry Collector's
`filelog` receiver tails that file and forwards the lines to Loki; Grafana's
Explore view queries Loki. The demo log carries control-plane metadata only
(§23.8) — scenario name, pipeline run id, status — never story text,
narration, or RSS payloads. When `--log-dir` is omitted no file is written, so
default behaviour is unchanged.

## Local backend

The local observability stack is brought up with
`docker-compose.observability.yml` and is a **view layer only** — the StoryTime
test suite never requires it.

Traces: `storytime` → OTLP/HTTP → OpenTelemetry Collector → Jaeger (UI on
http://127.0.0.1:16686).

Metrics (Phase 6A): `storytime` → OTLP/HTTP → OpenTelemetry Collector →
Prometheus → Grafana. Before Phase 6A the collector had only a traces
pipeline, so metric instruments were emitted but landed nowhere; the collector
now has a `metrics` pipeline whose `prometheus` exporter republishes the
instruments on an in-network scrape endpoint. The exporter sets
`add_metric_suffixes: false`, so the Prometheus series carry **exactly** the
names declared above — `pipeline_runs_total`, not `pipeline_runs_total_total`.
The only added series are the intrinsic `_bucket` / `_sum` / `_count` of the
two histograms. Note that Prometheus exposes the dotted OTLP label keys
`pipeline.stage` and `pipeline.status` with an underscore (`pipeline_stage`,
`pipeline_status`); PromQL and the provisioned dashboards use the underscore
form.

Logs (Phase 8B): demo log file → OpenTelemetry Collector `filelog` receiver →
(standard OTLP/HTTP) → Loki → Grafana. The collector gained a `logs` pipeline;
its exporter is the generic `otlphttp` exporter pointed at Loki's native OTLP
ingest endpoint — deliberately not a proprietary `loki` exporter and not a
vendor exporter (§23.4). Logs reach the collector as **mounted files**, never
by Python OTLP log export.

Grafana (UI on http://127.0.0.1:3000) is provisioned entirely as code from
`config/grafana/`: a Prometheus datasource, a Jaeger datasource, a Loki
datasource (Phase 8B), and six dashboards (`config/grafana/dashboards/*.json`)
that chart only the eight real Phase 5 metrics. Logs are read through Grafana's
Explore view against the Loki datasource — Phase 8B adds no logs dashboard, so
the metric-honesty guarantee of the six metric dashboards is untouched.
Nothing is configured by clicking in the UI.

Collector resiliency (Phase 8B, §23.10): every pipeline runs a `memory_limiter`
processor first, and the Jaeger and Loki exporters carry `retry_on_failure`
plus a `sending_queue` — so a backend outage drops data rather than crashing
the collector or stalling a run.

Export is non-blocking: a `BatchSpanProcessor` and a
`PeriodicExportingMetricReader` drop spans/metrics on a collector outage rather
than stalling a run. With the default `noop` adapter no telemetry is emitted
and the pipeline behaves identically.

## Blue/green front door (Phase 7B)

The Phase 7B blue/green front door (`storytime.frontdoor`) is **outside the
pipeline telemetry path**. Pipeline spans and metrics are emitted by each
slot's *pipeline* process and carry that slot's `deployment.slot` /
`deployment.environment` on the OTel `Resource`. The front door fronts only
*feed-serving* HTTP traffic (`storytime serve`), which emits no pipeline
telemetry. Routing feed traffic through the front door, or switching which
slot it serves, therefore does not change any span or metric attribution — the
backend slot's own config remains the sole control of pipeline telemetry. The
front door imports no `opentelemetry` (enforced by the import-linter contract)
and is intentionally not instrumented; request-level proxy telemetry would be
a separate future phase. See `docs/deployment-bluegreen-option-b.md`.

`python -m storytime.demo` (module `storytime.demo`) runs real pipeline
scenarios — a straight-through run, text/audio approval pause-and-resume,
text/audio rejection, a rejected manifest, and an artifact-validation failure —
so the dashboards have genuine telemetry to display. It is a telemetry
*generator*, never a telemetry *source*: it drives the real pipeline entry
points and lets the instrumented code emit the spans and metrics. It is bounded
to a single workspace directory. With `--telemetry noop` it runs the identical
scenarios with telemetry disabled, which is how the test suite exercises it
without Docker. See `docs/observability-demo.md`.

## Containerized slots: identical resource identity (Phase 7C.1 / 7D)

Running a slot as a Docker container (the optional `docker-compose.app.yml`
path) does **not** change its telemetry identity. The OpenTelemetry `Resource`
is built only from StoryTime config — `service.name`, `service.version`,
`deployment.environment`, `deployment.slot`, and `service.instance.id` — and
that config is identical whether the slot runs bare-metal or in a container.

`service.instance.id` is pinned to a stable, slot-derived value
(`storytime-blue` / `storytime-green`), derived only from `deployment.slot`.
It is deliberately **never** a container ID, PID, hostname, IP, random value,
or start timestamp: those churn on every rebuild/restart and would fragment a
slot into many short-lived telemetry entities. Because the value depends only
on the slot, a blue slot reports `storytime-blue` across restarts and across
the bare-metal/container boundary alike.

No automatic Docker/host/process resource detector is enabled, and no
resource-detector package is a dependency. The explicitly-constructed resource
attributes are authoritative: they are merged last, so even a
container-supplied `OTEL_RESOURCE_ATTRIBUTES` value cannot override the pinned
`service.instance.id`. The app owns telemetry identity; the Collector owns
routing and any future (Phase 8) fan-out. See `docs/deployment-containerized.md`.


## Vendor export profiles (Phase 8C, optional, off by default)

Phase 8C adds optional, disabled-by-default vendor export profiles for
Dynatrace and New Relic. They are configuration only — no application code, no
dependency, and no application test changed for Phase 8C.

The default local stack (`docker compose -f docker-compose.observability.yml
up -d`) uses `config/otel-collector.yaml`, which has **no vendor exporter at
all** and makes no outbound vendor call. Vendor export is reached only by
explicitly adding one vendor override compose file:

```text
docker compose -f docker-compose.observability.yml \
               -f docker-compose.vendor.dynatrace.yml up -d
```

(or `-f docker-compose.vendor.newrelic.yml` for New Relic). Each override swaps
the Collector onto its single-vendor config under `config/vendor/` — the local
config plus one `otlphttp` exporter that fans traces, metrics, and logs out to
that vendor **in addition to** the local Jaeger/Prometheus/Loki legs. The two
vendor overrides are mutually exclusive (a single Collector reads one config);
bring the stack up with at most one. Both vendor profiles use the standard
`otlphttp` exporter (Architecture Baseline 23.4); there is no proprietary
exporter and no Datadog exporter (Datadog is deferred, 23.11). Vendor endpoints
and tokens are injected from a git-ignored `config/vendor.secret.env` — no
secret is ever committed (23.6, 23.7).

The vendor leg cannot break StoryTime: each vendor exporter has a bounded
`retry_on_failure` and a `sending_queue`, the vendor exporter is an independent
sibling of the local exporters, and the app only ever talks to the local
Collector. A vendor outage drops that leg's data and nothing else (23.10).
Full detail is in `docs/vendor-export-profiles.md`.
