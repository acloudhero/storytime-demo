# StoryTime — Security & Secrets Hygiene Checklist

The local-first security and secrets baseline for StoryTime, stated explicitly
so a release candidate can be checked against it. This is a Phase 11A hardening
surface: it documents the posture the repository already holds and makes it
verifiable; it changes no behaviour.

StoryTime is **local-first by design**. It runs on one machine, from the
command line, and makes no authenticated network calls in its default mode.
That property is the foundation of its security posture: the trust surface is
small because almost nothing leaves the machine.

## Secrets posture

### No real secrets are committed

The repository contains **no real credentials, tokens, endpoints, account
identifiers, or keys**. The two environment-template files are placeholders
only:

- `.env.example` — the local environment template. Every value is a
  non-sensitive default (telemetry mode, loopback host/port, deployment
  labels). The file states explicitly that no value in it is a secret.
- `config/vendor.secret.env.example` — the optional Phase 8C vendor-export
  credentials **template**. Every value is an obvious `REPLACE-...`
  placeholder, and the placeholder endpoints use the RFC 2606 reserved
  `.invalid` TLD so they are non-routable.

### Secret-bearing files are git-ignored

`.gitignore` reserves the secret-file convention so a filled-in credentials
file can never be committed:

- `.env`
- `*.secret.env` (this covers `config/vendor.secret.env`)
- `*.local.env`
- `*.env.local`

To use the optional vendor export, a user copies the `.example` template to a
git-ignored real file and fills it in privately — it is never committed.

### Committed env files that are intentionally not secrets

`config/deploy/blue.env` and `config/deploy/green.env` **are** committed. They
carry only blue/green slot identity and telemetry resource attributes
(deployment label, slot name, loopback host/port, telemetry mode) — no
credentials. Each file states in its own header that it contains no secrets and
is safe to commit. This is a deliberate, documented exception, not an
oversight.

## Network and API posture

- **No network calls are required for validation.** All six quality gates and
  the entire test suite run offline. The only network access in normal use is
  the package download performed by `uv sync`.
- **No external API is required for the demo seed path.** The `demo/` fixtures
  and seed texts drive the real local pipeline with no paid service and no
  remote call.
- **Outbound telemetry is opt-in and disabled by default.**
  `STORYTIME_TELEMETRY=noop` is the default; the OpenTelemetry stack and the
  optional vendor export are explicit opt-ins. The Phase 8A baseline confines
  any vendor fan-out to the local OpenTelemetry Collector — application code
  emits telemetry only to a local endpoint.

## Telemetry and logging hygiene

- StoryTime's telemetry adapter redacts absolute filesystem paths at a single
  hygiene choke point, so machine-specific paths do not leak into spans.
- The operator-facing surfaces show **structured** fields only. The failure
  queue and operator report surface the structured `error_kind` code, never
  the free-text `error_message`; and the governance decision enum, never the
  raw `blocked_reason` text. Raw story/narration text is never placed in
  reports, queue output, telemetry, or logs.
- Observability links are links only — no embedded data and no secrets in URLs.

## Governance posture

- The blocked-source deny-list (`config/governance/blocked-sources.yaml`) ships
  **empty** — the demo uses only CC0 / public-domain / explicit-permission /
  local-test-fixture content, so nothing is blocked by default. A demo-only
  deny-list is supplied per run via `STORYTIME_BLOCKED_SOURCES` and changes no
  committed configuration.
- The static legal-hallucination verification gate (Architecture Baseline
  §24.14) scans the repository's code, config, and non-governance docs for
  forbidden legal-certification vocabulary and reports zero violations. It runs
  inside the pytest suite, so a green `pytest` run already proves it.
- Governance status is recorded honestly: the Trust Envelope transcribes a
  human operator's recorded licensing decision. StoryTime performs no legal
  determination and does not certify copyright safety; every governance display
  carries the standing "record of a human decision, not legal advice"
  disclaimer. Governance is **source authorization**, not viewpoint
  acceptability — it is not a content-moderation system.

## Release-candidate secrets-hygiene checklist

Before treating an archive as a release candidate, confirm:

- [ ] No `.env`, `*.secret.env`, or `*.local.env` file is present in the
      archive — only the `*.example` templates.
- [ ] `.env.example` and `config/vendor.secret.env.example` contain
      placeholders only; no real endpoint, token, account id, or key.
- [ ] `config/deploy/blue.env` / `green.env` contain only slot identity and
      telemetry attributes — no credentials.
- [ ] `config/governance/blocked-sources.yaml` is empty (`blocked_sources: []`).
- [ ] `uv run pytest -q` passes — which includes a clean legal-hallucination
      scan.
- [ ] No `runs/`, `feed/`, `logs/`, `operator-report/`, or generated database
      file is in the archive (these are runtime output and could contain
      run-specific data) — see `docs/release-candidate-hardening.md`.

## Related documents

- `docs/release-candidate-hardening.md` — the hardening baseline overview.
- `docs/architecture-baseline.md` Section 24 — the Governance Baseline
  (Trust Envelope, licensing, fail-closed gating, secrets policy).
- `docs/known-limitations.md` — the honest account of governance boundaries.
- `.env.example`, `config/vendor.secret.env.example` — the env templates.
