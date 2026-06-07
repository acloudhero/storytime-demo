/**
 * demoMode — Phase 15C static-demo flag and canonical demo copy.
 *
 * The public deployment is a cloud-hosted **static** operator demo: there is
 * no backend behind it. `STATIC_DEMO_MODE` gates the two backend-dependent
 * views (Local Bridge, Live Proof Loop) so they never make a network call on
 * the public demo; the app renders a clear local-only notice instead. A
 * developer running the backend locally can set `STATIC_DEMO_MODE` to `false`
 * to use the live loopback views.
 *
 * The exact disclaimer string is required (verbatim) by the Phase 15C static
 * guard and by the demo docs, so it lives here as the single source of truth.
 */

/** True on the public static demo: no backend, backend-dependent views gated. */
export const STATIC_DEMO_MODE = true as const;

/** The exact, verbatim public-demo disclaimer (do not reword). */
export const STATIC_DEMO_DISCLAIMER =
  "This is a cloud-hosted static operator demo of a local-first, observability-native pipeline and its cloud-readiness seams.";

/** Message shown when a backend-dependent action is reached in static demo mode. */
export const STATIC_DEMO_ACTION_MESSAGE =
  "StoryTime is currently in Static Demo mode. In local execution, this action talks to the backend WorkQueue/API on your machine. Cloud backend execution is deferred to a later phase.";
