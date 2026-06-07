"""Telemetry attribute names — OTel-free constants.

ARCH-LOCK: Telemetry Import Boundary (see storytime.adapters.telemetry.base)
DO NOT REFACTOR: This module declares the StoryTime span/metric attribute
vocabulary as plain strings. It deliberately does NOT import opentelemetry, so
the runner, the approval service, and the rehydration code can name a span or
metric attribute without coupling to the OpenTelemetry SDK. The SDK-level work
of attaching these to real spans stays in storytime.adapters.telemetry.otel,
the sole OpenTelemetry module.

Two design rules are baked into this vocabulary:

* It is intentionally *low cardinality*. ``pipeline.run_id`` is the single
  unbounded attribute and it belongs on spans only, never on a metric label
  (an unbounded label would explode a metric's time-series count).
* It carries no process identity. There is deliberately no hostname, working
  directory, or absolute-path attribute here: trace/metric identity must not
  depend on where the process happens to run (Phase 7 blue/green compat).

Resource-level attributes (``service.name``, ``service.version``,
``deployment.environment``, ``deployment.slot``) are *not* listed here — they
are set once on the OpenTelemetry ``Resource`` inside the OTel adapter from
immutable config, never per span.
"""

from __future__ import annotations

# -- pipeline span/metric attributes -----------------------------------------

# The durable correlation key. Present on every pipeline.run and pipeline.stage
# span. Unbounded — spans only, NEVER a metric label.
ATTR_PIPELINE_RUN_ID = "pipeline.run_id"

# The stage name (a closed set: ingest / synthesize / assemble / publish /
# approve_text / approve_audio). Safe as a span attribute and a metric label.
ATTR_PIPELINE_STAGE = "pipeline.stage"

# The terminal status of a stage or run span ("succeeded" / "failed" /
# "awaiting_approval"). Set when the span ends.
ATTR_PIPELINE_STATUS = "pipeline.status"

# "true" when the span belongs to a resumed (rehydrated) run, "false" for a
# straight-through run. Lets a query separate fresh runs from resumes.
ATTR_PIPELINE_RESUME = "pipeline.resume"

# The operator-facing gate label ("text" / "audio") — set on an approval-gate
# stage span only.
ATTR_APPROVAL_STAGE = "pipeline.approval.stage"

# The recorded operator decision at an approval gate ("approved" / "rejected"
# / "pending") — set on an approval-gate stage span when the decision is known.
ATTR_APPROVAL_DECISION = "pipeline.approval.decision"

# -- stage-contributed span attributes ---------------------------------------
# A stage may return these in StageResult.span_attributes. They are plain,
# low-cardinality strings; a stage never imports OpenTelemetry to set them.

# The kind of artifact a stage produced ("text.plain" / "audio.wav" /
# "audio.mp3" / "episode.metadata").
ATTR_ARTIFACT_KIND = "artifact.kind"

# The artifact-envelope schema version a stage wrote (a small integer string).
ATTR_ARTIFACT_VERSION = "artifact.version"

# "true" if the produced artifact envelope carries a payload SHA-256. The full
# hash is deliberately NOT a routine span attribute (high cardinality, no
# query value); presence is enough for an at-a-glance integrity check.
ATTR_ARTIFACT_HASH_PRESENT = "artifact.hash_present"

# The TTS adapter name used by synthesize ("mock" / "piper" / ...).
ATTR_TTS_ADAPTER = "tts.adapter"

# The audio container format a stage emitted ("wav" / "mp3").
ATTR_AUDIO_FORMAT = "audio.format"

# The number of items in the RSS feed publish wrote. Bounded small integer.
ATTR_RSS_ITEM_COUNT = "rss.item_count"

# -- error attributes --------------------------------------------------------

# A short, low-cardinality error discriminant (e.g. "TextHashMismatch"). Safe.
ATTR_ERROR_KIND = "error.kind"

# A human-readable error message. The OTel adapter sanitises this before it
# reaches a span (absolute paths redacted, length bounded) — see
# storytime.adapters.telemetry.hygiene.
ATTR_ERROR_MESSAGE = "error.message"

# -- metric label keys -------------------------------------------------------

# pipeline_runs_total label: "run" | "resume" | "stage".
LABEL_MODE = "mode"

# pipeline_approvals_total labels.
LABEL_GATE = "gate"
LABEL_DECISION = "decision"

# pipeline_artifact_validation_failed_total label: a small fixed reason set.
LABEL_REASON = "reason"


__all__ = [
    "ATTR_APPROVAL_DECISION",
    "ATTR_APPROVAL_STAGE",
    "ATTR_ARTIFACT_HASH_PRESENT",
    "ATTR_ARTIFACT_KIND",
    "ATTR_ARTIFACT_VERSION",
    "ATTR_AUDIO_FORMAT",
    "ATTR_ERROR_KIND",
    "ATTR_ERROR_MESSAGE",
    "ATTR_PIPELINE_RESUME",
    "ATTR_PIPELINE_RUN_ID",
    "ATTR_PIPELINE_STAGE",
    "ATTR_PIPELINE_STATUS",
    "ATTR_RSS_ITEM_COUNT",
    "ATTR_TTS_ADAPTER",
    "LABEL_DECISION",
    "LABEL_GATE",
    "LABEL_MODE",
    "LABEL_REASON",
]
