"""Telemetry adapters.

build_telemetry imports the OpenTelemetry implementation lazily so that a
NoopTelemetry-only deployment never imports opentelemetry at all.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from storytime.adapters.telemetry.base import RunHandle, StageHandle, TelemetryAdapter
from storytime.adapters.telemetry.noop import NoopTelemetry

if TYPE_CHECKING:
    from storytime.config import StoryTimeConfig

__all__ = [
    "NoopTelemetry",
    "RunHandle",
    "StageHandle",
    "TelemetryAdapter",
    "build_telemetry",
]


def build_telemetry(config: StoryTimeConfig) -> TelemetryAdapter:
    """Return the telemetry adapter selected by *config*.

    The OTel adapter (and therefore opentelemetry itself) is imported only when
    config.telemetry == "otel". service_version / environment / deployment_slot
    / service_instance_id become the OTel Resource identity -- generic and
    configurable so a blue/green rollout (bare-metal or containerized)
    attributes traces without touching any business logic. service_instance_id
    is the stable, slot-derived value (Phase 7C / 7C.1 Resource Identity
    Contract). NoopTelemetry is the default and never imports opentelemetry.
    """
    if config.telemetry == "otel":
        from storytime.adapters.telemetry.otel import OTelTelemetry

        return OTelTelemetry(
            otlp_endpoint=config.otlp_endpoint,
            service_version=config.service_version,
            environment=config.environment,
            deployment_slot=config.deployment_slot,
            service_instance_id=config.service_instance_id,
        )
    return NoopTelemetry()
