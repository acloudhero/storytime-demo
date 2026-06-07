/**
 * App — the StoryTime operator-console shell.
 *
 * Navigation is plain React state (no router, no BrowserRouter, no server
 * rewrites) so the static build works from any static host or the local
 * filesystem. Phase 13D.2 promotes the **Demo Walkthrough** view from a
 * placeholder to a real read-only guided reviewer / demo path view
 * (`./components/DemoWalkthroughView`). The walkthrough takes two
 * App-level callbacks — `setView` (for switching top-level views) and
 * `inspectRun` (for opening Pipeline Run Detail focused on a stable
 * run id) — so its in-page step buttons can drive navigation without a
 * router. Otherwise this file is the same shape as Phase 13D.1.
 *
 * The remaining navigation entries (Architecture Story, Roadmap,
 * Settings) are honest placeholders for later Phase 13 subphases (Phase
 * 13E or later). The export from `EXPORT_META` is shown as a small
 * read-only chip in the header so a reviewer can see at a glance that
 * the data behind every view is a Demo Snapshot, not live state. The
 * Evidence / Validation view restates the same in detail and frames
 * Demo / Active / Candidate as data snapshots, not deployment
 * environments.
 */

import { useState } from "react";
import { DemoWalkthroughView } from "./components/DemoWalkthroughView";
import { EvidenceValidationView } from "./components/EvidenceValidationView";
import { FailureRecoveryView } from "./components/FailureRecoveryView";
import { GovernanceSafetyView } from "./components/GovernanceSafetyView";
import { HomePage } from "./components/HomePage";
import { LiveProofView } from "./components/LiveProofView";
import { LocalBridgeView } from "./components/LocalBridgeView";
import { PipelineRunDetailPage } from "./components/PipelineRunDetailPage";
import {
  Placeholder,
  type PlaceholderContent,
} from "./components/Placeholder";
import { StaticDemoNotice } from "./components/StaticDemoNotice";
import { EXPORT_META } from "./data/adapter";
import { STATIC_DEMO_DISCLAIMER, STATIC_DEMO_MODE } from "./data/demoMode";
import { NAV, PLACEHOLDERS, type View } from "./navigation";

export function App(): JSX.Element {
  const [view, setView] = useState<View>("home");
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);

  function inspectRun(runId: string): void {
    setSelectedRunId(runId);
    setView("runs");
  }

  function renderView(): JSX.Element {
    switch (view) {
      case "home":
        return <HomePage onOpenRuns={() => setView("runs")} />;
      case "runs":
        return (
          <PipelineRunDetailPage
            selectedRunId={selectedRunId}
            onSelectRun={setSelectedRunId}
          />
        );
      case "governance":
        return <GovernanceSafetyView onInspectRun={inspectRun} />;
      case "failure":
        return <FailureRecoveryView onInspectRun={inspectRun} />;
      case "evidence":
        return <EvidenceValidationView />;
      case "demo":
        return (
          <DemoWalkthroughView
            onNavigate={setView}
            onInspectRun={inspectRun}
          />
        );
      case "bridge":
        return STATIC_DEMO_MODE ? (
          <StaticDemoNotice
            content={{
              title: "Local Bridge",
              localIntent:
                "The Local Bridge is a read-only operator console over a " +
                "backend you run on your own machine: it shows health, " +
                "readiness, and a queue snapshot, and can submit a guarded " +
                "retry of a failed stage — all over an HTTP loopback origin.",
              localCapabilities: [
                "Read-only health and readiness probes against 127.0.0.1 / localhost.",
                "A queue snapshot reflecting the backend's durable state.",
                "A single guarded retry-failed-stage action, backend-decided and bounded.",
                "A manual reload of the committed static export (no backend needed).",
              ],
            }}
          />
        ) : (
          <LocalBridgeView />
        );
      case "liveproof":
        return STATIC_DEMO_MODE ? (
          <StaticDemoNotice
            content={{
              title: "Live Proof Loop",
              localIntent:
                "The Live Proof Loop runs a small end-to-end proof against a " +
                "backend on your own machine and shows the resulting run " +
                "detail — a live, local demonstration of the same contracts " +
                "the static snapshot describes.",
              localCapabilities: [
                "Health and run-list probes against an HTTP loopback origin.",
                "A bounded proof-fixture run that exercises the local pipeline.",
                "Read-only inspection of the produced run detail and stages.",
                "Loopback-only by design; it refuses non-local base URLs.",
              ],
            }}
          />
        ) : (
          <LiveProofView />
        );
      default: {
        const content = PLACEHOLDERS[view];
        return content ? (
          <Placeholder content={content} />
        ) : (
          <Placeholder
            content={PLACEHOLDERS.architecture as PlaceholderContent}
          />
        );
      }
    }
  }

  return (
    <div className="app">
      <div className="demo-banner" role="note">
        Static demo build · {STATIC_DEMO_DISCLAIMER}
      </div>

      <header className="site-header">
        <div className="site-header__inner">
          <div className="brand">
            <span className="brand__mark">
              Story<em>Time</em>
            </span>
            <span className="brand__tag">
              portfolio &amp; operator console
            </span>
            <span
              className="data-chip"
              title={`Schema ${EXPORT_META.schemaVersion} · ${EXPORT_META.generatedBy}`}
            >
              Data source · Demo Snapshot
            </span>
          </div>
          <nav className="site-nav" aria-label="Primary">
            {NAV.map((item) => (
              <button
                key={item.id}
                type="button"
                className={
                  item.soon
                    ? "site-nav__item site-nav__item--soon"
                    : "site-nav__item"
                }
                aria-current={view === item.id ? "page" : undefined}
                onClick={() => setView(item.id)}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="site-main" key={view}>
        {renderView()}
      </main>

      <footer className="site-footer">
        <div className="site-footer__inner">
          <span>
            StoryTime — a governed, observable, local-first content-to-audio
            pipeline with an operator console
          </span>
          <span>Static · read-only · demo data only</span>
        </div>
      </footer>
    </div>
  );
}
