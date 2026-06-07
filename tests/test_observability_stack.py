"""Phase 8B — local multi-backend observability stack tests.

Phase 8B expands the local observability topology with Loki and a local log
route: the StoryTime demo harness writes structured JSON-lines logs, the
OpenTelemetry Collector ``filelog`` receiver tails them, and the Collector
forwards them to Loki for Grafana to query.

These are static configuration checks plus log-sink behaviour checks. They
need no Docker, no network, and no vendor credentials — Architecture Baseline
Section 23 rule 9. They also assert the Section 23 governance rules: standard
OTLP only, no vendor exporters, the collector owns routing, and logs are plain
structured files (never Python OTLP log export).
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from storytime.demo import run_demo
from storytime.demo.harness import DemoResult, DemoScenarioResult
from storytime.demo.logsink import (
    DEMO_LOG_FILENAME,
    scenario_record,
    summary_record,
    write_demo_log,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_DIR = _REPO_ROOT / "config"

# Vendor names / exporters that Phase 8B must not introduce (Section 23 rules
# 3-6). Phase 8B is local-only; vendor fan-out is the future Phase 8C.
_FORBIDDEN_VENDOR_TOKENS = (
    "dynatrace",
    "newrelic",
    "new_relic",
    "datadog",
)


def _load_yaml(path: Path) -> dict[str, object]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------
# Collector config — logs pipeline, resilience, no vendor coupling.
# --------------------------------------------------------------------------

def test_collector_has_a_logs_pipeline_with_a_filelog_receiver() -> None:
    doc = _load_yaml(_CONFIG_DIR / "otel-collector.yaml")
    pipelines = doc["service"]["pipelines"]
    assert "logs" in pipelines, "collector has no logs pipeline"
    assert "filelog" in pipelines["logs"]["receivers"], (
        "logs pipeline must use the filelog receiver (Phase 8B Option C)"
    )
    # The filelog receiver reads mounted local files — not the network.
    filelog = doc["receivers"]["filelog"]
    includes = filelog["include"]
    assert any("/var/log/storytime" in path for path in includes)


def test_collector_logs_pipeline_exports_to_loki_over_standard_otlp() -> None:
    doc = _load_yaml(_CONFIG_DIR / "otel-collector.yaml")
    exporters = doc["exporters"]
    # Standard otlphttp exporter only (Section 23.4) — no proprietary `loki`
    # exporter, no vendor exporter.
    assert "otlphttp/loki" in exporters
    loki_exporter = exporters["otlphttp/loki"]
    assert "loki" in loki_exporter["endpoint"]
    logs_exporters = doc["service"]["pipelines"]["logs"]["exporters"]
    assert "otlphttp/loki" in logs_exporters
    # No proprietary `loki` exporter type and no vendor exporter key anywhere.
    assert "loki" not in exporters, (
        "use the standard otlphttp exporter, not the proprietary loki exporter"
    )


def test_collector_pipelines_are_resilient() -> None:
    """Section 23.10: memory_limiter first in every pipeline; retry + queue."""
    doc = _load_yaml(_CONFIG_DIR / "otel-collector.yaml")
    assert "memory_limiter" in doc["processors"]
    for name, pipeline in doc["service"]["pipelines"].items():
        processors = pipeline["processors"]
        assert processors[0] == "memory_limiter", (
            f"{name} pipeline: memory_limiter must be the first processor"
        )
        assert "batch" in processors, f"{name} pipeline missing batch processor"
    # Network exporters carry retry + sending queue (drop, never block a run).
    for exporter_name in ("otlp/jaeger", "otlphttp/loki"):
        exporter = doc["exporters"][exporter_name]
        assert exporter["retry_on_failure"]["enabled"] is True
        assert exporter["sending_queue"]["enabled"] is True


def test_collector_config_introduces_no_vendor_coupling() -> None:
    """Section 23 rules 3-6: no vendor exporters/agents/config in Phase 8B."""
    raw = (_CONFIG_DIR / "otel-collector.yaml").read_text(encoding="utf-8").lower()
    for token in _FORBIDDEN_VENDOR_TOKENS:
        assert token not in raw, f"collector config must not mention {token!r}"


def test_collector_metrics_and_traces_pipelines_are_preserved() -> None:
    """Phase 8B must not rewrite the existing traces/metrics paths."""
    doc = _load_yaml(_CONFIG_DIR / "otel-collector.yaml")
    pipelines = doc["service"]["pipelines"]
    assert "otlp/jaeger" in pipelines["traces"]["exporters"]
    assert "prometheus" in pipelines["metrics"]["exporters"]
    # Metric honesty (Phase 6A) is untouched.
    assert doc["exporters"]["prometheus"]["add_metric_suffixes"] is False


# --------------------------------------------------------------------------
# Loki config.
# --------------------------------------------------------------------------

def test_loki_config_is_valid_yaml_and_local_only() -> None:
    doc = _load_yaml(_CONFIG_DIR / "loki.yaml")
    # Demo-grade local config: auth disabled, filesystem storage.
    assert doc["auth_enabled"] is False
    assert doc["server"]["http_listen_port"] == 3100
    assert "filesystem" in doc["common"]["storage"]


# --------------------------------------------------------------------------
# docker-compose.observability.yml — Loki service, loopback ports, log mount.
# --------------------------------------------------------------------------

def test_observability_compose_has_a_loki_service() -> None:
    doc = _load_yaml(_REPO_ROOT / "docker-compose.observability.yml")
    services = doc["services"]
    assert "loki" in services, "observability stack has no Loki service"
    loki = services["loki"]
    # Pinned to an explicit tag (Gemini edit 6) — not `latest`.
    assert ":" in loki["image"] and not loki["image"].endswith(":latest")
    assert loki["image"].startswith("grafana/loki:")


def test_observability_compose_ports_are_loopback_bound() -> None:
    """Every published host port binds 127.0.0.1 (Section 23 rule 15)."""
    doc = _load_yaml(_REPO_ROOT / "docker-compose.observability.yml")
    for name, service in doc["services"].items():
        for mapping in service.get("ports", []):
            assert str(mapping).startswith("127.0.0.1:"), (
                f"{name}: host port {mapping} is not loopback-bound"
            )


def test_collector_mounts_the_demo_log_directory_read_only() -> None:
    doc = _load_yaml(_REPO_ROOT / "docker-compose.observability.yml")
    volumes = doc["services"]["otel-collector"]["volumes"]
    log_mounts = [v for v in volumes if "/var/log/storytime" in v]
    assert log_mounts, "collector does not mount the demo log directory"
    assert log_mounts[0].endswith(":ro"), "log mount must be read-only"


def test_grafana_depends_on_loki() -> None:
    doc = _load_yaml(_REPO_ROOT / "docker-compose.observability.yml")
    assert "loki" in doc["services"]["grafana"]["depends_on"]


# --------------------------------------------------------------------------
# Grafana provisioning — Loki datasource.
# --------------------------------------------------------------------------

def test_grafana_provisions_a_loki_datasource() -> None:
    path = (
        _CONFIG_DIR
        / "grafana" / "provisioning" / "datasources" / "datasources.yaml"
    )
    doc = _load_yaml(path)
    by_name = {ds["name"]: ds for ds in doc["datasources"]}
    # All three local backends are provisioned as code.
    assert {"Prometheus", "Jaeger", "Loki"} <= set(by_name)
    loki = by_name["Loki"]
    assert loki["type"] == "loki"
    assert "loki" in loki["url"]
    assert loki["editable"] is False


# --------------------------------------------------------------------------
# Structured log sink — JSON Lines, control-plane only, append-only.
# --------------------------------------------------------------------------

def _fake_scenario(name: str = "success", ok: bool = True) -> DemoScenarioResult:
    return DemoScenarioResult(
        name=name,
        description="fake scenario for testing",
        expected="completed",
        actual="completed" if ok else "failed",
        ok=ok,
        detail="status=completed",
        pipeline_run_id="01JFAKE0000000000000000000",
    )


def test_scenario_record_is_valid_control_plane_metadata() -> None:
    record = scenario_record(
        _fake_scenario(), service_version="0.2.0", environment="demo"
    )
    # JSON-serializable and carries the expected control-plane keys.
    json.dumps(record)
    for key in ("timestamp", "level", "scenario", "pipeline.run_id", "status"):
        assert key in record
    assert record["service.name"] == "storytime"
    assert record["event"] == "demo.scenario"


def test_summary_record_is_valid_control_plane_metadata() -> None:
    result = DemoResult(
        workspace=Path("/tmp/ws"),
        telemetry="noop",
        otlp_endpoint="http://127.0.0.1:4318",
        scenarios=(_fake_scenario(),),
    )
    record = summary_record(result, service_version="0.2.0")
    json.dumps(record)
    assert record["event"] == "demo.summary"
    assert record["scenario_count"] == 1


def test_log_records_carry_no_data_plane_payloads() -> None:
    """Section 23.8: no story text / narration / RSS / payloads in logs.

    The guarantee is structural: a log record's keys are a fixed closed set of
    control-plane fields, and every value is short. There is no field through
    which raw story text, narration, or an RSS payload could ride along.
    """
    record = scenario_record(
        _fake_scenario(), service_version="0.2.0", environment="demo"
    )
    expected_keys = {
        "timestamp", "level", "logger", "service.name", "service.version",
        "deployment.environment", "event", "scenario", "pipeline.run_id",
        "status", "expected", "ok", "message",
    }
    assert set(record) == expected_keys, "log record has unexpected fields"
    # Every value is short — no field can carry a payload-sized blob.
    for value in record.values():
        assert len(str(value)) <= 256, "log field exceeds the safe length bound"


def test_write_demo_log_writes_one_json_object_per_line(tmp_path: Path) -> None:
    result = DemoResult(
        workspace=tmp_path / "ws",
        telemetry="noop",
        otlp_endpoint="http://127.0.0.1:4318",
        scenarios=(_fake_scenario("success"), _fake_scenario("bad", ok=False)),
    )
    path = write_demo_log(tmp_path / "logs", result, service_version="0.2.0")
    assert path.name == DEMO_LOG_FILENAME
    lines = path.read_text(encoding="utf-8").splitlines()
    # Two scenarios + one summary line.
    assert len(lines) == 3
    for line in lines:
        json.loads(line)  # every line is a standalone JSON object


def test_write_demo_log_appends_across_runs(tmp_path: Path) -> None:
    result = DemoResult(
        workspace=tmp_path / "ws",
        telemetry="noop",
        otlp_endpoint="http://127.0.0.1:4318",
        scenarios=(_fake_scenario(),),
    )
    log_dir = tmp_path / "logs"
    write_demo_log(log_dir, result, service_version="0.2.0")
    path = write_demo_log(log_dir, result, service_version="0.2.0")
    # Each run writes 1 scenario + 1 summary line; two runs => 4 lines.
    assert len(path.read_text(encoding="utf-8").splitlines()) == 4


def test_demo_writes_a_log_file_when_log_dir_is_given(tmp_path: Path) -> None:
    """End-to-end: a real (noop) demo run produces a tailable log file."""
    result = run_demo(
        workspace=tmp_path / "ws",
        telemetry="noop",
        scenarios=("bad_manifest",),
        log_dir=tmp_path / "logs",
    )
    log_file = tmp_path / "logs" / DEMO_LOG_FILENAME
    assert log_file.is_file()
    lines = log_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2  # one scenario + summary
    scenario_line = json.loads(lines[0])
    assert scenario_line["scenario"] == "bad_manifest"
    assert scenario_line["status"] == result.scenarios[0].actual


def test_demo_writes_no_log_file_by_default(tmp_path: Path) -> None:
    """Default behaviour is unchanged: no log_dir => no log file."""
    run_demo(
        workspace=tmp_path / "ws",
        telemetry="noop",
        scenarios=("bad_manifest",),
    )
    assert not (tmp_path / "logs").exists()


# --------------------------------------------------------------------------
# Makefile — ./logs preflight (Phase 8B.1 operational cleanup).
# --------------------------------------------------------------------------

def _makefile_targets() -> dict[str, str]:
    """Return a {target: recipe-block} map parsed from the Makefile."""
    text = (_REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    targets: dict[str, str] = {}
    current: str | None = None
    lines: list[str] = []
    for raw in text.splitlines():
        if raw and not raw.startswith((" ", "\t", "#")) and ":" in raw:
            if current is not None:
                targets[current] = "\n".join(lines)
            current = raw.split(":", 1)[0].strip()
            lines = []
        elif current is not None and raw.startswith("\t"):
            lines.append(raw.strip())
    if current is not None:
        targets[current] = "\n".join(lines)
    return targets


def test_makefile_has_a_logs_preflight_target() -> None:
    """Phase 8B.1: a target creates ./logs before the stack/demo need it."""
    targets = _makefile_targets()
    assert "logs-dir" in targets, "Makefile has no logs-dir preflight target"
    assert "mkdir -p logs" in targets["logs-dir"]


def test_makefile_observability_and_demo_targets_preflight_logs() -> None:
    """`observability-up` and `demo` must ensure ./logs exists first.

    The compose file bind-mounts ./logs into the Collector; if Docker creates
    the directory it may be root-owned and unwritable by the local demo. Both
    Docker-facing targets therefore depend on the logs-dir preflight.
    """
    text = (_REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    for target in ("observability-up", "demo"):
        # The dependency is declared on the target's rule line.
        rule = next(
            line for line in text.splitlines()
            if line.startswith(f"{target}:")
        )
        assert "logs-dir" in rule, (
            f"Makefile target {target!r} must depend on the logs-dir preflight"
        )
