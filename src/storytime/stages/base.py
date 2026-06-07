"""Pipeline stage interface.

ARCH-LOCK: Stage Boundary
DO NOT REFACTOR: A Stage takes a RunnerContext (orchestration services) and a
serializable StageInput, and returns a StageResult. Stages do NOT call other
stages, do NOT write to SQLite directly, and do NOT import OpenTelemetry.
Rationale: Architecture Baseline sections 8-9. The PipelineRunner is the only
orchestrator; stages stay pure-ish, decoupled, and unit-testable.

RunnerContext is imported only for typing (TYPE_CHECKING) so the stages package
has no runtime dependency on the runner package.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from storytime.dto import StageInput, StageResult

if TYPE_CHECKING:
    from storytime.runner.context import RunnerContext


@runtime_checkable
class Stage(Protocol):
    """A single pipeline stage."""

    name: str

    def run(self, ctx: RunnerContext, stage_input: StageInput) -> StageResult: ...
