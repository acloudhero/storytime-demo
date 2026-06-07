# StoryTime — Phase 14 Readiness Handoff (Cloud / Distributed)

**Status.** Written by **Phase 13L — Phase 13 Closure / Demo-Local Completion
Lock** (implementation candidate, pending review, **not locked**). **Phase 13K is
the last locked phase.** This is an **architecture-first, implementation-free**
brief for a future round. It does not begin Phase 14, designs nothing in detail,
and grants no authority to begin Phase 14.

```text
Next major phase:   Phase 14 — Cloud / Distributed
First sub-phase:    Phase 14A — Cloud/Distributed Architecture Baseline
Status:             NOT STARTED
```

Phase 14 may begin only **after** Phase 13 is explicitly closed — that is, after
Phase 13L completes the Phase Closure Protocol (GPT review, Gemini critique, any
cleanup, explicit user lock) and the user makes an explicit Phase 13 closure
decision. Until then Phase 14 is not authorized. See
[`docs/phase-closure-protocol.md`](phase-closure-protocol.md) and
[`docs/phase13-closure.md`](phase13-closure.md).

## The one non-negotiable: preserve the Phase 13 discipline

Cloud/Distributed StoryTime must carry forward, unchanged, the safety model that
Phase 13 proved:

- The **browser remains an operator surface** — it observes and requests; it does
  not execute or store durable state.
- The **backend owns state and execution.** All real work happens server-side.
- **Providers and credentials never move into the browser.** No API keys, no
  provider SDKs, no signed-URL-minting secrets in client code.
- **Artifacts, manifests, and audit events remain backend-owned**, addressable,
  and verifiable.
- **Jobs become asynchronous and observable** — submission returns an accepted
  job reference; acceptance is not success; progress and outcome are queryable.
- **Governance and cost controls stay before expensive work**, exactly as the
  local governance/cost gate does today.
- **OpenTelemetry remains a first-class design axis** — traces, metrics, and logs
  are designed in, not bolted on.

If a future cloud design would violate any of these, that is a signal the design
is wrong, not that the discipline should bend.

## High-level questions the Phase 14A baseline must answer

These are framing questions for the future baseline round — not answers, and not
a design.

1. **What changes when StoryTime becomes live and distributed?** The single
   loopback bridge becomes a network API with real clients; one operator becomes
   many; one machine becomes many processes; manual reloads become event- or
   poll-driven reads against durable, shared state.
2. **What remains from the Phase 13 safety model?** Everything in the section
   above. The boundaries do not relax in the cloud — they get stricter.
3. **What new trust boundaries appear?** Client ↔ API authentication and
   authorization; tenant ↔ tenant isolation; API ↔ worker; worker ↔ provider;
   service ↔ object store; service ↔ database. Each needs an explicit contract.
4. **What state moves out of static export / SQLite / local files into cloud
   services?** Durable run/job/episode state → a managed database; artifacts and
   audio → object storage; the operator read model → a derived, cacheable
   projection rather than a committed static file.
5. **What becomes asynchronous and durable?** Generation, TTS, assembly, and
   publishing become durable queued jobs with retries, dead-lettering, and
   idempotency keys — generalizing today's `202 Accepted` retry boundary.
6. **What must remain impossible from the browser?** Triggering provider calls
   directly, holding credentials, executing commands, mutating durable state
   without going through the governed, authenticated, audited API, and reading
   another tenant's data.
7. **What is the minimum safe cloud golden path?** The smallest end-to-end slice
   — authenticated operator request → governed/cost-checked job submission →
   asynchronous worker → artifact in object storage → audit event → observable
   completion in the operator read model — with no provider secret ever near the
   browser.

## Proposed Phase 14 sequence (roadmap level — NOT locked, NOT started)

This is a **proposed** decomposition for future review only. It is not locked, it
is not authorized, and naming a sub-phase here does not start it. Each would be
its own candidate → review → lock cycle under the Phase Closure Protocol.

```text
Phase 14A — Cloud/Distributed Architecture Baseline        (next proposed baseline; NOT STARTED)
Phase 14B — Runtime State / Database Migration Plan
Phase 14C — Object Storage + Artifact Boundary
Phase 14D — Queue / Worker / Orchestrator Boundary
Phase 14E — Cloud API + Auth Boundary
Phase 14F — Cloud Operator Mode Read Model
Phase 14G — Cloud Observability Baseline
Phase 14H — First End-to-End Cloud Golden Path
Phase 14I — Cloud Failure / Retry / Recovery
Phase 14J — Cloud Demo Hardening
```

Like Phase 13A before it, **Phase 14A is expected to be a documentation-only
architecture-baseline round** — it would design the cloud/distributed shape on
paper and would not build it. Whether the sequence above is adopted, reordered,
or replaced is a decision for the Phase 14A round and its reviewers.

## What this handoff explicitly does NOT do

It does not add cloud deployment code, Docker/Kubernetes/Terraform/Helm
resources, cloud provider configuration, authentication, a database migration, an
object-storage integration, a queue/worker, a cloud API, or any runtime behavior.
It implements no part of Phase 14 and starts no part of Phase 14. It is a brief,
nothing more.
