"""Pipeline stages.

The Stage contract lives in storytime.stages.base. The Phase 3 thin vertical
slice adds four concrete stages — ingest, synthesize, assemble, publish — each
in its own module. Phase 4 adds the ApprovalGateStage, a persisted interactive
operator approval gate. They are re-exported here for convenience; the runner
only ever depends on the Stage protocol, never on a concrete stage.
"""

from storytime.stages.approve import (
    ApprovalGateStage,
    audio_approval_gate,
    text_approval_gate,
)
from storytime.stages.assemble import AssembleStage
from storytime.stages.base import Stage
from storytime.stages.ingest import IngestStage
from storytime.stages.publish import PublishStage
from storytime.stages.synthesize import SynthesizeStage

__all__ = [
    "ApprovalGateStage",
    "AssembleStage",
    "IngestStage",
    "PublishStage",
    "Stage",
    "SynthesizeStage",
    "audio_approval_gate",
    "text_approval_gate",
]
