/**
 * Ambient type declaration for CSS Modules (`*.module.css`).
 *
 * Vite resolves `*.module.css` imports as objects whose keys are the
 * locally-scoped class names. This declaration tells the TypeScript strict
 * compiler the type of those imports so the Phase 13D `GovernanceSafetyView`
 * and `FailureRecoveryView` modules — which import their CSS as
 * module-scoped class maps — typecheck cleanly.
 *
 * Scope-of-introduction note: introduced in Phase 13D for the new component
 * stylesheets only. The Phase 13B/13C shell continues to use the existing
 * global `src/styles.css`; this declaration adds no behaviour to that file
 * and does not migrate any existing style.
 */

declare module "*.module.css" {
  const classes: { readonly [key: string]: string };
  export default classes;
}
