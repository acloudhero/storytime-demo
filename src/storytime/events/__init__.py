"""Internal event model. Leaf package: imports nothing else from storytime."""

from storytime.events.model import EventType, PipelineEvent

__all__ = ["EventType", "PipelineEvent"]
