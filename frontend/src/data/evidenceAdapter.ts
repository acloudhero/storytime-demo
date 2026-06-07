/**
 * evidenceAdapter — Phase 13D.1 Evidence / Validation static view-model.
 *
 * Organises the static evidence references and validation categories the
 * Evidence / Validation view displays. Three rules govern the contents:
 *
 *   1. No `fetch`. No file I/O. No runtime parsing of repository docs. The
 *      adapter ships hardcoded portfolio copy and repository-relative path
 *      strings only — opening the referenced files happens in the user's
 *      own editor, not in the browser.
 *   2. No invented live status. There are no live test results, no live CI
 *      pass/fail counts, no fabricated freshness timestamps. The view
 *      categorises evidence by claim and points to where reviewers find it.
 *   3. Counts pulled from the existing static export (e.g. number of runs,
 *      number of disabled future actions across the export) are descriptive,
 *      not assertions about a live system. They come from `adapter.ts` and
 *      `governanceAdapter.ts`, both of which read the locked Phase 13C
 *      `storytime-demo-export.json` at module-load time.
 *
 * The literal disclaimer "STATIC PORTFOLIO DATA — NOT A LIVE CI/CD DASHBOARD"
 * is exported here and rendered prominently by the consuming view. The state-
 * discipline guard and a deliberate grep in `frontend/src` both expect this
 * exact string to be present.
 */

import {
  DEMO_FAILURE_QUEUE,
  DEMO_RUN_DETAILS,
  DEMO_RUN_SUMMARIES,
  EXPORT_META,
} from "./adapter";
import { GOVERNANCE_RUN_ROWS } from "./governanceAdapter";

/* ──────────────────── disclaimer ──────────────────── */

/**
 * The mandatory Evidence / Validation disclaimer. Must remain present
 * verbatim in `frontend/src` per the Phase 13D.1 contract.
 */
export const EVIDENCE_DISCLAIMER =
  "STATIC PORTFOLIO DATA — NOT A LIVE CI/CD DASHBOARD";

/* ──────────────────── static evidence categories ──────────────────── */

/**
 * A single category of evidence. `claim` states what StoryTime claims;
 * `proof` describes where a reviewer can verify the claim in the
 * repository, in their own editor, without running the browser. `paths`
 * lists the repository-relative files (or paths) that hold the proof.
 */
export interface EvidenceCategory {
  /** Stable id, used as React key. */
  id: string;
  /** Short heading shown in the view. */
  title: string;
  /** What StoryTime claims about itself, in plain language. */
  claim: string;
  /**
   * Where the claim is supported in the repository — descriptive prose,
   * not a runtime assertion.
   */
  proof: string;
  /** Repository-relative paths a reviewer can open in their editor. */
  paths: readonly string[];
}

export const EVIDENCE_CATEGORIES: readonly EvidenceCategory[] = [
  {
    id: "backend-validation-gates",
    title: "Backend validation gates",
    claim:
      "StoryTime's backend ships with six Docker-free validation gates that " +
      "must be green before any phase can be locked.",
    proof:
      "Each locked phase records the exact gate output (uv pytest, ruff, " +
      "mypy, import-linter, storytime doctor, and the typed-static-export " +
      "tests) in the verification log entry for that phase. Reviewers can " +
      "open the entries below to see the recorded outputs, and can run " +
      "the same six gates locally from the project root.",
    paths: ["docs/verification-log.md", "tests/test_operator_export.py"],
  },
  {
    id: "frontend-validation-gates",
    title: "Frontend validation gates",
    claim:
      "The bounded frontend ships with TypeScript typecheck and Vite build " +
      "gates, scoped to the static-export contract.",
    proof:
      "The frontend gates (npm run typecheck, npm run build) are recorded " +
      "alongside the backend gates in the same verification-log entries. " +
      "The deterministic static export the frontend reads from is locked " +
      "by the contract document below.",
    paths: [
      "docs/verification-log.md",
      "docs/frontend-static-export-contract.md",
    ],
  },
  {
    id: "no-network-discipline",
    title: "No-network discipline",
    claim:
      "The frontend does not perform any network call: no fetch, axios, " +
      "XMLHttpRequest, WebSocket, or other live integration.",
    proof:
      "Each locked phase verification entry includes the mechanical grep " +
      "for `fetch`, `axios`, `XMLHttpRequest`, and `WebSocket` across " +
      "`frontend/src`. Any matches are documentation comments that " +
      "explicitly assert the absence of network calls.",
    paths: [
      "docs/verification-log.md",
      "docs/frontend-static-export-contract.md",
    ],
  },
  {
    id: "deterministic-export",
    title: "Deterministic export",
    claim:
      "The static export the frontend reads is a deterministic, " +
      "byte-stable artifact produced by the backend export module — not a " +
      "hand-edited blob.",
    proof:
      "`tests/test_operator_export.py` re-renders the export from the " +
      "backend module and asserts the committed JSON is byte-identical. " +
      "The contract document below records the schema version and the " +
      "frozen export shape.",
    paths: [
      "tests/test_operator_export.py",
      "docs/frontend-static-export-contract.md",
    ],
  },
  {
    id: "archive-hygiene",
    title: "Archive hygiene",
    claim:
      "Each locked-phase tarball excludes caches, virtual envs, binaries, " +
      "secrets, and prior nested archives.",
    proof:
      "The artifact manifest records the SHA-256, size, entry count, and " +
      "exclusion list for each delivered tarball. The verification log " +
      "lists the explicit exclusion flags used at package time.",
    paths: ["docs/artifact-manifest.md", "docs/verification-log.md"],
  },
  {
    id: "state-discipline-guard",
    title: "State-discipline guard",
    claim:
      "A Python-only state-discipline test guards the State Preservation " +
      "Bundle so it never claims a future phase as locked, never claims " +
      "the current candidate as locked, and never erases earlier lock " +
      "records.",
    proof:
      "The guard reads the living state docs and asserts current-phase, " +
      "last-locked-phase, forbidden-future-claims, and append-only " +
      "history invariants. It is part of the standard `uv run pytest -q` " +
      "run for every phase.",
    paths: ["tests/test_failure_mode_regression.py"],
  },
  {
    id: "append-only-history",
    title: "Append-only history",
    claim:
      "Locked decisions are never rewritten: each phase appends a new " +
      "entry to `docs/canonical-state.md` and `docs/phase-history.md`.",
    proof:
      "The state-discipline guard explicitly checks that earlier lock " +
      "markers (Phase 11A–11D, 12A–12D, 13A, 13B, 13C, 13D and the " +
      "post-Phase-10 reconciliation) are still present in both documents. " +
      "A regression there fails the gate.",
    paths: ["docs/phase-history.md", "docs/canonical-state.md"],
  },
] as const;

/* ──────────────────── repository references for the references panel ─── */

/**
 * A small, ordered list of repository-relative files that the Evidence /
 * Validation view points to. Distinct from `EVIDENCE_CATEGORIES.paths`
 * because some references appear across multiple categories.
 */
export interface EvidenceRepoReference {
  /** Stable id, used as React key. */
  id: string;
  /** Repository-relative path the reviewer can open. */
  path: string;
  /** One-line description of what they will find there. */
  note: string;
}

export const EVIDENCE_REPO_REFERENCES: readonly EvidenceRepoReference[] = [
  {
    id: "verification-log",
    path: "docs/verification-log.md",
    note: "Per-phase record of every gate's exact output, from Phase 7 to today.",
  },
  {
    id: "static-export-contract",
    path: "docs/frontend-static-export-contract.md",
    note: "The deterministic, read-only static export shape the frontend depends on.",
  },
  {
    id: "deferred-register",
    path: "docs/frontend-gui-deferred-work-register.md",
    note: "Explicit ledger of frontend work intentionally deferred to later subphases.",
  },
  {
    id: "phase-history",
    path: "docs/phase-history.md",
    note: "Append-only narrative of every locked round.",
  },
  {
    id: "artifact-manifest",
    path: "docs/artifact-manifest.md",
    note: "Tarball lineage: name, SHA-256, size, entry count, exclusions per phase.",
  },
  {
    id: "state-discipline-test",
    path: "tests/test_failure_mode_regression.py",
    note: "The state-discipline guard that protects the State Preservation Bundle.",
  },
  {
    id: "operator-export-test",
    path: "tests/test_operator_export.py",
    note: "The contract test asserting the committed static export is byte-identical to a fresh render.",
  },
] as const;

/* ──────────────────── data-source / demo-snapshot framing ──────────────── */

/**
 * Demo / Active / Candidate **data snapshots**, not deployment environments.
 * Phase 13D.1 surfaces this distinction explicitly: the prior frontend
 * deferred-register draft used "Demo / Blue / Green" naming that risked
 * being mis-read as a deployment posture. Phase 13D.1 reframes the names to
 * make clear that the planned switcher would change which static **data**
 * the frontend reads — never which environment / instance / host serves it.
 */
export interface DataSourceSnapshot {
  /** Stable id, used as React key. */
  id: string;
  /** Display label ("Demo", "Active", "Candidate"). */
  label: string;
  /** Whether this is the data source the current build reads. */
  current: boolean;
  /** Whether this snapshot represents future, planned work. */
  future: boolean;
  /** Description of what the snapshot would contain. */
  description: string;
}

export const DATA_SOURCE_SNAPSHOTS: readonly DataSourceSnapshot[] = [
  {
    id: "demo",
    label: "Demo",
    current: true,
    future: false,
    description:
      "The bundled portfolio dataset. Committed at " +
      "`frontend/src/data/storytime-demo-export.json` with a frozen " +
      "schemaVersion. This is what the current build of the frontend " +
      "reads.",
  },
  {
    id: "active",
    label: "Active",
    current: false,
    future: true,
    description:
      "The (future) current local / operator export snapshot. Would be " +
      "produced by `storytime export-demo-ui` against a reviewer's own " +
      "local pipeline runs and loaded read-only into the frontend. Not " +
      "yet implemented.",
  },
  {
    id: "candidate",
    label: "Candidate",
    current: false,
    future: true,
    description:
      "The (future) candidate / alternate export snapshot. Would let a " +
      "reviewer compare two locally-produced snapshots side by side, " +
      "still read-only. Not yet implemented.",
  },
] as const;

/**
 * Standing framing copy for the Data Source card in the Evidence view.
 * Names "Active" and "Candidate" explicitly to head off the older
 * blue/green misreading captured in the deferred-work register.
 */
export const DATA_SOURCE_FRAMING = {
  heading: "Data source — Demo Snapshot",
  body:
    "The current build reads the bundled Demo Snapshot. Active and " +
    "Candidate, listed below, are **data snapshots**, not deployment " +
    "environments. They describe planned read-only data sources a future " +
    "subphase could let a reviewer load locally — they do not describe " +
    "blue/green hosts, traffic-shifting, or any production deployment " +
    "posture. No snapshot switching, promotion, or backend mutation is " +
    "implemented in Phase 13D.1.",
  diagramCaption:
    "Switching between Demo, Active, and Candidate is intentionally future " +
    "work. Reviewing the current artifact only requires Demo.",
} as const;

/* ──────────────────── small static facts for the "scope" line ─────────── */

/**
 * Static descriptive counts derived from the locked Phase 13C export.
 * These are not live values — they describe the bundled Demo Snapshot at
 * build time. The export module that produced them is byte-identical to
 * the Phase 13D source.
 */
export const EVIDENCE_EXPORT_FACTS = {
  schemaVersion: EXPORT_META.schemaVersion,
  generatedBy: EXPORT_META.generatedBy,
  exportKind: EXPORT_META.exportKind,
  runCount: DEMO_RUN_DETAILS.length,
  runSummaryCount: DEMO_RUN_SUMMARIES.length,
  failureQueueCount: DEMO_FAILURE_QUEUE.length,
  governanceRowCount: GOVERNANCE_RUN_ROWS.length,
} as const;

/* ──────────────────── view-level talking points ────────────────────── */

/**
 * Short, plain-language talking points the Evidence view shows beneath the
 * categories. They restate the boundary in conversational form.
 */
export const EVIDENCE_TALKING_POINTS: readonly string[] = [
  "This static portfolio view points reviewers to validation evidence preserved in the repository.",
  "The GUI does not rerun tests. The evidence shown here is static, not a live CI dashboard.",
  "Each repository reference below is a path inside the artifact you are looking at — open it in your editor.",
  "Counts come from the bundled Demo Snapshot only; they describe build-time facts, not live system state.",
  "Active and Candidate are data snapshots, not deployment environments — see the Data Source card.",
] as const;
