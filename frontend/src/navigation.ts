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
    eyebrow: "Portfolio section · deferred",
    title: "Architecture Story",
    plannedPhase: "Deferred after Phase 15C",
    intent:
      "This public demo currently presents the architecture through the " +
      "Overview, Demo Walkthrough, Evidence / Validation, Local Bridge, " +
      "and Live Proof Loop views. A fuller standalone Architecture Story " +
      "page is intentionally deferred so the public site remains honest: " +
      "this is a cloud-hosted static operator demo, not a live production " +
      "cloud backend.",
    willInclude: [
      "A deeper system-boundary explanation that expands on the current " +
        "walkthrough checkpoints.",
      "A fuller local-first architecture write-up.",
      "A cloud-readiness narrative covering runtime roles, queue, artifact, " +
        "observability, and recovery seams.",
      "A clear distinction between the current static demo and later cloud " +
        "backend runtime work.",
      "A pointer back to the Demo Walkthrough as the primary entry point.",
    ],
  },
  roadmap: {
    eyebrow: "Portfolio section · deferred",
    title: "Roadmap",
    plannedPhase: "Deferred after Phase 15C",
    intent:
      "A public roadmap page will summarize the completed local-first " +
      "operator proof, the locked Phase 15C static demo, and the planned " +
      "later cloud backend runtime path without implying that backend " +
      "cloud execution exists today.",
    willInclude: [
      "Completed milestones through the Phase 15C public static demo.",
      "The distinction between locked local-first proof, static public demo, " +
        "and future cloud backend runtime work.",
      "A concise next-phase path for Phase 15D and beyond.",
      "A pointer to docs/roadmap.md as the source of record.",
    ],
  },
  settings: {
    eyebrow: "Operator view · deferred",
    title: "Settings / Config",
    plannedPhase: "Deferred after Phase 15C",
    intent:
      "Settings and snapshot switching remain intentionally deferred. " +
      "The public site is a static, read-only demo snapshot. It does not " +
      "switch between live environments, does not contact a backend, and " +
      "does not expose runtime configuration.",
    willInclude: [
      "An honest read-only snapshot selector only after additional static " +
        "snapshots exist.",
      "Display preferences for operator views.",
      "A clear statement of which snapshots are available.",
      "No secrets, no backend mutation, and no public runtime configuration.",
    ],
  },
};