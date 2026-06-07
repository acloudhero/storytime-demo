/**
 * ModeOverview — Phase 13J at-a-glance mode cards.
 *
 * Renders the four operator-facing modes (Demo, Local Bridge, Governed Local
 * TTS Proof, Manual Snapshot Reload) as scannable cards with a tone badge and
 * a few honest facts each. Purely presentational and sourced from the
 * frontend-owned {@link CONSOLE_MODES} content — it reads no live state and
 * exposes no control.
 */

import { CONSOLE_MODES, type ConsoleTone } from "../data/operatorConsole";
import { ConsoleBadge } from "./ConsoleBadge";
import styles from "./consolePolish.module.css";

const TONE_WORD: Record<ConsoleTone, string> = {
  demo: "static",
  local: "loopback",
  proof: "backend",
  reload: "manual",
};

export function ModeOverview(): JSX.Element {
  return (
    <div className={styles.modeGrid}>
      {CONSOLE_MODES.map((mode) => (
        <article className={styles.modeCard} key={mode.id}>
          <div className={styles.modeCard__head}>
            <h3 className={styles.modeCard__title}>{mode.label}</h3>
            <ConsoleBadge tone={mode.tone} label={TONE_WORD[mode.tone]} />
          </div>
          <p className={styles.modeCard__lead}>{mode.oneLiner}</p>
          <ul className={styles.modeCard__points}>
            {mode.points.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </article>
      ))}
    </div>
  );
}
