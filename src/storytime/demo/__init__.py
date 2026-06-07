"""StoryTime observability demo harness (Phase 6A).

The harness runs real StoryTime pipeline scenarios so the local observability
stack has genuine telemetry to display — successful runs, approval pauses and
resumes, rejections, a rejected manifest, and an artifact-validation failure.

It generates *real* telemetry: it drives the actual pipeline entry points
(``run_vertical_slice`` / ``resume_run`` / ``apply_approval_decision``) with
the telemetry adapter selected by configuration. It never fabricates spans or
metrics. It is bounded to a single local workspace directory and touches
nothing else.

Run it with ``python -m storytime.demo`` (see ``storytime.demo.__main__``).
"""

from storytime.demo.harness import DemoResult, DemoScenarioResult, run_demo

__all__ = ["DemoResult", "DemoScenarioResult", "run_demo"]
