# Optional Vendor Export Profiles (Phase 8C)

How to fan StoryTime telemetry out to an external observability backend —
**optionally**, **locally configured**, and **disabled by default**.

> Read `docs/telemetry-map.md` and `docs/observability-demo.md` first. This
> document only adds the optional vendor leg on top of the local Phase 8B
> stack (OpenTelemetry Collector + Prometheus + Loki + Jaeger + Grafana). It
> changes nothing about how StoryTime itself behaves.

## 1. What Phase 8C is — and is not

Phase 8C adds disabled-by-default vendor export profiles for Dynatrace and New
Relic. They are configuration and documentation only.

What it **is**: two independent, mutually exclusive override compose files —
`docker-compose.vendor.dynatrace.yml` and `docker-compose.vendor.newrelic.yml`
— each paired with an example vendor Collector config under `config/vendor/`.
Each exports over standard OTLP/HTTP from the Collector — the same protocol the
local stack already uses.

What it is **not** (Architecture Baseline section 23.3, 23.14): not a change to
StoryTime application behaviour (no `src/` file, no `pyproject.toml`
dependency, and no application test changed); no vendor SDK or agent anywhere;
not cloud deployment, Kubernetes, or production wiring; and not Datadog —
Datadog is deferred (23.11), as it would need a proprietary exporter that 23.4
forbids without a new amendment.

The StoryTime app still emits one OTLP stream to one local Collector. The
Collector — and only the Collector — decides whether copies of that stream are
also sent to a vendor (Architecture Baseline 23.2).

## 2. The topology

```text
StoryTime app
  -> local OpenTelemetry Collector
       -> Jaeger        (traces, local)
       -> Prometheus    (metrics, local)
       -> Loki          (logs, local)
       -> Dynatrace     (OTLP/HTTP, optional - off by default)   } pick at most
       -> New Relic     (OTLP/HTTP, optional - off by default)   } one
```

The vendor leg is an additional exporter. The local legs are unchanged and
independent: if the vendor endpoint is down, the local stack and the app are
unaffected (section 6).

## 3. Disabled by default — how

The default stack is brought up with one file and routes locally only:

```sh
docker compose -f docker-compose.observability.yml up -d
```

That uses `config/otel-collector.yaml`, which contains no vendor exporter at
all. Nothing to misconfigure; no outbound vendor call is possible.

Vendor export is reached only by adding an explicit second file — exactly one
of the two vendor overrides:

```sh
# Dynatrace:
docker compose -f docker-compose.observability.yml \
               -f docker-compose.vendor.dynatrace.yml up -d

# or New Relic:
docker compose -f docker-compose.observability.yml \
               -f docker-compose.vendor.newrelic.yml up -d
```

Each override swaps the Collector onto its single-vendor config under
`config/vendor/` (the local config plus that one vendor profile). No override
file means no vendor config means no vendor exporter on any pipeline
(Architecture Baseline 23.6, 23.10).

## 4. The two profiles are independent — and mutually exclusive

Phase 8C ships **two independent vendor profiles**. Each is activated on its
own: a user with only Dynatrace credentials uses only the Dynatrace override
and never has to touch New Relic, and vice versa. This is the point of the
split — no profile depends on the other, and no file editing is needed to
turn one off.

The two overrides are **mutually exclusive**: bring the stack up with **at most
one** of them. This is a real constraint, not a style preference. A single
Collector process reads a single resolved configuration file, and Docker
Compose replaces (does not merge) the `command:` field across override files —
the last `-f` wins. So passing both vendor overrides on one command line does
**not** produce a two-vendor pipeline; it silently activates only whichever
override appears last. Pick exactly one vendor per stack bring-up.

Running a governed demo against both vendors is done sequentially — bring the
stack up with one override, observe, `down`, then bring it up with the other.
Simultaneous dual-vendor export is intentionally outside the Phase 8C profile
set; an operator who genuinely needs it would have to author a single combined
Collector config by hand (copying both `otlphttp/...` exporter blocks and
adding both names to the three pipeline `exporters` lists), which is a
deliberate, unsupported, off-roadmap step.

## 5. Enabling a vendor profile

### 5.1 Create the secrets file

Vendor endpoints and tokens are secrets, so they live in a git-ignored file —
never in `.env`, never in any committed file (23.7):

```sh
cp config/vendor.secret.env.example config/vendor.secret.env
# then edit config/vendor.secret.env with your real values
```

`config/vendor.secret.env` matches the `*.secret.env` pattern in `.gitignore`
and `.dockerignore`, so it can never be committed or baked into an image. The
committed `config/vendor.secret.env.example` holds only obvious placeholders.
One template serves both profiles: fill in only the section for the vendor you
are activating — the other vendor's placeholders are simply never read.

### 5.2 Dynatrace profile

In `config/vendor.secret.env` set `DYNATRACE_OTLP_ENDPOINT` (your Dynatrace
environment's OTLP/HTTP ingest URL, ending in `/api/v2/otlp`) and
`DYNATRACE_API_TOKEN` (an API token with OTLP ingest scopes). The Collector's
`otlphttp/dynatrace` exporter — defined in
`config/vendor/otel-collector.dynatrace.example.yaml` — sends standard
OTLP/HTTP with an `Authorization: Api-Token <token>` header — a generic
`otlphttp` exporter, not a proprietary one (23.4). Bring it up with:

```sh
mkdir -p logs    # see docs/observability-demo.md preflight
docker compose -f docker-compose.observability.yml \
               -f docker-compose.vendor.dynatrace.yml up -d
python -m storytime.demo --log-dir logs
```

### 5.3 New Relic profile

In `config/vendor.secret.env` set `NEWRELIC_OTLP_ENDPOINT` (the New Relic
OTLP/HTTP ingest endpoint for your region) and `NEWRELIC_LICENSE_KEY` (your
license/ingest key). The Collector's `otlphttp/newrelic` exporter — defined in
`config/vendor/otel-collector.newrelic.example.yaml` — sends standard OTLP/HTTP
with an `api-key: <license key>` header. Bring it up with:

```sh
mkdir -p logs    # see docs/observability-demo.md preflight
docker compose -f docker-compose.observability.yml \
               -f docker-compose.vendor.newrelic.yml up -d
python -m storytime.demo --log-dir logs
```

Telemetry now appears in the local Grafana/Jaeger and in the configured vendor
backend.

## 6. Secret safety

- No real endpoint, token, tenant ID, account ID, or license key appears
  anywhere in this repository. `config/vendor.secret.env.example` uses obvious
  `REPLACE-WITH-YOUR-...` placeholders and `.invalid` hostnames (RFC 2606
  reserved, non-routable).
- Both `config/vendor/otel-collector.dynatrace.example.yaml` and
  `config/vendor/otel-collector.newrelic.example.yaml` reference every vendor
  value as `${env:...}` — they embed no literal secret or endpoint.
- The real `config/vendor.secret.env` is git-ignored and docker-ignored.
- A static test (`tests/test_vendor_export_profiles.py`) enforces all of this.

## 7. Resiliency — a vendor outage cannot break StoryTime

Architecture Baseline 23.10 requires that vendor-endpoint failure never affect
local execution. Each vendor config implements this: every pipeline runs
`memory_limiter` first and `batch`; the vendor exporter has a bounded
`retry_on_failure` (`max_elapsed_time: 60s`) and a `sending_queue`, so a
failing batch is retried briefly then dropped; the vendor exporter is an
independent sibling of the local exporters, so the vendor being unreachable
does not stop traces reaching Jaeger, metrics reaching Prometheus, or logs
reaching Loki; and the StoryTime app only ever talks to the local Collector,
which is unaffected by the vendor leg. Failure mode is drop-not-crash. Removing
the vendor override from the command returns the stack to local-only with zero
vendor exporters.

## 8. Governance

Phase 8C is governed entirely by the locked Architecture Baseline Section 23
(Collector-Owned Multi-Backend Telemetry Fan-Out): collector-owned fan-out
(23.2); no vendor SDKs in app code (23.3); standard otlp/otlphttp only, no
proprietary or Datadog exporter (23.4); the outbound exception is narrow and
the app/tests stay offline (23.5); disabled-by-default profiles (23.6);
environment-only secrets (23.7); control-plane-only telemetry (23.8); Collector
resiliency (23.10); backend priority Dynatrace then New Relic, Datadog deferred
(23.11). Phase 8C is the third and final Phase 8 sub-phase (23.13). The
Phase 8C.1 cleanup split the original single combined override into the two
independent, mutually exclusive profiles documented here.
