# StoryTime Demo Seed Data / Golden Path Fixtures

This directory holds the **Phase 10F** curated demo seed data and golden-path
fixture scenarios. They let an operator demonstrate the existing StoryTime
pipeline, operator report, failure queue, Trust Envelope governance, and
`storytime rerun` command reproducibly, from a clean local environment.

These are **inputs and descriptions**, not generated runtime artifacts. They
do not add product features, do not change pipeline behaviour, and do not fake
a success path — every scenario drives the real existing system.

## Layout

```
demo/
  README.md                       this file
  seed/                           demo source texts + schema-valid manifests
    demo-golden-path.{txt,json}
    demo-retryable-failure.{txt,json}
    demo-governance-blocked.{txt,json}
    demo-needs-review.{txt,json}
  governance/
    demo-blocked-sources.yaml      demo-only deny-list for the blocked scenario
  fixtures/
    index.yaml                     the fixture-set index
    01-successful-golden-path.yaml
    02-retryable-technical-failure.yaml
    03-governance-blocked.yaml
    04-needs-review-approval-gate.yaml
    05-rerun-requested.yaml
    06-completed-after-rerun.yaml
```

## Content licensing

Every demo seed text is **original text written for StoryTime demo fixtures**
and dedicated to the public domain under **CC0-1.0**. No external, copyrighted,
or ambiguously-licensed text is included. Each fixture definition records the
content's licensing basis and the governance decision it is expected to
produce.

## Running the demo

The operator runbook is **[`docs/demo.md`](../docs/demo.md)**. It walks through
the successful path, the governance-blocked path, the failure-queue path, the
re-run request path, and the report-inspection path, with the exact local
commands for each. The runbook is local-first: it needs no cloud account, no
paid APIs, and no external services, and it checks in no generated audio.
