/**
 * StaticDemoNotice — Phase 15C local-only notice for backend-dependent views.
 *
 * On the public static demo (`STATIC_DEMO_MODE`), the Local Bridge and Live
 * Proof Loop views are gated by this notice instead of mounting their live
 * loopback components, so the public demo makes no network call and shows no
 * generic error. It reuses the existing layout classes (`stack`, `eyebrow`,
 * `page-title`, `callout`, `note-muted`) — no new component system, no layout
 * change, no `alert()`.
 */

import { STATIC_DEMO_ACTION_MESSAGE } from "../data/demoMode";

export interface StaticDemoNoticeContent {
  /** The gated view's title (e.g. "Local Bridge"). */
  title: string;
  /** One honest sentence about what the view does in local execution. */
  localIntent: string;
  /** What the view does when the backend runs locally (loopback only). */
  localCapabilities: string[];
}

export function StaticDemoNotice({
  content,
}: {
  content: StaticDemoNoticeContent;
}): JSX.Element {
  return (
    <div className="stack">
      <header className="reveal reveal--1">
        <p className="eyebrow">Local-only · disabled in Static Demo</p>
        <h1 className="page-title">{content.title}</h1>
      </header>
      <div className="panel reveal reveal--2">
        <p className="callout">
          <strong>Static Demo mode.</strong> {STATIC_DEMO_ACTION_MESSAGE}
        </p>
        <p style={{ maxWidth: "60ch", margin: 0 }}>{content.localIntent}</p>
        <h3 className="sub-title">What this view does in local execution</h3>
        <ul>
          {content.localCapabilities.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
        <p className="note-muted" style={{ marginTop: "16px" }}>
          This view contacts a backend you run on your own machine over an
          HTTP loopback origin (127.0.0.1 / localhost). The public demo shows a
          static snapshot; cloud backend execution is deferred to a later
          phase. Every other view here is backed by the committed demo
          snapshot and needs no backend.
        </p>
      </div>
    </div>
  );
}
