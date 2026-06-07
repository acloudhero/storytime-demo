/**
 * DemoWalkthroughView — Demo Walkthrough / Reviewer Story Path view.
 *
 * A real read-only view (refreshed in Phase 13K to tell the governed
 * local-chain story and stay consistent with the canonical written
 * walkthrough, docs/demo-walkthrough.md). It is a presentation shell over
 * `demoWalkthroughAdapter`
 * — the adapter holds the long-form content (route definitions, step
 * notes, architecture checkpoints, deferred-work explanations, talking
 * points, repository references), and this component renders it.
 *
 * Navigation between routes uses a plain `useState<RouteId>` segmented
 * control inside the view; no router, no Context, no persistence, no
 * URL params, no localStorage. Each route step renders a "Go to {view}"
 * button that calls back into the App-level navigation via the
 * `onNavigate` / `onInspectRun` callbacks; the user leaves the
 * Walkthrough view and can return through the main nav.
 *
 * The view contains no `fetch`/`axios`/network call, no mutation, no
 * dynamic file loading. It is static.
 */

import { useState } from "react";
import type { View } from "../navigation";
import {
  ARCHITECTURE_CHECKPOINTS,
  DEFERRED_ITEMS,
  HEADER,
  INTERVIEW_TALKING_POINTS,
  REPOSITORY_REFERENCES,
  ROUTES,
  type Route,
  type RouteId,
  type WalkthroughStep,
} from "../data/demoWalkthroughAdapter";
import styles from "./DemoWalkthroughView.module.css";

export interface DemoWalkthroughViewProps {
  /** Switch to a top-level view in the App. */
  readonly onNavigate: (view: View) => void;
  /** Open the Pipeline Run Detail view focused on `runId`. */
  readonly onInspectRun: (runId: string) => void;
}

function StepCard({
  step,
  onNavigate,
  onInspectRun,
}: {
  readonly step: WalkthroughStep;
  readonly onNavigate: (view: View) => void;
  readonly onInspectRun: (runId: string) => void;
}): JSX.Element {
  const handleGo = (): void => {
    if (step.inspectRunId !== undefined) {
      onInspectRun(step.inspectRunId);
    } else {
      onNavigate(step.targetView);
    }
  };

  const buttonLabel =
    step.inspectRunId !== undefined
      ? `Open ${step.targetLabel} for this run →`
      : `Go to ${step.targetLabel} →`;

  return (
    <article className={styles.stepCard}>
      <header className={styles.stepHead}>
        <h3 className={styles.stepTitle}>{step.title}</h3>
        <span className={styles.stepBadge}>{step.targetLabel}</span>
      </header>
      {step.runContext !== undefined ? (
        <p className={styles.stepRunContext}>{step.runContext}</p>
      ) : null}
      <dl className={styles.stepDetail}>
        <dt>What to inspect</dt>
        <dd>{step.whatToInspect}</dd>
        <dt>What it proves</dt>
        <dd>{step.whatItProves}</dd>
      </dl>
      <ul className={styles.stepTalkingPoints} aria-label="Talking points">
        {step.talkingPoints.map((point, idx) => (
          <li key={idx}>{point}</li>
        ))}
      </ul>
      <div className={styles.stepActions}>
        <button
          type="button"
          className={styles.stepNavBtn}
          onClick={handleGo}
        >
          {buttonLabel}
        </button>
      </div>
    </article>
  );
}

function RouteSection({
  route,
  onNavigate,
  onInspectRun,
}: {
  readonly route: Route;
  readonly onNavigate: (view: View) => void;
  readonly onInspectRun: (runId: string) => void;
}): JSX.Element {
  return (
    <section className={styles.routeSection} aria-labelledby="active-route-heading">
      <header className={styles.routeHead}>
        <h2 id="active-route-heading" className={styles.routeTitle}>
          {route.label}
        </h2>
        <span className={styles.routeMeta}>
          {route.purpose} · about {route.approximateMinutes} min ·{" "}
          {route.steps.length} stop{route.steps.length === 1 ? "" : "s"}
        </span>
      </header>
      <p className={styles.routeIntro}>{route.intro}</p>
      <ol className={styles.stepList}>
        {route.steps.map((step) => (
          <li key={step.id} className={styles.stepListItem}>
            <StepCard
              step={step}
              onNavigate={onNavigate}
              onInspectRun={onInspectRun}
            />
          </li>
        ))}
      </ol>
    </section>
  );
}

export function DemoWalkthroughView({
  onNavigate,
  onInspectRun,
}: DemoWalkthroughViewProps): JSX.Element {
  const [activeRoute, setActiveRoute] = useState<RouteId>("ten-min");
  // ROUTES is statically non-empty (defined in demoWalkthroughAdapter with
  // four entries) — the non-null assertion narrows past the
  // noUncheckedIndexedAccess strict-mode warning. The ?? fallback then
  // guarantees a Route, never undefined, even if a future RouteId is added
  // to the union without a matching ROUTES entry.
  const fallbackRoute = ROUTES[0]!;
  const route =
    ROUTES.find((r) => r.id === activeRoute) ?? fallbackRoute;

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <p className={styles.eyebrow}>{HEADER.eyebrow}</p>
        <h1 className={styles.title}>{HEADER.title}</h1>
        <p className={styles.lede}>{HEADER.lede}</p>
      </header>

      <div
        className={styles.tabBar}
        role="tablist"
        aria-label="Walkthrough routes"
      >
        {ROUTES.map((r) => {
          const isActive = r.id === activeRoute;
          return (
            <button
              key={r.id}
              type="button"
              role="tab"
              aria-selected={isActive}
              className={
                isActive
                  ? `${styles.tab} ${styles.tabActive}`
                  : styles.tab
              }
              onClick={() => setActiveRoute(r.id)}
            >
              <span className={styles.tabLabel}>{r.label}</span>
              <span className={styles.tabSubLabel}>
                ~{r.approximateMinutes} min
              </span>
            </button>
          );
        })}
      </div>

      <RouteSection
        route={route}
        onNavigate={onNavigate}
        onInspectRun={onInspectRun}
      />

      <section
        className={styles.section}
        aria-labelledby="architecture-checkpoints-heading"
      >
        <header className={styles.sectionHead}>
          <h2
            id="architecture-checkpoints-heading"
            className={styles.sectionTitle}
          >
            Architecture checkpoints
          </h2>
          <p className={styles.sectionSubtitle}>
            Short cards that explain the system boundary behind what you just
            clicked through, embedded here rather than in a separate page.
          </p>
        </header>
        <div className={styles.checkpointGrid}>
          {ARCHITECTURE_CHECKPOINTS.map((cp) => (
            <article key={cp.id} className={styles.checkpointCard}>
              <h3 className={styles.checkpointTitle}>{cp.title}</h3>
              <p className={styles.checkpointBody}>{cp.summary}</p>
              <ul className={styles.checkpointEvidence}>
                {cp.inspectableEvidence.map((line, idx) => (
                  <li key={idx}>{line}</li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      </section>

      <section
        className={styles.section}
        aria-labelledby="deferred-heading"
      >
        <header className={styles.sectionHead}>
          <h2 id="deferred-heading" className={styles.sectionTitle}>
            What is intentionally deferred
          </h2>
          <p className={styles.sectionSubtitle}>
            Named, not hidden. Every deferred item below is tracked in{" "}
            <code className={styles.pathCode}>
              docs/frontend-gui-deferred-work-register.md
            </code>{" "}
            and gated behind its own review round.
          </p>
        </header>
        <ul className={styles.deferredList}>
          {DEFERRED_ITEMS.map((item) => (
            <li key={item.id} className={styles.deferredItem}>
              <span className={styles.deferredTitle}>{item.title}</span>
              <span className={styles.deferredBody}>{item.explanation}</span>
            </li>
          ))}
        </ul>
      </section>

      <section
        className={styles.section}
        aria-labelledby="talking-points-heading"
      >
        <header className={styles.sectionHead}>
          <h2 id="talking-points-heading" className={styles.sectionTitle}>
            Interview / SE demo talking points
          </h2>
          <p className={styles.sectionSubtitle}>
            Scannable callout cards. Each one is anchored to something you can
            actually inspect in the GUI or the repository.
          </p>
        </header>
        <div className={styles.talkingPointGrid}>
          {INTERVIEW_TALKING_POINTS.map((tp) => (
            <article key={tp.id} className={styles.talkingPointCard}>
              <h3 className={styles.talkingPointLabel}>{tp.label}</h3>
              <p className={styles.talkingPointBody}>{tp.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className={styles.section} aria-labelledby="refs-heading">
        <header className={styles.sectionHead}>
          <h2 id="refs-heading" className={styles.sectionTitle}>
            Repository references
          </h2>
          <p className={styles.sectionSubtitle}>
            Open these files directly to verify any claim above. The
            walkthrough deliberately points at real artifacts rather than
            paraphrasing them.
          </p>
        </header>
        <ul className={styles.refList}>
          {REPOSITORY_REFERENCES.map((ref) => (
            <li key={ref.path} className={styles.refItem}>
              <span className={styles.refLabel}>{ref.label}</span>
              <code className={styles.pathCode}>{ref.path}</code>
              <span className={styles.refHint}>{ref.hint}</span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
