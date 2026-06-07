/**
 * navigation — Phase 13D.2 nav metadata helper.
 *
 * Extracts the static nav-key definitions, labels, and placeholder copy
 * out of `App.tsx` so the App component stays small and the view
 * definitions are documented in one place. This is metadata only: no
 * router, no Context, no global state. `App.tsx` continues to hold its
 * plain `useState<View>` navigation, the `inspectRun(runId)` drill-down
 * callback, and (new in Phase 13D.2) an `onNavigate(view)` callback
 * passed to the Demo Walkthrough view so its in-page step buttons can
 * change views without a router.
 *
 * Phase 13D.2 promotes the **Demo Walkthrough** view from a placeholder
 * to a real view (`soon: false`). Demo Walkthrough sits next to
 * Evidence / Validation in the nav order so the real Phase 13B–13D.2
 * views form a contiguous group at the start of the nav, with the
 * remaining honest placeholders after them. The remaining placeholder
 * entries (Architecture Story, Roadmap, Settings) still point at Phase
 * 13E or later, because Phase 13D.2 is itself static / read-only and
 * not the right subphase for adding new live behaviour. The Settings
 * placeholder continues to describe the deferred Demo / Active /
 * Candidate snapshot selector.
 */

import type { PlaceholderContent } from "./components/Placeholder";

/* ─────────────────── view keys ─────────────────── */

/**
 * The exhaustive set of view keys the app's plain `useState` navigation
 * uses. Any new view must be added here and in the `App.renderView`
 * switch.
 */
export type View =
  | "home"
  | "runs"
  | "architecture"
  | "demo"
  | "evidence"
  | "governance"
  | "failure"
  | "bridge"
  | "liveproof"
  | "roadmap"
  | "settings";

/* ─────────────────── nav items ─────────────────── */

export interface NavItem {
  id: View;
  label: string;
  /** True for views that are placeholders for later subphases. */
  soon: boolean;
}

/**
 * Ordered nav list rendered into the site header. Order matters for
 * reviewers: the real Phase 13B–13D.2 views come first (Overview,
 * Pipeline Run Detail, Governance / Safety, Failure / Recovery,
 * Evidence / Validation, Demo Walkthrough), followed by the remaining
 * honest placeholders. Demo Walkthrough sits at the end of the real
 * group because it is the reviewer-facing entry point that links into
 * the other views.
 */
export const NAV: readonly NavItem[] = [
  { id: "home", label: "Overview", soon: false },
  { id: "runs", label: "Pipeline Run Detail", soon: false },
  { id: "governance", label: "Governance / Safety", soon: false },
  { id: "failure", label: "Failure / Recovery", soon: false },
  { id: "evidence", label: "Evidence / Validation", soon: false },
  { id: "demo", label: "Demo Walkthrough", soon: false },
  { id: "bridge", label: "Local Bridge", soon: false },
  { id: "liveproof", label: "Live Proof Loop", soon: false },
  { id: "architecture", label: "Architecture Story", soon: true },
  { id: "roadmap", label: "Roadmap", soon: true },
  { id: "settings", label: "Settings / Config", soon: true },
] as const;

/* ─────────────────── placeholder copy ─────────────────── */

/**
 * Static copy for the remaining placeholder views. Each placeholder
 * points at the subphase that would replace it; per Phase 13D.2, the
 * remaining views are all flagged for Phase 13E or later. The
 * Architecture Story placeholder copy reflects that Phase 13D.2 has
 * absorbed ~80–90% of the narrative into the Demo Walkthrough view's
 * embedded checkpoints, with a possible later standalone page still
 * tracked as deferred. The Settings placeholder still describes the
 * deferred Demo / Active / Candidate snapshot selector — Phase 13D.2
 * does not implement switching, only the static framing.
 */
export const PLACEHOLDERS: Record<string, PlaceholderContent> = {
  architecture: {
    eyebrow: "Portfolio section · planned",
    title: "Architecture Story",
    plannedPhase: "Phase 13E or later",
    intent:
      "A standalone architecture page would explain the system boundary " +
      "and the local-first design at greater depth than the embedded " +
      "checkpoints in the Demo Walkthrough. Phase 13D.2 already " +
      "absorbs about 80–90% of that narrative through the walkthrough " +
      "checkpoints; a fuller standalone page is deferred to a possible " +
      "later phase.",
    willInclude: [
      "A deeper system-boundary explanation that goes beyond the " +
        "embedded walkthrough checkpoints.",
      "A fuller local-first architecture write-up.",
      "A future cloud / hosting path explanation, framed as optional.",
      "Public portfolio polish and interview leave-behind material.",
      "A pointer back to the Demo Walkthrough as the primary entry " +
        "point.",
    ],
  },
  roadmap: {
    eyebrow: "Portfolio section · planned",
    title: "Roadmap",
    plannedPhase: "Phase 13E or later",
    intent:
      "The Phase 13 subphase roadmap (13A–13G), so a reviewer can see " +
      "how the portfolio website and operator GUI are being built " +
      "incrementally.",
    willInclude: [
      "The 13A–13G subphase decomposition and current status.",
      "What each subphase adds and what it deliberately defers.",
      "A pointer to docs/phase13-roadmap.md as the source of record.",
    ],
  },
  settings: {
    eyebrow: "Operator view · planned",
    title: "Settings / Config",
    plannedPhase: "Phase 13E or later",
    intent:
      "The data-snapshot selector (Demo / Active / Candidate) and " +
      "display preferences. In Phase 13D.2 the only snapshot is Demo " +
      "and no switching is implemented; Active and Candidate are data " +
      "snapshots, not deployment environments.",
    willInclude: [
      "A Demo / Active / Candidate data-snapshot selector once " +
        "additional read-only snapshots exist (browser-loaded, never " +
        "mutating).",
      "Display preferences for the operator views.",
      "An honest statement of which snapshots are actually available.",
    ],
  },
};
