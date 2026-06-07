/**
 * OperatorWorkflow — Phase 13J local-operator workflow.
 *
 * Renders the natural seven-step local-operator reading order as a semantic
 * ordered list so the Local Bridge page sequence has an explicit story. The
 * visible number chip is decorative (the list itself carries the order for
 * assistive technology). Presentational only; sourced from
 * {@link OPERATOR_FLOW}. It triggers nothing — every real action stays in its
 * own panel below.
 */

import { OPERATOR_FLOW } from "../data/operatorConsole";
import styles from "./consolePolish.module.css";

export function OperatorWorkflow(): JSX.Element {
  return (
    <ol className={styles.flow}>
      {OPERATOR_FLOW.map((step) => (
        <li className={styles.flow__step} key={step.n}>
          <span className={styles.flow__num} aria-hidden="true">
            {step.n}
          </span>
          <div>
            <p className={styles.flow__title}>{step.title}</p>
            <p className={styles.flow__detail}>{step.detail}</p>
          </div>
        </li>
      ))}
    </ol>
  );
}
