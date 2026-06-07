"""Phase 7A — blue/green Option A: deployment identity and state separation.

These tests cover the Phase 7A surface only:

* slot-scoped default state/feed roots, and that an explicit path override
  still wins (so a shared layout is possible but never accidental);
* slot validation (the slot is a filesystem path segment now, so traversal
  must be rejected fail-fast);
* the operator-facing deployment label / summary;
* the blue/green resource attribution actually reaching the OTel ``Resource``.

The OTel assertion imports opentelemetry directly: the import-linter contract
covers ``src`` only, and a telemetry-resource test is a legitimate place to
inspect OTel objects (the same exemption ``tests/test_telemetry_otel.py`` uses).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)

from storytime import __version__
from storytime.adapters.telemetry.otel import OTelTelemetry
from storytime.config import StoryTimeConfig, deployment_summary, load_config

# -- slot-scoped path resolution --------------------------------------------

def test_no_slot_keeps_the_pre_phase7a_layout() -> None:
    """With no slot the defaults are exactly runs/ and feed/ — no regression."""
    config = load_config({})
    assert config.runs_dir == Path("runs")
    assert config.feed_dir == Path("feed")
    assert config.deployment_slot == ""
    assert config.environment == "local"
    assert config.state_db_path == Path("runs") / "state.db"


def test_slot_scopes_the_default_state_and_feed_roots() -> None:
    """A slot scopes runs/<slot> and feed/<slot> so slots never share state."""
    blue = load_config({"STORYTIME_DEPLOYMENT_SLOT": "blue"})
    green = load_config({"STORYTIME_DEPLOYMENT_SLOT": "green"})

    assert blue.runs_dir == Path("runs") / "blue"
    assert blue.feed_dir == Path("feed") / "blue"
    assert green.runs_dir == Path("runs") / "green"
    assert green.feed_dir == Path("feed") / "green"

    # The whole point: the two slots resolve to different SQLite databases.
    assert blue.state_db_path != green.state_db_path
    assert blue.state_db_path == Path("runs") / "blue" / "state.db"


def test_explicit_runs_dir_overrides_the_slot_scoped_default() -> None:
    """An explicit STORYTIME_RUNS_DIR wins — a shared layout stays possible."""
    config = load_config(
        {"STORYTIME_DEPLOYMENT_SLOT": "blue", "STORYTIME_RUNS_DIR": "/srv/shared"}
    )
    assert config.runs_dir == Path("/srv/shared")
    # The slot still scopes the feed root, which was not overridden.
    assert config.feed_dir == Path("feed") / "blue"


def test_explicit_feed_dir_overrides_the_slot_scoped_default() -> None:
    config = load_config(
        {"STORYTIME_DEPLOYMENT_SLOT": "green", "STORYTIME_FEED_DIR": "out/feed"}
    )
    assert config.feed_dir == Path("out/feed")
    assert config.runs_dir == Path("runs") / "green"


# -- slot validation (the slot is a path segment) ----------------------------

@pytest.mark.parametrize("bad", ["../etc", "blue/green", "/abs", ".hidden", "Blue"])
def test_unsafe_slot_values_are_rejected_fail_fast(bad: str) -> None:
    """A slot with a slash, traversal, leading dot, or upper-case is rejected."""
    with pytest.raises(ValueError, match="STORYTIME_DEPLOYMENT_SLOT"):
        load_config({"STORYTIME_DEPLOYMENT_SLOT": bad})


@pytest.mark.parametrize("ok", ["blue", "green", "slot-1", "blue.2", "g0"])
def test_safe_slot_values_are_accepted(ok: str) -> None:
    config = load_config({"STORYTIME_DEPLOYMENT_SLOT": ok})
    assert config.deployment_slot == ok
    assert config.runs_dir == Path("runs") / ok


# -- deployment label / summary ---------------------------------------------

def test_deployment_label_with_and_without_a_slot() -> None:
    plain = load_config({"STORYTIME_ENVIRONMENT": "staging"})
    assert plain.deployment_label == "staging"

    slotted = load_config(
        {"STORYTIME_ENVIRONMENT": "staging", "STORYTIME_DEPLOYMENT_SLOT": "blue"}
    )
    assert slotted.deployment_label == "staging/blue"


def test_deployment_summary_reports_identity_and_roots() -> None:
    config = load_config(
        {"STORYTIME_ENVIRONMENT": "demo", "STORYTIME_DEPLOYMENT_SLOT": "green"}
    )
    text = "\n".join(deployment_summary(config))
    assert "demo/green" in text
    assert "green" in text
    assert str(Path("runs") / "green" / "state.db") in text
    assert str(Path("feed") / "green") in text


def test_deployment_summary_marks_an_absent_slot() -> None:
    text = "\n".join(deployment_summary(load_config({})))
    assert "(none)" in text


# -- telemetry resource attribution -----------------------------------------

def test_blue_green_identity_reaches_the_otel_resource() -> None:
    """deployment.slot / deployment.environment land on the OTel Resource.

    Resource attributes are set once from immutable config; every span shares
    them. This is how a blue and a green process are told apart in Jaeger /
    Prometheus without adding any per-span cardinality.
    """
    exporter = InMemorySpanExporter()
    adapter = OTelTelemetry(
        otlp_endpoint="http://127.0.0.1:4318",
        service_version="9.9.9",
        environment="staging",
        deployment_slot="green",
        span_exporter=exporter,
        metric_reader=InMemoryMetricReader(),
    )
    run = adapter.on_run_started("run-bg", {})
    adapter.on_run_ended(run, "succeeded")

    finished = exporter.get_finished_spans()
    assert finished, "expected the run span to be exported"
    resource = finished[0].resource.attributes
    assert resource["service.name"] == "storytime"
    assert resource["service.version"] == "9.9.9"
    assert resource["deployment.environment"] == "staging"
    assert resource["deployment.slot"] == "green"


def test_absent_slot_omits_the_deployment_slot_resource_attribute() -> None:
    """With no slot, deployment.slot is omitted rather than set to an empty
    string — an empty resource attribute would be misleading noise."""
    exporter = InMemorySpanExporter()
    adapter = OTelTelemetry(
        otlp_endpoint="http://127.0.0.1:4318",
        service_version=__version__,
        environment="local",
        deployment_slot="",
        span_exporter=exporter,
        metric_reader=InMemoryMetricReader(),
    )
    run = adapter.on_run_started("run-noslot", {})
    adapter.on_run_ended(run, "succeeded")

    resource = exporter.get_finished_spans()[0].resource.attributes
    assert "deployment.slot" not in resource
    assert resource["deployment.environment"] == "local"


# -- direct StoryTimeConfig construction is unchanged ------------------------

def test_directly_constructed_config_still_has_safe_defaults() -> None:
    """StoryTimeConfig built directly (e.g. by the demo harness) is unchanged:
    environment defaults to 'local', deployment_slot to '' (no slot)."""
    config = StoryTimeConfig(
        runs_dir=Path("runs"),
        feed_dir=Path("feed"),
        telemetry="noop",
        otlp_endpoint="http://127.0.0.1:4318",
        http_host="127.0.0.1",
        http_port=8000,
    )
    assert config.environment == "local"
    assert config.deployment_slot == ""
    assert config.deployment_label == "local"
