/**
 * operatorConsole — Phase 13J reviewer-facing presentation content.
 *
 * Frontend-owned copy for the operator-console polish: the mode overview, the
 * boundary legend, the Local Bridge operator workflow, and the READ-ONLY
 * governed-TTS-proof summary. This is a *presentation adapter*: it is static,
 * frontend-owned reviewer copy that does NOT read the committed static export
 * contract and does NOT read any live artifact. It changes no contract and adds
 * no execution path.
 *
 * The TTS content here is deliberately conceptual and honest about the locked
 * Phase 13I governed proof: the provider is the deterministic mock, the real
 * provider is deferred / disabled (not bundled), generation is owned by the
 * backend CLI, and the browser cannot trigger it. None of this implies a
 * frontend control; it explains a backend boundary.
 */

/** Visual tone keys mapped to semantic badge styles in component CSS. */
export type ConsoleTone = "demo" | "local" | "proof" | "reload";

export interface ConsoleMode {
  id: string;
  label: string;
  tone: ConsoleTone;
  /** One scannable sentence. */
  oneLiner: string;
  /** Two to four short, honest facts. */
  points: readonly string[];
}

/**
 * The four operator-facing modes. Order is reviewer-first: what they see by
 * default (Demo), the optional local surface (Local Bridge), the governed
 * backend proof (TTS), and the manual refresh that ties them together.
 */
export const CONSOLE_MODES: readonly ConsoleMode[] = [
  {
    id: "demo",
    label: "Demo Mode",
    tone: "demo",
    oneLiner: "Static portfolio / reviewer view — safe and non-consequential.",
    points: [
      "Backed by a committed static export snapshot.",
      "Read-only by default; no backend required.",
      "A static snapshot, not a live sync.",
    ],
  },
  {
    id: "bridge",
    label: "Local Bridge",
    tone: "local",
    oneLiner: "Optional loopback bridge for controlled local actions.",
    points: [
      "The backend owns execution and state.",
      "One controlled action: retry a failed stage.",
      "Loopback only; no browser credentials.",
    ],
  },
  {
    id: "tts",
    label: "Governed Local TTS Proof",
    tone: "proof",
    oneLiner: "Mock-first backend chain that produces a local audio artifact.",
    points: [
      "Artifact + manifest + audit evidence.",
      "No frontend generation control.",
      "Real provider deferred / disabled (not bundled).",
    ],
  },
  {
    id: "reload",
    label: "Manual Snapshot Reload",
    tone: "reload",
    oneLiner: "Operator-triggered read-model refresh — never automatic.",
    points: [
      "Replaces only the in-memory read model.",
      "Not a live sync.",
      "Not proof that a job succeeded.",
    ],
  },
];

export interface BoundaryLegendEntry {
  label: string;
  tone: ConsoleTone;
  blurb: string;
}

/** A compact at-a-glance legend of the three authority/data kinds. */
export const BOUNDARY_LEGEND: readonly BoundaryLegendEntry[] = [
  {
    label: "Static demo",
    tone: "demo",
    blurb: "The committed snapshot the portfolio shows by default.",
  },
  {
    label: "Local bridge",
    tone: "local",
    blurb: "Backend-owned execution, observed over loopback.",
  },
  {
    label: "Backend proof",
    tone: "proof",
    blurb: "Artifact / manifest / audit evidence from the governed chain.",
  },
];

export interface OperatorStep {
  n: number;
  title: string;
  detail: string;
}

/** The natural local-operator reading order for the Local Bridge surface. */
export const OPERATOR_FLOW: readonly OperatorStep[] = [
  {
    n: 1,
    title: "Understand the current mode",
    detail:
      "You are in the static demo. Some surfaces below additionally need a " +
      "local bridge running on loopback.",
  },
  {
    n: 2,
    title: "Check bridge status / readiness",
    detail: "Probe the loopback bridge's health and readiness. Read-only.",
  },
  {
    n: 3,
    title: "Review the queue & action lifecycle",
    detail:
      "Inspect the queue snapshot and an existing action's lifecycle. " +
      "Read-only.",
  },
  {
    n: 4,
    title: "Submit a controlled retry",
    detail:
      "Where the bridge reports it as executable, submit exactly one " +
      "retry_failed_stage. This is the only submittable action.",
  },
  {
    n: 5,
    title: "Observe the lifecycle",
    detail:
      "Watch the submitted action's status. Acceptance is not success — a " +
      "202 means the request was queued, not that the job completed.",
  },
  {
    n: 6,
    title: "Manually reload the snapshot",
    detail:
      "Refresh the read model from the committed static export. This is a " +
      "manual read-model refresh, not a live sync.",
  },
  {
    n: 7,
    title: "Inspect the TTS proof evidence",
    detail:
      "Review the governed TTS proof's artifact / manifest / audit summary " +
      "below. Read-only — generation is backend/CLI-owned.",
  },
];

export interface TtsFact {
  label: string;
  value: string;
  tone: "ok" | "idle" | "warn";
}

export interface TtsLifecycleEntry {
  event: string;
  meaning: string;
}

/**
 * Read-only, conceptual evidence about the locked Phase 13I governed TTS proof.
 * Values are descriptive concepts, not live readings: the panel explains the
 * boundary, it does not fetch artifacts or trigger anything.
 */
export const TTS_PROOF_SUMMARY = {
  intro:
    "StoryTime can generate a local audio artifact through a governed, " +
    "observable, auditable backend boundary. This panel explains that proof " +
    "read-only — it triggers nothing.",
  facts: [
    { label: "Provider mode", value: "mock (deterministic)", tone: "ok" },
    {
      label: "Real provider",
      value: "not bundled · disabled · deferred",
      tone: "idle",
    },
    {
      label: "Approved fixture",
      value: "one allowlisted text fixture; identity recorded",
      tone: "ok",
    },
    {
      label: "Source text",
      value: "recorded as a SHA-256 hash + character count — never raw text",
      tone: "ok",
    },
    {
      label: "Artifact",
      value: "one atomic local WAV under a controlled directory",
      tone: "ok",
    },
    {
      label: "Manifest",
      value: "written beside the artifact (provider, hash, bytes, cost)",
      tone: "ok",
    },
    {
      label: "Cost",
      value: "a labeled estimate (configurable rate); never live pricing",
      tone: "warn",
    },
  ] as readonly TtsFact[],
  lifecycle: [
    { event: "tts.requested", meaning: "the governed run was requested" },
    {
      event: "tts.guard_rejected",
      meaning: "a guard rejected the run before any provider call",
    },
    { event: "tts.executing", meaning: "the mock provider is synthesizing" },
    {
      event: "tts.completed",
      meaning: "the artifact and manifest were written atomically",
    },
    {
      event: "tts.failed",
      meaning: "execution failed; no partial artifact is left behind",
    },
  ] as readonly TtsLifecycleEntry[],
  ownership: [
    "Generation is owned by the backend CLI (storytime tts-proof).",
    "The browser cannot trigger generation; this panel is read-only evidence.",
    "Mock output proves the governed boundary — it is not real provider audio.",
  ],
} as const;

/**
 * An honest, phase-light summary of what the system can do today and the
 * boundaries it keeps. Used on the overview so a reviewer reads capability and
 * boundaries together, rather than a stale phase number.
 */
export const BUILD_STATUS = {
  headline:
    "A governed, observable, local-first content-to-audio pipeline with a " +
    "professional operator console.",
  capabilities: [
    "Deterministic static demo export with read-only operator views.",
    "Loopback local-bridge observability plus one controlled retry action.",
    "Manual static-export snapshot reload (read model only).",
    "A governed mock-first local TTS proof: artifact, manifest, and audit evidence.",
  ],
  boundaries: [
    "Read-only by default; the backend owns execution and state.",
    "No browser credentials, no durable browser storage, no automatic sync.",
    "The real TTS provider is deferred; the browser cannot trigger generation.",
  ],
} as const;
