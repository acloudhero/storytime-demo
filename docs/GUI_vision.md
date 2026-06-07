# GUI Vision — StoryTime Phase 13 Roadmap Note

**Date:** May 26, 2026  
**Roadmap tag:** Phase 13 — Operator GUI / Decoupled Frontend Vision  
**Purpose:** Preserve the user's GUI requirement and the mediator architecture response for future StoryTime roadmap planning.

---

## User Vision Statement

Look and feel / visibility / function control / access... I'm not a code for this guy The primary way that I interact with software is through GUI it's hard for me to fully visualize and internalize software system without a tactile interaction layer. We have to build that front end and it has to be decoupled from the back end in a way that it behaves the same whether the back end is cloud-based or local

---

## GPT-5.5 Response / Architecture Interpretation

Yes. That changes the priority.

You are not just trying to impress a reviewer. You need StoryTime to become **legible to you** as an operator. That means the GUI is not cosmetic. It is the missing human interaction layer.

The right framing is:

> StoryTime needs a decoupled operator console that can sit on top of either local or cloud backends without changing the user experience.

That is a real architectural requirement.

## The key principle

The frontend should **not know whether StoryTime is local or cloud-based**.

It should know only one thing:

```text
I talk to a StoryTime Control Plane through a stable contract.
```

That contract can be backed by:

```text
Local files
Local API
Containerized backend
Remote cloud API
Static demo JSON
```

But the GUI should behave the same.

This means the front end needs to be built around an abstraction like:

```text
StoryTime Operator API / Control Plane Contract
```

Not around direct access to Python internals.

## What has to exist before the GUI

Before building screens, StoryTime needs a **front-end contract layer**.

I would define it like this:

```text
Phase 13A — Operator Console Contract / GUI Architecture Baseline
```

This phase would not be “build the whole GUI.” It would define the stable interface the GUI depends on.

It should answer:

```text
What data does the GUI need?
Where does it come from?
What actions are allowed?
Which actions are read-only?
Which actions mutate backend state?
What works locally?
What works in cloud?
What is the same in both?
```

## The GUI architecture I recommend

The clean architecture is:

```text
Operator GUI
   ↓
StoryTime Client SDK / Adapter
   ↓
Control Plane Contract
   ↓
Backend Adapter
      ├── Local file adapter
      ├── Local API adapter
      └── Cloud API adapter later
```

The GUI should call something like:

```text
listPipelineRuns()
getPipelineRun(runId)
getTrustEnvelope(runId)
getFailureQueue()
getStaticReport(runId)
getObservabilityLinks(runId)
retryRun(runId)             later
approveGovernance(runId)    later
rejectGovernance(runId)     later
```

The GUI should **not** care whether those functions are reading from a local JSON file, a local FastAPI endpoint, or a cloud service.

## What the first GUI should show

For you, the first GUI should focus on visibility and tactile control.

The first screens should be:

```text
Dashboard
Pipeline Runs
Pipeline Run Detail
Failure Queue
Governance Review
Trust Envelope Viewer
Static Report Viewer
Settings / Backend Connection
```

The most important screen is **Pipeline Run Detail**.

That screen should make the system real:

```text
Story submitted
Rights checked
Text processed
Metadata generated
TTS stage
Audio stage
RSS publishing stage
Failure/retry state
Governance decision
Trace/report links
Operator next action
```

That is where you will finally be able to “feel” the software.

## Function control and access

This needs to be designed in layers.

### Layer 1: Read-only visibility

First GUI version:

```text
View runs
View status
View reports
View failures
View governance decisions
View observability links
```

No mutation risk.

### Layer 2: Safe operator actions

Second GUI version:

```text
Retry failed run
Re-run from stage
Open report
Copy RSS link
Export evidence
```

### Layer 3: Governance actions

Third GUI version:

```text
Approve
Reject
Block
Request review
Record operator note
```

### Layer 4: Admin/config actions

Later:

```text
TTS settings
Source settings
RSS settings
Backend mode
Cloud/local connection
Telemetry destination
```

This matters because you do **not** want the first GUI to become a dangerous control panel before the contract is mature.

## Local vs cloud behavior

To make it behave the same locally and in cloud, the GUI should use a backend-mode abstraction.

Something like:

```text
Backend Mode:
- Demo static
- Local runtime
- Cloud runtime
```

But the screens should not change.

Only the adapter changes.

Example:

```text
Demo static mode:
GUI reads sample JSON from /demo-data

Local runtime mode:
GUI calls http://localhost:8000/operator-api

Cloud runtime mode:
GUI calls https://storytime.example.com/operator-api
```

Same UI. Same data shapes. Same screens.

That is the decoupling you are describing.

## This affects the roadmap

I would not bury this inside Phase 12.

Phase 12 should close the portfolio/documentation layer.

Then Phase 13 should start GUI architecture.

Recommended sequence:

```text
Phase 12B — Portfolio Evidence Pack / Reviewer Assets
Phase 12C — Public Career Copy / Resume / LinkedIn Packaging
Phase 12D — Phase 12 Closure / GUI Readiness Handoff

Phase 13A — Operator Console Contract / GUI Architecture Baseline
Phase 13B — Read-Only Operator Console Shell
Phase 13C — Pipeline Run Detail + Trust Envelope Viewer
Phase 13D — Failure Queue + Static Report Viewer
Phase 13E — Safe Mutation Controls
Phase 13F — Local/Cloud Backend Adapter Hardening
```

## The first GUI phase should not start with React

This is important.

Do **not** start with “build me a React app.”

Start with:

```text
Define the operator console contract.
```

Then:

```text
Build the read-only UI against a mocked/static adapter.
```

That way the GUI can exist before the backend API is perfect, and the backend can evolve without breaking the UI.

## My strongest recommendation

After Phase 12 closes, start Phase 13 with this title:

```text
Phase 13A — Operator Console Contract / Decoupled GUI Architecture
```

Acceptance criteria should include:

```text
A stable frontend data contract
A local/static adapter strategy
A future cloud adapter strategy
A screen map
A function-control matrix
A read-only vs mutation boundary
A permissions/access model
A no-backend-rewrite rule
A no-cloud-assumption rule
```

That phase will let you build the GUI without losing the architecture discipline.

The GUI is not polish. It is the missing operator layer. It should become the primary way you experience StoryTime.

---

## Roadmap Tag

Tag this file as a future roadmap reference for:

```text
Phase 13 — Operator GUI / Decoupled Frontend
```

Recommended first subphase:

```text
Phase 13A — Operator Console Contract / Decoupled GUI Architecture
```
