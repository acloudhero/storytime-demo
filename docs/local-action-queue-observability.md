# Local Action Queue Observability (Phase 13F — future model, not implemented)

> **Status:** Architecture / contract baseline only. Phase 13F is an
> implementation candidate, pending review, **not locked**.
>
> - **Phase 13F does not implement the queue.**
> - **Phase 13F does not implement workers.**
> - **Phase 13F does not implement metrics exporters.**
> - **Phase 13F does not implement OpenTelemetry instrumentation.**
>
> The architecture must still define what must be observable *before* a queue is
> implemented. The user requirement is explicit: a queue that accepts local
> work but cannot reveal its depth, oldest-item age, in-flight count, failed
> count, or stuck-item state is not acceptable for StoryTime.

## 1. Why observability is a precondition, not an afterthought

A future asynchronous local action queue (needed because long-running pipeline
/ TTS actions must not block the browser — see
`docs/local-bridge-architecture.md` §15) must be observable from the very first
implementation. Designing the observable surface now prevents shipping a blind
queue later.

## 2. Required local queue gauges / point-in-time measurements

Concepts that the future queue must expose (names may be refined if a clearer
convention is defined, but the concepts must be present):

- `local_action_queue_depth` — number of queued (not yet started) actions.
- `local_action_in_flight_count` — number of currently executing actions.
- `local_action_completed_count` — completed actions (cumulative or windowed).
- `local_action_failed_count` — failed actions.
- `local_action_rejected_count` — rejected actions (validation / allowlist /
  precondition / duplicate).
- `local_action_dead_letter_count` — actions moved to the failure / dead-letter
  queue.
- `local_action_oldest_queued_age_seconds` — age of the oldest queued action.
- `local_action_longest_in_flight_age_seconds` — age of the longest-running
  in-flight action (stuck-action signal).
- `local_action_retry_count` — retries performed.
- `local_action_queue_capacity` — configured local load limit.
- `local_action_queue_saturation_ratio` — depth / capacity.
- `local_export_last_success_age_seconds` — age of the last successful export
  refresh.
- `local_export_last_failure_age_seconds` — age of the last failed export
  refresh.

## 3. Required local queue events / logs

- action accepted
- action rejected
- action started
- action completed
- action failed
- action cancelled
- action deduplicated by idempotency key
- export refresh started
- export refresh completed
- export refresh failed
- action moved to failure / dead-letter queue

## 4. Required local queue attributes

Attributes that should tag the events / measurements above:

- `action.request_id`
- `action.job_id`
- `action.name`
- `action.status`
- `action.target.run_id`
- `action.target.stage_id`
- `workspace.id`
- `workspace.slot`
- `storage.target_type`
- `idempotency_key`
- `execution_timing`
- `queue.name`
- `queue.depth`
- `retry.count`

## 5. Load limiting (local mode)

- Local mode should start with a **fixed conservative concurrency** limit.
- **One long-running pipeline action at a time** is acceptable for the first
  implementation.
- Validation-only actions may be **fast-path** if clearly safe.
- Excess requests should be **rejected or queued** according to an explicit,
  documented policy — with explicit backpressure.
- Duplicate requests must be guarded by **idempotency keys**.
- The UI must be able to **explain backpressure** (why a request was deferred /
  rejected), using the gauges above.
- **Local mode should not attempt autoscaling**; it prefers predictable safety
  over throughput.

## 6. Stuck-action detection

`local_action_longest_in_flight_age_seconds` crossing a threshold is the
stuck-action signal. The future implementation must be able to surface a stuck
action (and allow cancel / dead-letter), not silently hang.

## 7. Distributed / Cloud carry-forward

The same concepts map cleanly to a future distributed / cloud mode so the local
observability model is not throwaway:

- queue depth → per-queue / per-pool depth,
- queue age → oldest-item age across the fleet,
- worker saturation → in-flight vs worker-pool capacity,
- action failure rate → error-rate SLO signal,
- retry rate → retry-storm detection,
- dead-letter count → alerting signal,
- export refresh latency → freshness SLO,
- autoscaling signals → derived from depth + age + saturation,
- alert / SLO signals → derived from failure rate + freshness.

Queue metrics should be designed so they map cleanly from local observability
to distributed observability later.

## 8. Explicit non-implementation

- Do not implement async workers (Phase 13F).
- Do not implement polling (Phase 13F).
- Do not implement job-queue code (Phase 13F).
- Do not implement OpenTelemetry instrumentation (Phase 13F).
- Do not implement metrics exporters (Phase 13F).
- Do not introduce a metrics backend (Phase 13F).
- Do not design provider-specific cloud implementation (Phase 13F).

This document is the observability contract a later phase must satisfy before
its queue is considered acceptable.
