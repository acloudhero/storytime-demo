# StoryTime — Phase 9B Minimal Trust Envelope Implementation Prompt

> **Status: DRAFT PROMPT — not implementation.** This file is a draft prompt
> for the next round, authored during the Phase 9A.1 / Phase 9A lock-closure
> round. It authorizes nothing by itself. It must be reviewed, scoped, and
> gated under the Phase Closure Protocol before any Phase 9B implementation
> begins. Drafting this file changed no application code, schema, config, or
> behaviour.

You are Claude Opus 4.7 acting as Chief Implementation / Hardening Engineer.

## Task

Implement **Phase 9B — Minimal Trust Envelope Implementation**.

Phase 9B is the implementation phase that turns the locked Phase 9A governance
law (`docs/architecture-baseline.md` Section 24) into a concrete, minimal,
working artifact and gate. Implement only what Section 24 defines; do not
expand scope.

Read first, in this order:

1. `LLM_DIRECTOR.md`
2. `docs/handoff-state.md`
3. `docs/canonical-state.md`
4. `docs/phase-history.md`
5. `docs/architecture-baseline.md` — **Section 24 is the governing law for
   this phase**; also read Section 6 (source manifest), Section 7 (inter-stage
   artifact format), Section 9 (pipeline stage model), and Section 5 (local
   state store / SQLite).
6. `docs/roadmap.md`
7. `docs/open-issues.md`
8. `docs/phase-closure-protocol.md`
9. `docs/telemetry-map.md`
10. `docs/runbook.md`
11. `docs/verification-log.md`
12. `docs/artifact-manifest.md`
13. `docs/roundtable-import-bridge.md`

Do not rely on stale RoundTable rounds or prior chat context. The repository
State Preservation Bundle is authoritative.

## Required phase-gate verification

Before editing, verify from the uploaded state bundle:

1. Phase 9A is **locked** (`docs/canonical-state.md` records the Phase 9A lock;
   `docs/architecture-baseline.md` Section 24 status block reads "Locked").
2. `docs/architecture-baseline.md` Section 24 is **canonical** architecture
   law.
3. The requested next phase is **Phase 9B — Minimal Trust Envelope
   Implementation**.
4. Phase 9B has **not already started** (no Trust Envelope schema, gate,
   blocked-source config, or grep/regex gate already exists in the repo).

If any condition fails, stop and return:

```text
BLOCKED — PHASE 9B STATE MISMATCH
```

Do not attempt to repair phase state unless explicitly instructed.

## Authoritative governance law

The locked `docs/architecture-baseline.md` Section 24 is the governing law.
Implement exactly what it specifies. In particular:

- §24.2 — StoryTime is **not** a legal rights-clearance engine; the human
  operator is the source of truth for licensing decisions.
- §24.3 — No legal automation / no legal hallucination.
- §24.4 / §24.5 — Allowed and disallowed source categories;
  source-authorization-not-viewpoint rule (governance is **not**
  content moderation).
- §24.6 — Fail-closed governance gate: check early, hard-block before
  TTS / audio / RSS.
- §24.7 / §24.8 — The Trust Envelope concept and its canonical minimum schema.
- §24.9 — Blocked-source policy.
- §24.10 — Secrets policy.
- §24.12 — Telemetry / privacy carryover.
- §24.14 — Future static legal-hallucination grep/regex gate.
- §24.15 — Phase 10 dependency contract.

If Phase 9B finds any genuine conflict between Section 24 and existing locked
architecture, **stop and report it** rather than resolving it unilaterally;
Section 24 changes require a new explicit, user-approved amendment.

## 1. Implementation scope

Phase 9B implements, minimally and honestly:

1. **Trust Envelope schema** — a schema-validated record conforming to the
   canonical §24.8 schema.
2. **Durable artifact-envelope governance truth** — the Trust Envelope is
   embedded in or linked from the durable artifact envelope (§7); the durable
   envelope is the governance source of truth for portability/recovery.
3. **SQLite projection** — a queryable projection of the Trust Envelope for
   operational queries; it must be rebuildable from the durable envelopes and
   must never be treated as the source of truth.
4. **Fail-closed governance gate** — checks governance status as early as
   practical and hard-blocks before TTS, audio processing, or RSS publishing
   when no `APPROVED` Trust Envelope exists.
5. **Local blocked-source config** — a local, explicit, inspectable
   blocked-source configuration file (§24.9), expected at
   `config/governance/blocked-sources.yaml`.
6. **Static legal-hallucination grep/regex gate** — a static verification
   check that bars the §24.14 forbidden legal-certification vocabulary from
   docs, config, and implementation, with an allowlist for the governance
   docs that legitimately define that vocabulary.
7. **Tests** — see section 6 below.
8. **Docs / runbook updates** — update `docs/architecture-baseline.md` only if
   a new amendment is genuinely required (it should not be — §24 is the law);
   update `docs/runbook.md`, `docs/telemetry-map.md` if telemetry is touched,
   and the State Preservation Bundle living docs.

Keep the implementation minimal. This is the *minimal* Trust Envelope: the
smallest honest implementation that satisfies Section 24, not a
governance product.

## 2. Required hard constraints

Phase 9B must not:

- add legal automation or any automated legal determination;
- add an AI copyright classifier or any model-inferred rights status;
- add legal-compliance, legal-advice, or legal-clearance claims;
- add authentication, users, roles, or permissions;
- add cloud security, hosted databases, or a production secrets manager;
- add scraping or arbitrary website ingestion;
- add hosted services or cloud deployment;
- store secrets in source, committed docs, SQLite, or artifact envelopes;
- put raw story text, narration text, full URLs containing secrets, long
  notes, or `review_context_summary` text into telemetry;
- add viewpoint, topic, or content filtering / moderation / safety
  classification — governance is source authorization, not viewpoint
  acceptability (§24.5);
- add compliance scoring of any kind;
- add CI/CD secrets;
- weaken the Phase 8 telemetry/privacy rules;
- reopen any locked phase.

The six Docker-free quality gates must remain Docker-free. The core
application and the full test suite must still run with no internet access and
no Docker.

## 3. Fail-closed requirement

Implement the §24.6 fail-closed gate:

- **Check early.** Check governance status as early as practical in the
  pipeline — ideally before or during approval / rehydration — so an
  unauthorized source is surfaced and stopped as soon as possible.
- **Block hard.** Regardless of how early a check runs, the pipeline must
  **block execution before TTS, audio processing, or RSS publishing** unless
  an `APPROVED` Trust Envelope exists for the source.
- **Fail closed on every non-approved state.** If the governance decision is
  `BLOCKED`, `REJECTED`, `NEEDS_REVIEW`, or `UNKNOWN`, or if the Trust
  Envelope is missing, malformed, or unverifiable, the pipeline must fail
  closed before TTS and must not publish to RSS.
- An early check that passes never licenses a later stage to skip the hard
  gate; the before-TTS/audio/RSS block is the load-bearing invariant.

Wire the gate into the pipeline honestly, consistent with the Section 9 stage
model. Record gate decisions in the durable event log / state store as
appropriate, referencing IDs and hashes — never content payloads.

## 4. Trust Envelope schema

Use the **exact locked Section 24.8 schema**. Field names may be trivially
aligned only where genuine repo consistency requires it (e.g. casing or a
prefix matching existing manifest/envelope fields); the **semantics, the enum
value sets, and the durable-envelope-wins rule must be preserved**.

Required fields (per §24.8):

```yaml
schema_version: string
source_ref: string
source_url: string | null
source_title: string | null
source_author: string | null
license_type: enum
license_url: string | null
license_evidence_ref: string | null
decision: enum
decision_timestamp: ISO-8601 string
approver_id: string
allowed_use: string | null
attribution_required: boolean | null
commercial_use_allowed: boolean | null
blocked_reason: string | null
governance_notes: string | null
review_context_summary: string | null
artifact_hash_refs: list[string]
```

- `review_context_summary` — a short human-readable justification for the
  operator's decision; **must not** contain raw story text or private content.
- `artifact_hash_refs` — list of artifact hash references tying the envelope
  to the run's artifacts, consistent with the §7 artifact-hash model.

`license_type` minimum value set: `CC0`, `US_PUBLIC_DOMAIN`,
`EXPLICIT_PERMISSION`, `LOCAL_TEST_FIXTURE`, `BLOCKED`, `UNKNOWN`.

`decision` minimum value set: `APPROVED`, `REJECTED`, `BLOCKED`,
`NEEDS_REVIEW`.

The durable artifact envelope is the governance source of truth for
portability/recovery; the SQLite projection is an operational-query
convenience and must be rebuildable from the durable envelopes.

## 5. Blocked-source config

Implement a local, explicit, inspectable blocked-source config at
`config/governance/blocked-sources.yaml`. It must not be a cloud service, must
not fetch remote blocklists, and must not scrape or classify websites. Each
entry should carry a source pattern / URL / domain reference, a `reason`, an
`added` timestamp if practical, and an optional `note`. A source matched by
this config resolves to a `BLOCKED` decision and fails the §24.6 gate.

## 6. Testing

Add genuine tests (no placeholders). At minimum:

- **Schema validation** — a well-formed Trust Envelope validates; a malformed
  one is rejected.
- **Approved source proceeds** — a source with an `APPROVED` Trust Envelope
  passes the gate and the pipeline continues.
- **Missing envelope fails closed** — a source with no Trust Envelope is
  blocked before TTS and not published to RSS.
- **Non-approved states fail closed** — `BLOCKED`, `REJECTED`,
  `NEEDS_REVIEW`, and `UNKNOWN` each fail closed before TTS/RSS.
- **Malformed / unverifiable envelope fails closed.**
- **Blocked-source config blocks a source** — a source matched by
  `config/governance/blocked-sources.yaml` resolves to `BLOCKED` and fails the
  gate.
- **No legal-hallucination terms** — the static grep/regex gate finds no
  forbidden legal-certification vocabulary in docs, config, or implementation
  (governance docs that define the vocabulary are allowlisted).
- **No raw text in telemetry** — governance telemetry, if any, carries only
  bounded status metadata; no raw source/narration text, notes, or review
  summaries.
- **No secrets** — no secret is committed; none is stored in SQLite or in
  artifact envelopes.

## 7. Verification

Run the six Docker-free quality gates and report exactly what passed or
failed — never fabricate results:

1. `uv sync --frozen --extra dev`
2. `uv run pytest -q`
3. `uv run ruff check .`
4. `uv run mypy`
5. `uv run lint-imports`
6. `uv run storytime doctor`

## 8. Archive

Produce a new archive:

```text
storytime-phase9b-minimal-trust-envelope-implementation.tar.gz
```

Include the full project tree and the full State Preservation Bundle files.

Exclude: `.venv/`, `runs/`, `feed/`, `.env`, real `*.secret.env`, caches,
generated logs, secrets.

Report: archive filename, SHA-256, files changed, gates run (pass/fail),
living docs updated, open issues added/closed, and a lock-readiness
assessment.

## 9. Required final report

End the Phase 9B round with the standard implementation report (per
`LLM_DIRECTOR.md`):

1. Files changed
2. Tests/gates run
3. Living docs updated
4. Living docs unchanged and why
5. Open issues added/closed
6. Artifact produced (filename + SHA-256)
7. Confirmation that the State Preservation Bundle is included
8. Lock readiness assessment

Per the Phase Closure Protocol, Phase 9B implementation output is **not** phase
completion: it must be reviewed by GPT-5.5, critiqued by Gemini, and explicitly
approved by the user before Phase 9B locks.

## Hard prohibitions (restated)

Do not, in Phase 9B: add legal automation, an AI copyright classifier, or
compliance scoring; add legal/compliance/clearance claims; add
auth/users/roles/permissions; add cloud security, hosted databases, or a
production secrets manager; add scraping or arbitrary website ingestion; add
hosted services or cloud deployment; store secrets in source, docs, SQLite, or
artifact envelopes; add CI/CD secrets; add viewpoint/topic/content
filtering, moderation, or safety classification; put raw story text into
telemetry; weaken Phase 8 telemetry/privacy rules; reopen locked phases; or
expand scope beyond what locked Section 24 defines.
