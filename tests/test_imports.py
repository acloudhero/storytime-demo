"""Every scaffold module must import cleanly."""

from __future__ import annotations

import importlib

MODULES = [
    "storytime",
    "storytime.config",
    "storytime.doctor",
    "storytime.util.ids",
    "storytime.util.hashing",
    "storytime.util.clock",
    "storytime.events",
    "storytime.events.model",
    "storytime.artifacts",
    "storytime.artifacts.envelope",
    "storytime.artifacts.io",
    "storytime.manifest",
    "storytime.manifest.schema",
    "storytime.manifest.validator",
    "storytime.dto",
    "storytime.dto.stage_io",
    "storytime.state",
    "storytime.state.schema",
    "storytime.state.store",
    "storytime.adapters.telemetry",
    "storytime.adapters.telemetry.base",
    "storytime.adapters.telemetry.noop",
    "storytime.adapters.telemetry.propagation",
    "storytime.adapters.telemetry.metrics",
    "storytime.adapters.telemetry.attributes",
    "storytime.adapters.telemetry.hygiene",
    "storytime.adapters.tts",
    "storytime.adapters.tts.base",
    "storytime.adapters.tts.mock",
    "storytime.adapters.tts.manual_import",
    "storytime.adapters.tts.piper",
    "storytime.adapters.storage",
    "storytime.adapters.storage.local",
    "storytime.tts_proof",
    "storytime.tts_proof.config",
    "storytime.tts_proof.events",
    "storytime.tts_proof.manifest",
    "storytime.tts_proof.boundary",
    "storytime.stages",
    "storytime.stages.base",
    "storytime.stages.ingest",
    "storytime.stages.synthesize",
    "storytime.stages.encode",
    "storytime.stages.assemble",
    "storytime.stages.publish",
    "storytime.pipeline",
    "storytime.runner",
    "storytime.runner.context",
    "storytime.runner.runner",
    "storytime.rss",
    "storytime.rss.builder",
    "storytime.http",
    "storytime.http.server",
    "storytime.runtime",
    "storytime.runtime.roles",
    "storytime.runtime.config",
    "storytime.runtime.health",
    "storytime.runtime.boundary_readiness",
    "storytime.cli.app",
]


def test_all_modules_import() -> None:
    for name in MODULES:
        module = importlib.import_module(name)
        assert module is not None


def test_version_is_exposed() -> None:
    import storytime

    assert storytime.__version__ == "0.2.0"
