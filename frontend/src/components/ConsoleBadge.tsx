/**
 * ConsoleBadge — Phase 13J shared tone badge.
 *
 * A small, purely presentational pill that maps a {@link ConsoleTone} to one
 * of the established semantic palettes. It carries a text label and a shape
 * (the dot) so state is never communicated by colour alone. It is not a
 * control: it has no role, no handler, and no interactive affordance.
 */

import type { ConsoleTone } from "../data/operatorConsole";
import styles from "./consolePolish.module.css";

function toneClass(tone: ConsoleTone): string | undefined {
  switch (tone) {
    case "demo":
      return styles.toneDemo;
    case "local":
      return styles.toneLocal;
    case "proof":
      return styles.toneProof;
    case "reload":
      return styles.toneReload;
  }
}

export function ConsoleBadge({
  tone,
  label,
}: {
  tone: ConsoleTone;
  label: string;
}): JSX.Element {
  return (
    <span className={`${styles.badge} ${toneClass(tone)}`}>
      <span className={styles.badgeDot} aria-hidden="true" />
      {label}
    </span>
  );
}
