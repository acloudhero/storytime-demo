"""RunnerContext — the minimal frozen orchestration context.

ARCH-LOCK: RunnerContext is minimal and frozen
DO NOT REFACTOR: RunnerContext carries ONLY stable orchestration services:
config, clock, state store, telemetry adapter, storage adapter. Do NOT add
mutable per-stage business state, OTel Span objects, artifact payloads, or
stage outputs. Stage-specific adapters (e.g. a chosen TTS engine) are
constructor-injected into stages, not placed here (Round 5 clarification A1).
Rationale: Round 3 / Round 5 locked decision. This is the deliberate
counterweight to a mutable god-object PipelineContext.
"""

from __future__ import annotations

from dataclasses import dataclass

from storytime.adapters.storage import StorageAdapter
from storytime.adapters.telemetry import TelemetryAdapter
from storytime.config import StoryTimeConfig
from storytime.state import StateStore
from storytime.util.clock import Clock


@dataclass(frozen=True, slots=True)
class RunnerContext:
    """Stable services shared across stages for the lifetime of a process."""

    config: StoryTimeConfig
    clock: Clock
    state: StateStore
    telemetry: TelemetryAdapter
    storage: StorageAdapter
