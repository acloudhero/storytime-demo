/**
 * Placeholder — an honest placeholder for portfolio sections and operator
 * views that later Phase 13 subphases will build. It states plainly that the
 * section is planned, names the subphase, and lists what it will contain. It
 * never claims functionality exists, and it stays deliberately lightweight.
 */

export interface PlaceholderContent {
  eyebrow: string;
  title: string;
  /** The Phase 13 subphase that will build this section. */
  plannedPhase: string;
  /** One honest sentence about what this section will become. */
  intent: string;
  /** A short list of what the built section will include. */
  willInclude: string[];
}

export function Placeholder({
  content,
}: {
  content: PlaceholderContent;
}): JSX.Element {
  return (
    <div className="stack">
      <header className="reveal reveal--1">
        <p className="eyebrow">{content.eyebrow}</p>
        <h1 className="page-title">{content.title}</h1>
      </header>
      <div className="placeholder reveal reveal--2">
        <span className="placeholder__phase">
          planned for {content.plannedPhase}
        </span>
        <p style={{ maxWidth: "60ch", margin: 0 }}>{content.intent}</p>
        <h3 className="sub-title">What this section will include</h3>
        <ul>
          {content.willInclude.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
        <p className="note-muted" style={{ marginTop: "16px" }}>
          This is a placeholder. Nothing on this page is implemented yet — it is
          shown so the intended structure of the StoryTime portfolio and
          operator GUI is visible during Phase 13C.
        </p>
      </div>
    </div>
  );
}
