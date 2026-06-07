# StoryTime Product Charter

## 1. Product Definition

StoryTime is a local-first, CLI-driven, observability-native content-to-audio pipeline.

Its purpose is to convert approved CC0 or US public-domain text into podcast-ready audio, RSS feed artifacts, and traceable pipeline telemetry. The project is intentionally scoped as both a usable content pipeline and a disciplined engineering process proving ground for future projects.

StoryTime is not merely a podcast app. It is a controlled pipeline that turns source text into an audio publishing artifact while preserving provenance, licensing status, pipeline state, and observability signals from the beginning.

The product must remain small enough to build and verify in stages, but structured enough to support later cloud-native expansion.

The core product promise is:

> Given an approved source text, StoryTime can produce a podcast-ready audio artifact, an RSS feed artifact, and a traceable record of the pipeline journey.

The project begins local-first. It does not begin with cloud deployment, user accounts, hosted services, AI agents, automatic source discovery, marketplace features, or external API dependencies.

## 2. MVP Seed

The MVP seed is:

```text
One approved text in.
One audio file out.
One RSS item published.
One traceable journey showing the pipeline.
```

This seed is the atomic unit of correctness for StoryTime.

## 3. MVP Scope

The MVP is strictly limited to:
1.  **Ingestion:** Local file ingestion of CC0/US-PD text + manifest.
2.  **Approval:** A persisted approval step.
3.  **Synthesis:** Generation of a single-episode audio file (via mock or local engine).
4.  **Assembly:** RSS feed generation.
5.  **Observability:** Persistent pipeline state, event logs, and trace emission.

## 4. Non-Goals

The following are explicitly out of scope for the StoryTime MVP and Phase 1-2:
* Cloud deployment, synchronization, or hosting.
* User accounts, authentication, or multi-tenant show management.
* Automatic source discovery, web scraping, or social media integration.
* Monetization, marketplace features, or ad-injection.
* Recommendation engines or personalized discovery.
* Multi-voice, persona, or conversational casting features.

## 5. User/Operator Workflow

The operator interacts with StoryTime via the CLI:
1.  `storytime ingest <path_to_text>`
2.  `storytime approve <run_id>`
3.  `storytime synthesize <run_id>`
4.  `storytime assemble <run_id>`
5.  `storytime publish <run_id>` (Generates local RSS)

## 6. Legal/Licensing Boundaries

* StoryTime manifests are constrained to CC0 + US public domain.
* The system must validate these licenses and explicitly halt processing if an unknown, commercial, or unsupported license type is detected.

## 7. Source Material Rules

* All input text must be accompanied by a manifest file containing Title, Author, and License fields.
* The manifest must use a closed schema to prevent metadata drift.

## 8. Data Retention Assumptions

* Pipeline state is preserved on local disk.
* Failed runs are preserved with full stage/reason records for debugging.
* Future retention policies will be implemented as a separate automated cleanup step.

## 9. Security Assumptions

* Operating in a single-user, local environment.
* No internet access is required.
* Input data is trusted only after manifest validation.

## 10. Observability-Native Requirements

* `pipeline_run_id` is the durable product correlation key for all artifacts, spans, logs, and events.
* Internal events are data-only and persisted to the local SQLite `event_log` table before telemetry emission.
* OpenTelemetry is a view over the source of truth, not the source of truth itself.

## 11. Local-First Constraints

* No external API calls.
* No cloud dependencies.
* All state must reside on local disk.

## 12. Future Cloud-Native Expansion Path

* Phase 2 scaffolding uses interfaces that can be swapped for cloud-native providers (e.g., `S3Storage` instead of `LocalStorage`, `PubSubEventBus` instead of `SQLiteEvents`) in future projects.

## 13. Major Risks

* **Complexity Creep:** Expanding MVP scope prematurely.
* **Observability Overhead:** Instrumenting stages to the point where the business logic is obscured.
* **Serialization Overhead:** Maintaining strict DTO boundaries.

## 14. Open Questions

The Product Charter intentionally leaves implementation-specific decisions outside the charter itself. Tooling, package management, collector image versions, TTS engine selection, and scaffold-level dependency choices are tracked separately in `docs/open-issues.md`.

Stable product-level open questions:

1. How strict should StoryTime remain about source licensing after the MVP?
2. Should future versions support additional Creative Commons license types beyond CC0?
3. What level of attribution support will be required if non-CC0 licenses are introduced later?
4. What minimum level of audio quality is acceptable for a published episode?
5. What operator review steps are required before an episode can be considered publishable?
6. What retention rules should apply to failed pipeline runs versus published artifacts?
7. What observability views are most important for explaining the pipeline journey to a technical reviewer?
8. What parts of the process must remain local-first even after future cloud-native expansion?
9. What evidence should StoryTime preserve to prove that a source was approved before audio generation?
10. What public-facing documentation should be produced once the MVP works?

## 15. MVP Acceptance Criteria

The StoryTime MVP is accepted only when the software proves the product seed:

```text
One approved text in.
One audio file out.
One RSS item published.
One traceable journey showing the pipeline.
```

MVP acceptance criteria:

1. A local operator can run the pipeline from an explicit CLI command.
2. The pipeline can process a local text file and source manifest without requiring an internet connection.
3. No external API keys, cloud credentials, hosted databases, cloud TTS services, or remote storage services are required to execute an MVP pipeline run.
4. The source manifest is required before processing.
5. The system rejects missing manifests.
6. The system rejects unsupported, unknown, commercial, or non-approved license types.
7. The MVP allows only CC0 and US public-domain source material.
8. A valid source text and manifest can be associated with a durable pipeline_run_id.
9. The same pipeline_run_id correlates source metadata, stage records, artifact records, logs, telemetry events, and generated outputs.
10. OpenTelemetry trace IDs may be used for telemetry inspection, but pipeline_run_id remains the durable product correlation key.
11. A reviewer can follow the pipeline journey from source validation through audio generation or import, RSS artifact creation, and final output.
12. The pipeline produces a playable local audio artifact.
13. The pipeline produces a valid local RSS feed artifact containing the generated episode item.
14. The RSS item references the audio artifact with stable metadata.
15. Pipeline failures are recorded with the failed stage, reason, and pipeline_run_id.
16. Raw story text is not written into spans, telemetry attributes, or unbounded logs.
17. The MVP can be run and tested on a local development machine.
18. MockTTS or ManualImportTTS can satisfy the audio step before real TTS integration is required.
19. The operator can inspect generated artifacts after the run.
20. The operator can inspect the traceable journey through persisted events and/or local telemetry tooling.
21. The MVP does not require watcher automation, cloud deployment, vendor telemetry fan-out, user accounts, or hosted services.
22. The MVP remains within the non-goals defined in this charter.
23. The user explicitly approves the MVP result before the project advances beyond the MVP gate.
