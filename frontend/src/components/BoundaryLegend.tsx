/**
 * BoundaryLegend — Phase 13J compact boundary legend.
 *
 * A single scannable row that names the three authority/data kinds a reviewer
 * needs to keep distinct: the static demo snapshot, backend-owned local-bridge
 * execution, and the governed backend proof's artifact evidence. Presentational
 * only; sourced from {@link BOUNDARY_LEGEND}.
 */

import { BOUNDARY_LEGEND } from "../data/operatorConsole";
import { ConsoleBadge } from "./ConsoleBadge";
import styles from "./consolePolish.module.css";

export function BoundaryLegend(): JSX.Element {
  return (
    <div
      className={styles.legend}
      role="group"
      aria-label="Data and authority boundaries"
    >
      {BOUNDARY_LEGEND.map((entry) => (
        <div className={styles.legend__item} key={entry.label}>
          <ConsoleBadge tone={entry.tone} label={entry.label} />
          <p className={styles.legend__blurb}>{entry.blurb}</p>
        </div>
      ))}
    </div>
  );
}
