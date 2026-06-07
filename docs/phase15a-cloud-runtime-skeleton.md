> **Phase 15A — Cloud Runtime Skeleton (current implementation candidate; pending review; NOT locked).** Phase 14D remains the last locked phase (locked via `storytime-phase14d-cloud-distributed-architecture-baseline.tar.gz`, SHA-256 `a4ccc8aa59beaf6365081973d1c3d78235df028ef0f3214979e9d3b98f4dcce6`). Phase 15 — Cloud / Distributed Runtime — is STARTED, with Phase 15A as the current candidate on top of the LOCKED Phase 14D local contracts. Phase 14E — Local Release Candidate / Full Local Mode Closure — remains NOT STARTED; it was intentionally bypassed for this transition. **Phase 15A is the smallest local-first, cloud-*shaped* runtime skeleton: it names a runtime ROLE separation (`api` / `worker` / `combined`), derives a health / readiness model from configuration, and reads exactly one new environment variable (`STORYTIME_RUNTIME_ROLE`).** It adds a pure-data `storytime.runtime` package and no new dependency. It does not implement an external broker, no distributed worker, no object storage, no authentication, no public ingress, no provider TTS, no audio, and no RSS; it is not a distributed system and does not run in the cloud. Phase 15B, Phase 15C, Phase 15D, and Phase 15E remain NOT STARTED.

# Phase 15A — Cloud Runtime Skeleton

This is the first runtime-shaping step of Phase 15. It is derived directly from the
locked Phase 14D mapping (`docs/phase14d-cloud-distributed-architecture-baseline.md`,
§5 service shape and §11.A), not from a greenfield cloud design. It exists to make
the later cloud decomposition narrower and more obvious — not to build the cloud, and
not to change any proven local behaviour.

The discipline is:

```text
Build local behavior before mapping cloud architecture.   (through Phase 14C)
Map cloud architecture before building cloud behavior.    (Phase 14D, LOCKED)
Name the runtime shape before standing up cloud services. (Phase 15A, here)
```

Phase 15A turns the 14D "future deployable service shape" from prose into a small,
typed, testable vocabulary that the *existing local process* can describe itself with.
A single process can be shaped as an `api`, a `worker`, or a `combined` node, and it
can report — purely from configuration — what it serves, what it drains, and whether
it is ready. Nothing here binds a public socket, opens a broker, or stands up a second
process; the default role reproduces the proven local single-process behaviour exactly.

It builds on, and does not modify, these locked documents:

- `docs/phase14d-cloud-distributed-architecture-baseline.md` — the locked as-built
  mapping (§5 service shape, §6 contract-by-contract mapping, §7 ownership, §11.A the
  recommended Phase 15A skeleton). This remains the authoritative future-architecture
  record; Phase 15A records its *current* status only in the living state docs.
- `docs/phase14d-deferred-cloud-work-register.md` — the deferred cloud work register.
- `docs/phase14-cloud-queue-mapping.md` — the Phase 14C.5.1 cloud-queue / recovery
  mapping contract.

---

## 1. Purpose

Phase 15A answers one narrow question with real, typed code rather than prose:

> How is a single local StoryTime process *shaped* — as an API node, a worker node,
> or both — and how does it report its own readiness, without changing any behaviour?

Concretely, Phase 15A delivers a `storytime.runtime` package that provides:

- a **runtime role vocabulary** (`api` / `worker` / `combined`, default `combined`);
- a **runtime configuration boundary** that derives a `RuntimeConfig` from the
  immutable `StoryTimeConfig` plus exactly one new environment variable; and
- a **configuration-derived health / readiness model** that maps a role to the local
  contracts it depends on and reports `ready` / `status` and a safe summary.

The winning outcome is honest and boring: the project can now *name* the API / worker /
combined runtime shapes that Phase 14D mapped, prove their boundaries with tests, and
derive readiness from configuration — while the running system stays exactly the
local-first, single-process, SQLite-backed proof it already was.

---

## 2. Non-goals

Phase 15A is deliberately the smallest possible step. It is a pure-data module plus
documentation, state records, and guard tests. In particular, Phase 15A:

- does not implement an external broker (no Redis, NATS, SQS, Temporal, Celery, Kafka,
  or RabbitMQ), and does not wrap, proxy, or adapt the existing `WorkQueue`;
- does not implement a distributed worker, replica leasing, or multi-process execution;
- does not implement object storage, no S3, no MinIO, no signed URLs, and no public
  artifact serving;
- does not implement authentication, no API keys, no OAuth, no JWT, and no public
  ingress; the API role keeps the locked loopback-only bind;
- does not implement Kubernetes, Terraform, or Helm, and no cloud deploy mechanics;
- does not implement provider-backed TTS, no audio generation, no audio playback, and
  no RSS publishing;
- does not implement dashboards, SLOs, alerting, distributed tracing, or a collector,
  and does not expand the Phase 14C.4 observer event schema;
- does not implement polling, WebSockets, or EventSource, and changes no frontend;
- adds no new dependency; `uv.lock` and `package*.json` are untouched, and
  `pyproject.toml` changes only to extend the existing import-linter OpenTelemetry
  contract so it also names `storytime.runtime`.

Phase 15A is not a distributed system and does not run in the cloud. It does not import
OpenTelemetry. It changes no backend, frontend, bridge, queue/worker, recovery,
artifact-store, or observation behaviour.

---

## 3. Locked Phase 14D baseline (what this builds on)

Phase 14D mapped each proven LOCAL contract to its future cloud/distributed shape on
paper and was then LOCKED. Phase 15A consumes that mapping unchanged:

- **Service shape (§5).** Phase 14D described a future API service, worker service, and
  durable database. Phase 15A names those as runtime *roles* of one local process,
  rather than standing them up as separate deployables.
- **Ownership (§7).** Durable state, the work queue, artifacts, and recovery lineage are
  backend-owned and never the browser's. Phase 15A's health model reports these as
  backend-owned dependencies and exposes no path, URL, or credential for any of them.
- **Ports.** The `WorkQueue`, `ArtifactStore`, `StorageAdapter`, and
  `QueueWorkerEventSink` boundaries proven through Phase 14C.5.1 remain the integration
  seams. Phase 15A references them by name in its dependency descriptors and
  instantiates none of them.
- **Recovery (§6.E / Phase 14C.5.1).** The durable `recovery_action` lineage table
  remains the backend-owned source of truth, unchanged by this phase.

Phase 14D remains the last locked phase. Phase 15A is a candidate on top of it and is
NOT locked.

---

## 4. Runtime role vocabulary

The vocabulary lives in `storytime.runtime.roles` and is pure data:

- `RuntimeRole` — a `StrEnum` with three members: `API` (`"api"`), `WORKER`
  (`"worker"`), and `COMBINED` (`"combined"`).
- Two declarative properties express the default behaviour of each role:
  - `serves_api_by_default` — true for `API` and `COMBINED`.
  - `runs_worker_loop_by_default` — true for `WORKER` and `COMBINED`.
- `DEFAULT_RUNTIME_ROLE` is `RuntimeRole.COMBINED` — the proven local default.
- `RoleDefinition` is a frozen description (`role`, `title`, `serves_api`,
  `runs_worker_loop`, `summary`); `role_definition(role)` returns it.
- `parse_role(value)` is case-insensitive and raises `ValueError` on an unrecognised
  value, so an unknown role fails fast rather than silently degrading.

The roles describe how a single LOCAL process is *shaped*, not where it runs. They add
no behaviour on their own; they are the shared nouns the rest of the package and the
tests are written against.

---

## 5. The three roles — `api`, `worker`, `combined`

### 5.1 `api`
- **Serves the operator read-model**, on loopback only, and **does not drain the local
  work queue by default** (`runs_worker_loop_by_default` is false).
- Reuses the LOCKED loopback bind guard: readiness checks the API bind host with the
  existing `validate_bind_host`, which accepts only `127.0.0.1` / `localhost` / `::1`.
- In the health model the `work_queue` dependency is reported as **not-applicable** for
  this role — the explicit signal that an API node does not own queue draining.

### 5.2 `worker`
- **Drains the existing local durable work queue** and executes the proven pipeline;
  it **serves no public API** (`serves_api_by_default` is false).
- Uses the existing `WorkQueue` / worker / recovery contracts unchanged: no broker, no
  new queue, no change to recovery eligibility or lineage.
- In the health model the `work_queue` dependency is reported as **configured**.

### 5.3 `combined`
- Does both — serves the loopback read-model and drains the local queue — and is the
  **proven local default**. Selecting no role yields `combined`, which is exactly the
  current single-process local behaviour.
- It is a local shape, not a production posture: `combined` does not imply cloud,
  distribution, or public exposure.

---

## 6. Health and readiness model

The model lives in `storytime.runtime.health` and is **pure data derived from
configuration and the role**. It instantiates no worker, queue, or artifact store,
binds no socket, opens no database, and wraps nothing.

- `evaluate_runtime_health(runtime_config, config)` returns a frozen `RuntimeHealth`
  with: `runtime_role`, `deployment`, `environment`, `slot`, `serves_api`,
  `runs_worker_loop`, `allows_public_ingress` (always false), `allows_wildcard_cors`
  (always false), a tuple of `dependencies`, and a tuple of `warnings` (empty).
- **Dependencies** are four `RuntimeDependency` descriptors, each carrying a
  `DependencyStatus` of `configured` or `not-applicable`:
  - `state_store` — configured for every role;
  - `work_queue` — configured for `worker` / `combined`, **not-applicable for `api`**
    (the core role-separation signal);
  - `artifact_store` — configured for every role;
  - `observer` — configured for every role, with a detail string naming the existing
    telemetry mode (`noop` / `otel`) from `StoryTimeConfig`.
- **`ready`** is derived: every dependency is `configured` or `not-applicable`, public
  ingress is not allowed, wildcard CORS is not allowed, and there are no warnings.
- **`status`** is `"ok"` when ready, otherwise `"degraded"`.
- **`to_summary()`** returns a plain `dict[str, object]` for safe display: role,
  deployment, environment, slot, the two behaviour flags, the ingress/CORS flags,
  `ready`, `status`, the dependency names with their statuses and details, and the
  warnings. It exposes **no secret, credential, or filesystem path**.
- `api_bind_is_loopback()` checks the fixed loopback API bind host through the locked
  `validate_bind_host`, returning false (rather than raising) if it is ever non-loopback.

Because the model is a pure function of `(RuntimeConfig, StoryTimeConfig)`, the same
inputs always produce the same health, and it can be unit-tested without touching the
filesystem, the network, or the queue.

---

## 7. Configuration boundary

The boundary lives in `storytime.runtime.config` and is intentionally tiny:

- `load_runtime_config(config, environ=None)` reads exactly one new environment
  variable, `STORYTIME_RUNTIME_ROLE` (constant `RUNTIME_ROLE_ENV`):
  - unset or empty → `DEFAULT_RUNTIME_ROLE` (`combined`);
  - a recognised value (`api` / `worker` / `combined`, any case) → that role;
  - an unrecognised value → `ValueError` (fail-fast, via `parse_role`).
- The returned `RuntimeConfig` is frozen: `role`, plus `deployment`, `environment`, and
  `deployment_slot` derived from the immutable `StoryTimeConfig`.
- The **deployment dimension is fixed to `local`** (constant `LOCAL_DEPLOYMENT`).
  `STORYTIME_DEPLOYMENT` is documented here as **DEFERRED** and is **not read as active
  configuration** in this phase; introducing real deployment targets is future work for
  the later cloud decomposition. `environment` and `deployment_slot` continue to come
  from the existing `StoryTimeConfig` fields and are not new Phase 15A inputs.

This keeps the genuinely-new configuration surface of Phase 15A to a single variable
with three valid values, and everything else derived from already-proven config.

---

## 8. What remains deferred

Everything cloud-shaped beyond *naming the roles and reporting readiness* is deferred
and recorded in the locked 14D register (`docs/phase14d-deferred-cloud-work-register.md`):
an external broker / cloud queue; a distributed, replica-safe worker; an object-storage
adapter and any artifact URL strategy; authentication and public ingress; a real
provider TTS integration, audio, and RSS; a telemetry export path / collector and any
dashboards, SLOs, or alerting; and any cloud deploy mechanics (Kubernetes, Terraform,
Helm, blue/green). None of these exist yet. Phase 15A neither builds nor starts them.

---

## 9. Phase 15B readiness implications

This turns the Phase 15A skeleton into a constraint for the next step. Phase 15B is
**not** designed here; this is recommended future sequencing, and Phase 15B remains NOT
STARTED.

The 14D-recommended Phase 15B is the Cloud Queue / Worker Adapter (§11.B): a managed
broker behind the existing `WorkQueue` port with a replica-safe worker, proving
no-double-execution under two or more workers via leasing and idempotent stage
execution. Phase 15A makes that narrower by giving Phase 15B a stable place to stand:

- the `worker` role already names "drains the queue", and its `work_queue` dependency is
  already the descriptor a managed-broker adapter would report against;
- the `api` role already declares it does not drain the queue, so splitting API and
  worker nodes does not change which node owns draining;
- readiness is already derived from configuration, so a future broker-backed adapter can
  surface its own readiness through the same `RuntimeHealth` shape without changing the
  contract.

Phase 15B would supply the managed broker behind the port; Phase 15A only names the
seam. Phase 15A does not start Phase 15B and does not mark any later phase active.

---

## 10. Validation expectations

Phase 15A is validated by the full locked gate, expected green on an untouched
checkout:

- `uv run pytest` — the existing suite plus the new `tests/test_runtime_roles.py`
  cases (role vocabulary, the three role behaviours, the health/readiness model, the
  configuration boundary, and the doc-state assertions).
- `uv run ruff check .` — lint clean.
- `uv run mypy src` — strict type-check clean; the runtime package is fully annotated.
- `uv run lint-imports` — both import-linter contracts kept, including the
  OpenTelemetry contract now naming `storytime.runtime` (the runtime package does not
  import OpenTelemetry).
- `uv run storytime doctor` — unchanged: it still checks exactly `python`, `sqlite3`,
  `opentelemetry`, and `ffmpeg`. Phase 15A adds no CLI command and no doctor check; the
  role separation is proven by the self-contained runtime module and its tests.

A behaviour-level expectation accompanies the gate: the default role is `combined`,
which reproduces the proven local single-process behaviour, so no existing test changes
meaning and no existing behaviour changes.

---

## 11. Explicit statement — no cloud behavior implemented

Phase 15A implements **no** cloud / distributed behavior. No external broker, cloud
queue, distributed worker, object-storage adapter, authentication system, public
ingress, provider TTS, audio, RSS, telemetry export, collector, dashboard, or
dependency was added. The `storytime.runtime` package is pure data: it names the
`api` / `worker` / `combined` runtime roles, derives a health / readiness model from
configuration, and reads one new environment variable. The running system remains a
local-first, single-process SQLite proof; the cloud-shaped roles named here are a plan,
and the later Phase 15 decomposition must provide the evidence the locked 14D baseline
requires before any cloud behavior is trusted.
