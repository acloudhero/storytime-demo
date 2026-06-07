/**
 * TTSProofSummary — Phase 13J read-only governed-TTS-proof evidence.
 *
 * Explains the locked Phase 13I governed local TTS proof as READ-ONLY
 * understanding: provider mode (mock), the deferred/disabled real provider, the
 * approved-fixture and text-hash concepts, the artifact / manifest / audit
 * lifecycle, and the labeled cost estimate. It is purely presentational and
 * sourced from the frontend-owned {@link TTS_PROOF_SUMMARY} content.
 *
 * Critically, this component creates NO execution path: it has no Generate
 * button, no provider/credential/file/URL input, no fetch, no audio player, and
 * no handler of any kind. Generation remains backend/CLI-owned; the browser
 * cannot trigger it. The panel only describes the boundary.
 */

import { Fragment } from "react";
import { TTS_PROOF_SUMMARY, type TtsFact } from "../data/operatorConsole";
import styles from "./consolePolish.module.css";

function factDotClass(tone: TtsFact["tone"]): string | undefined {
  switch (tone) {
    case "ok":
      return styles.factOk;
    case "warn":
      return styles.factWarn;
    case "idle":
      return styles.factIdle;
  }
}

export function TTSProofSummary(): JSX.Element {
  const summary = TTS_PROOF_SUMMARY;
  return (
    <section
      className={styles.tts}
      aria-label="Governed local TTS proof — read-only evidence"
    >
      <div className={styles.tts__head}>
        <h2 className={styles.tts__title}>
          Governed local TTS proof — read-only evidence
        </h2>
        <span
          className={`${styles.badge} ${styles.toneProof} ${styles.tts__readonly}`}
        >
          <span className={styles.badgeDot} aria-hidden="true" />
          read-only
        </span>
      </div>

      <p className={styles.tts__intro}>{summary.intro}</p>

      <dl className={styles.tts__facts}>
        {summary.facts.map((fact) => (
          <Fragment key={fact.label}>
            <dt>{fact.label}</dt>
            <dd>
              <span
                className={`${styles.tts__factDot} ${factDotClass(fact.tone)}`}
                aria-hidden="true"
              />
              {fact.value}
            </dd>
          </Fragment>
        ))}
      </dl>

      <div>
        <p className={styles.tts__subhead}>Audit / event lifecycle</p>
        <ul className={styles.tts__lifecycle}>
          {summary.lifecycle.map((entry) => (
            <li className={styles.tts__event} key={entry.event}>
              <code className={styles.tts__eventName}>{entry.event}</code>
              <span>{entry.meaning}</span>
            </li>
          ))}
        </ul>
      </div>

      <div>
        <p className={styles.tts__subhead}>Ownership &amp; boundary</p>
        <ul className={styles.tts__ownership}>
          {summary.ownership.map((line, index) => (
            <li key={index}>{line}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}
