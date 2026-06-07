# StoryTime — Public Repository Readiness

A checklist and guidance document for preparing the StoryTime repository for a
**public audience** — a public GitHub repository, a portfolio link shared with
a hiring manager, or any other setting where strangers can read the code and
the docs.

This document adds no product behaviour and creates no assets. It is a
**checklist a human runs before publishing** — it does not itself publish
anything, generate screenshots, produce demo audio or video, or add any binary
artifact, and it adds no licensing claim that the repository does not already
support. It packages, as a pre-publication discipline, the hygiene posture
that Phases 0–11 already established.

Companion documents this builds on: `docs/security-secrets-checklist.md` (the
authoritative secrets posture), `docs/known-limitations.md` (the honest
scope), `docs/screenshot-instructions.md` (the manual evidence-capture
instructions), `docs/fresh-clone-checklist.md` and
`docs/operator-reproducibility-checklist.md` (fresh-clone verification), and
`docs/artifact-manifest.md` (the archive-hygiene rules). Where this document
and one of those disagree on a detail, that companion document is
authoritative for its area.

**How to use it.** Work top to bottom before making the repository public, or
before sharing a link. Each item is a check, not an action to automate. The
final section — "Do not publish until verified" — lists the hard gates: if any
of those is unresolved, the repository is not ready to publish.

---

## 1. Public-safe README checklist

The `README.md` is the first thing a public visitor reads. Confirm:

- [ ] **The opening describes the project honestly.** The first paragraphs say
  what StoryTime is — a local-first, observability-native content-to-audio
  pipeline — without hype and without claiming users, scale, or a deployment.
- [ ] **The "For reviewers — start here" section is present and current.** It
  points a portfolio reviewer to the entry-point documents
  (`docs/portfolio-overview.md`, `docs/portfolio-evidence-index.md`,
  `docs/portfolio-demo-narrative.md`) and states the project status.
- [ ] **The status text matches the State Preservation Bundle.** The README's
  phase claims agree with `docs/handoff-state.md` (the authoritative current
  status). A public visitor should not see the README and the handoff state
  disagree.
- [ ] **The setup path works as written.** The documented setup —
  install `uv`, then `uv sync --frozen --extra dev`, then
  `uv run storytime doctor` — is the canonical form and was verified from a
  fresh clone in Phase 11B. Confirm it still reads correctly.
- [ ] **Scope is stated, not implied.** The README says plainly what StoryTime
  is *not* (no users, no SLA, no cloud, no commercial-vendor integration) and
  points to `docs/known-limitations.md`.
- [ ] **No internal-only language leaks.** The README is written for a public
  reader: no unexplained internal jargon, no broken cross-references, no
  placeholder "TODO" text.
- [ ] **Links resolve.** Every `docs/...` path the README references exists in
  the repository.

## 2. Secrets and configuration check

`docs/security-secrets-checklist.md` is the authoritative secrets document;
this is the pre-publication confirmation of it. Confirm:

- [ ] **No real credentials anywhere.** The repository contains no real
  tokens, API keys, license keys, account or tenant identifiers, or routable
  private endpoints. The only credential-shaped files are templates.
- [ ] **Environment templates are placeholders only.** `.env.example` carries
  only non-sensitive defaults and says so; `config/vendor.secret.env.example`
  contains only obvious `REPLACE-...` placeholders and uses the RFC 2606
  reserved `.invalid` TLD so placeholder endpoints are non-routable.
- [ ] **Secret-file patterns are git-ignored.** `.gitignore` reserves `.env`,
  `*.secret.env`, `*.local.env`, and `*.env.local`, so a filled-in
  credentials file cannot be committed.
- [ ] **Committed env files are intentionally non-secret.**
  `config/deploy/blue.env` and `config/deploy/green.env` carry only slot
  identity and telemetry resource attributes; each states in its header that
  it contains no secrets. Confirm this is still true.
- [ ] **Git history is clean of secrets.** Before a *first* public push,
  confirm no secret was ever committed and later deleted — a deleted secret
  still lives in history. (StoryTime has had no real secrets, so this is a
  confirmation, not a remediation; if a public mirror is created from a
  partial history, re-confirm.)
- [ ] **No machine-specific absolute paths or personal identifiers** are
  embedded in committed files.

## 3. Demo data check

StoryTime ships curated demo data in `demo/`. Before publishing, confirm:

- [ ] **All demo seed texts are genuinely public-domain / CC0.** The
  `demo/seed/` texts are original CC0 content with schema-valid source
  manifests; confirm nothing copyrighted slipped in.
- [ ] **The demo-only blocked-source list is clearly demo-scoped.**
  `demo/governance/demo-blocked-sources.yaml` is a demo-only deny-list used by
  one scenario through the existing `STORYTIME_BLOCKED_SOURCES` mechanism; it
  is not production configuration and is documented as demo-only.
- [ ] **No generated audio is committed.** The repository commits no `.wav` or
  `.mp3` output. Demo audio is produced locally at demo time and is not source.
- [ ] **The demo fixtures exercise the real system.** The six `demo/fixtures/`
  scenarios drive the real pipeline, report, queue, governance, and `rerun` —
  none fakes success. The fixture-integrity tests (`tests/test_demo_fixtures.py`)
  confirm their shape.
- [ ] **The demo runs offline.** `docs/demo.md` requires no cloud account, no
  paid API, and no external service.

## 4. Screenshot and visual-asset placeholder checklist

This phase deliberately creates **no** screenshots, images, demo audio, demo
video, slide decks, or other binary assets. If a public portfolio page wants
visual evidence, it is captured manually and kept *outside* this repository.
Confirm:

- [ ] **No binary visual assets are committed.** No `.png`, `.jpg`, `.gif`,
  `.mp4`, `.pdf`, or slide-deck file is in the repository tree. The repository
  stays source- and text-based.
- [ ] **`docs/screenshot-instructions.md` is treated as instructions, not
  assets.** It tells a human what to capture, manually, on their own machine;
  captured screenshots belong in the operator's own portfolio workspace, not
  in this repository.
- [ ] **If a public README or portfolio page references an image,** that image
  is hosted in the portfolio workspace or an external page — not added to this
  repository — and the reference is clearly an external link.
- [ ] **Text captures are preferred over screenshots** for CLI output: they
  are smaller, searchable, and verifiable. Capture only what the demo actually
  produced; never stage or edit evidence.

*Placeholder note:* if a future phase decides visual assets belong in the
repository, that is a scope decision for that phase — it is explicitly out of
scope here, and this checklist's default is "no binary assets."

## 5. Known-limitations checklist

A public reviewer must be able to find the honest boundaries quickly. Confirm:

- [ ] **`docs/known-limitations.md` is present, current, and linked** from the
  README's reviewer section.
- [ ] **The "what it is not" claims are consistent everywhere.** No public-
  facing document — README, portfolio overview, public copy, this kit's
  narrative — claims users, an SLA, cloud deployment, a commercial-vendor
  integration, a legal/rights-clearance determination, or a GUI that exists.
- [ ] **Vendor-neutrality is stated precisely.** Public copy says StoryTime
  *emits standard OpenTelemetry* and is *compatible with* OTLP fan-out — never
  that it integrates a named commercial vendor.
- [ ] **Governance language does not overclaim.** No public document describes
  the governance gate as a legal determination; the static legal-hallucination
  scanner (`tests/test_legal_hallucination_gate.py`) enforces this for
  governance copy, and public copy must hold the same line.
- [ ] **Future work is marked as future.** The Phase 13 Operator GUI vision
  (`docs/GUI_vision.md`, the roadmap note) is clearly labelled planned and
  **not started** — a public reader should not mistake it for a current
  feature.
- [ ] **The development process is described honestly.** If public copy
  mentions the multi-model RoundTable workflow, it does so accurately and
  without overstating it.

## 6. Repository hygiene check

Confirm the published tree is clean — the archive-hygiene rules in
`docs/artifact-manifest.md` are the standard:

- [ ] **No tooling caches.** No `.pytest_cache/`, `.ruff_cache/`,
  `.mypy_cache/`, or `__pycache__/` directories; all are git-ignored.
- [ ] **No runtime working state.** No `runs/`, `feed/`, `logs/`, or
  `operator-report/` directory; all are git-ignored generated output.
- [ ] **No environments or dependency caches.** No `.venv/`, `node_modules/`,
  or package cache.
- [ ] **No nested archives or large binaries.** No stray `*.tar.gz` inside the
  tree, no large binary blobs.
- [ ] **The six Docker-free quality gates pass** from a clean checkout:
  `uv sync --frozen --extra dev`, `uv run pytest -q`, `uv run ruff check .`,
  `uv run mypy`, `uv run lint-imports`, `uv run storytime doctor`. A public
  repository whose own gates fail undercuts every other claim.
- [ ] **The license situation is accurate.** Do not add a license claim the
  repository does not already support. If a `LICENSE` file is added before
  publishing, it is a deliberate, separate decision — this checklist does not
  invent one, and public copy must not assert a license that is not actually
  present.

## 7. Do not publish until verified — hard gates

These are the gates. If any one is unresolved, **the repository is not ready
to be made public.** Stop and resolve it first.

1. **No real secret is present, in the working tree or in git history.**
   (Section 2.)
2. **No copyrighted or non-public-domain content is committed**, including in
   `demo/seed/`. (Section 3.)
3. **No public-facing document overclaims** — no users, no SLA, no cloud
   deployment, no named commercial-vendor integration, no legal/rights-
   clearance determination, no GUI presented as existing. (Sections 1, 5.)
4. **The README status matches `docs/handoff-state.md`.** A public visitor
   must not catch the project contradicting its own state. (Section 1.)
5. **The six Docker-free quality gates pass from a clean checkout.**
   (Section 6.)
6. **No binary assets, caches, runtime state, or environments are committed.**
   (Sections 4, 6.)
7. **No license claim is asserted that the repository does not actually
   support.** (Section 6.)

Verifying these is a human responsibility; this document does not and cannot
perform the publication. Treat a "publish" decision the same way the project
treats a phase lock — explicit, checked, and reversible only at a cost.

---

This document is part of Phase 12C — Portfolio Demo Narrative / Public
Presentation Kit. Phase 12C is a documentation-only portfolio packaging phase;
it changes no product, runtime, API, CLI, or telemetry behaviour, and it
publishes nothing — it only prepares a human to publish responsibly.
