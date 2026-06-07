/**
 * HomePage — the portfolio homepage / project overview.
 *
 * Goal: a hiring manager or reviewer understands StoryTime within ~60 seconds.
 * Content is sourced from the static `DEMO_PROJECT` summary. Tone is a high-end
 * engineering portfolio: precise, honest about limitations, not SaaS marketing.
 */

import { DEMO_PROJECT, EXPORT_META } from "../data/adapter";
import { BUILD_STATUS } from "../data/operatorConsole";
import { BoundaryLegend } from "./BoundaryLegend";
import { ModeOverview } from "./ModeOverview";

export function HomePage({
  onOpenRuns,
}: {
  onOpenRuns: () => void;
}): JSX.Element {
  const project = DEMO_PROJECT;

  return (
    <div className="stack">
      <header className="reveal reveal--1">
        <p className="eyebrow">Engineering portfolio · operator GUI foundation</p>
        <h1 className="page-title">{project.name}</h1>
        <p className="lede">{project.tagline}</p>
      </header>

      <section className="reveal reveal--2 stack">
        <p style={{ maxWidth: "62ch" }}>{project.description}</p>
        <div className="callout">
          <strong>Read this site as a static shell.</strong> By default it is a
          read-only portfolio and operator console backed entirely by a
          deterministic static export — no backend connection, no live data, and
          no mutations. The optional Local Bridge surface adds backend-owned,
          loopback-only observability and one controlled retry action, and the
          governed local TTS proof appears as read-only artifact evidence. A
          good first stop is the{" "}
          <button
            type="button"
            className="linklike"
            onClick={onOpenRuns}
            style={{
              background: "none",
              border: 0,
              padding: 0,
              font: "inherit",
              color: "var(--signal-deep)",
              textDecoration: "underline",
              cursor: "pointer",
            }}
          >
            Pipeline Run Detail view
          </button>
          .
        </div>
      </section>

      <section className="reveal reveal--2 stack">
        <h2 className="section-title">How to read this console</h2>
        <p style={{ maxWidth: "62ch" }}>
          Four surfaces, three boundaries. The legend names what is static demo
          data, what is backend-owned local execution, and what is governed
          backend proof; the cards below summarize each mode.
        </p>
        <BoundaryLegend />
        <ModeOverview />
      </section>

      <section className="reveal reveal--3">
        <h2 className="section-title">What it demonstrates</h2>
        <div className="card-grid">
          {project.demonstrates.map((point, index) => (
            <article className="feature" key={index}>
              <h3>Point {index + 1}</h3>
              <p>{point}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="reveal reveal--3">
        <h2 className="section-title">Observability &amp; governance value</h2>
        <p style={{ maxWidth: "62ch" }}>
          StoryTime treats observability and governance as first-class, not
          afterthoughts. Every run is traceable through OpenTelemetry
          instrumentation and dashboards-as-code, and every run passes a
          fail-closed governance gate: a human-decided, durably recorded Trust
          Envelope must authorize a source before any expensive stage runs.
          The pipeline is honest about what it is — it records a human's
          authorization decision; it does not perform legal automation.
        </p>
        <p style={{ maxWidth: "62ch" }}>
          StoryTime is local-first by design. It runs end to end on one machine
          with no cloud account, SQLite and on-disk artifact envelopes are the
          source of truth, and telemetry export is optional and off by default.
        </p>
      </section>

      <section className="reveal reveal--4">
        <h2 className="section-title">Honest about what this is not</h2>
        <ul className="honest-list">
          {project.notClaims.map((claim, index) => (
            <li key={index}>{claim}</li>
          ))}
        </ul>
      </section>

      <section className="reveal reveal--4 stack">
        <h2 className="section-title">Current capabilities &amp; boundaries</h2>
        <p style={{ maxWidth: "62ch" }}>{BUILD_STATUS.headline}</p>
        <div className="card-grid">
          <article className="feature">
            <h3>What works today</h3>
            <ul className="honest-list">
              {BUILD_STATUS.capabilities.map((capability, index) => (
                <li key={index}>{capability}</li>
              ))}
            </ul>
          </article>
          <article className="feature">
            <h3>Boundaries it keeps</h3>
            <ul className="honest-list">
              {BUILD_STATUS.boundaries.map((boundary, index) => (
                <li key={index}>{boundary}</li>
              ))}
            </ul>
          </article>
        </div>
        <div className="panel">
          <dl className="kv">
            <dt>Data source</dt>
            <dd>
              A deterministic, read-only static export —{" "}
              <code>src/data/storytime-demo-export.json</code>, produced by{" "}
              <code>{EXPORT_META.generatedBy}</code> (schema{" "}
              <span className="mono">{EXPORT_META.schemaVersion}</span>) and
              consumed through <code>src/data/adapter.ts</code>. No backend
              connection, no network.
            </dd>
            <dt>Snapshot generated by</dt>
            <dd className="mono">{project.currentPhase}</dd>
            <dt>Snapshot note</dt>
            <dd>{project.currentPhaseStatus}</dd>
          </dl>
        </div>
      </section>

      <section className="reveal reveal--4">
        <h2 className="section-title">Reviewer paths</h2>
        <div className="card-grid">
          {project.reviewerPaths.map((path) => (
            <article className="path" key={path.id}>
              <div className="path__head">
                <span className="path__audience">{path.audience}</span>
                <span className="path__budget">{path.timeBudget}</span>
              </div>
              <p className="path__summary">{path.summary}</p>
              <ol>
                {path.steps.map((step, index) => (
                  <li key={index}>{step}</li>
                ))}
              </ol>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
