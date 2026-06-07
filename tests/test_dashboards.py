"""Phase 6A metric-honesty and observability-provisioning tests.

The headline guarantee of Phase 6A is **metric honesty**: a dashboard panel
must never reference a metric StoryTime does not emit. This module enforces
that automatically — it parses every PromQL expression in every provisioned
Grafana dashboard and rejects any ``pipeline_*`` token that is not a real
Phase 5 metric (or an intrinsic histogram series, or a real metric label).

It also checks that the dashboards are valid JSON, that the Grafana and
Prometheus provisioning files are valid YAML, and that the collector now has a
metrics pipeline — so the wiring the dashboards depend on actually exists.

No Docker is required: these are static file checks.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from storytime.adapters.telemetry.metrics import (
    ALL_METRICS,
    HISTOGRAM_METRICS,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DASHBOARD_DIR = _REPO_ROOT / "config" / "grafana" / "dashboards"
_CONFIG_DIR = _REPO_ROOT / "config"

# The six dashboards Phase 6A is required to ship.
_EXPECTED_DASHBOARDS = {
    "pipeline-overview.json",
    "stage-duration.json",
    "approval-resume.json",
    "failures-rejections.json",
    "artifact-validation.json",
    "run-timeline.json",
}

# Every ``pipeline_*`` token a dashboard expression is allowed to contain.
#  * the eight real metric names;
#  * the intrinsic _bucket / _sum / _count series of each histogram;
#  * the two metric LABEL names whose OTLP dotted form (pipeline.stage,
#    pipeline.status) is exposed by Prometheus with an underscore.
def _allowed_metric_tokens() -> set[str]:
    allowed = set(ALL_METRICS)
    for histogram in HISTOGRAM_METRICS:
        allowed |= {
            f"{histogram}_bucket",
            f"{histogram}_sum",
            f"{histogram}_count",
        }
    allowed |= {"pipeline_stage", "pipeline_status"}
    return allowed


_PIPELINE_TOKEN = re.compile(r"pipeline_[a-z_]+")


def _dashboard_files() -> list[Path]:
    return sorted(_DASHBOARD_DIR.glob("*.json"))


def _exprs(dashboard: dict[str, object]) -> list[str]:
    """Extract every PromQL target expression from a dashboard document."""
    found: list[str] = []
    panels = dashboard.get("panels", [])
    assert isinstance(panels, list)
    for panel in panels:
        assert isinstance(panel, dict)
        for target in panel.get("targets", []):
            assert isinstance(target, dict)
            expr = target.get("expr")
            if isinstance(expr, str) and expr.strip():
                found.append(expr)
    return found


def test_all_six_dashboards_are_present() -> None:
    names = {path.name for path in _dashboard_files()}
    assert names == _EXPECTED_DASHBOARDS


def test_every_dashboard_is_valid_json_with_required_fields() -> None:
    for path in _dashboard_files():
        doc = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(doc, dict), path.name
        # Fields Grafana's file provisioner needs.
        for key in ("uid", "title", "schemaVersion", "panels"):
            assert key in doc, f"{path.name} missing {key}"
        assert doc["panels"], f"{path.name} has no panels"


def test_dashboard_uids_are_unique() -> None:
    uids = [
        json.loads(path.read_text(encoding="utf-8"))["uid"]
        for path in _dashboard_files()
    ]
    assert len(uids) == len(set(uids))


def test_every_panel_has_at_least_one_target() -> None:
    for path in _dashboard_files():
        doc = json.loads(path.read_text(encoding="utf-8"))
        for panel in doc["panels"]:
            assert panel.get("targets"), (
                f"{path.name}: panel {panel.get('title')!r} has no targets"
            )


def test_dashboards_reference_only_real_phase5_metrics() -> None:
    """METRIC HONESTY: no panel may reference an unknown ``pipeline_*`` token."""
    allowed = _allowed_metric_tokens()
    violations: list[str] = []
    for path in _dashboard_files():
        doc = json.loads(path.read_text(encoding="utf-8"))
        for expr in _exprs(doc):
            for token in _PIPELINE_TOKEN.findall(expr):
                if token not in allowed:
                    violations.append(f"{path.name}: {token!r} in {expr!r}")
    assert not violations, "unknown metric tokens in dashboards:\n" + "\n".join(
        violations
    )


def test_every_real_metric_is_used_by_some_dashboard() -> None:
    """Each Phase 5 metric appears on at least one dashboard (no dead metrics)."""
    seen: set[str] = set()
    for path in _dashboard_files():
        doc = json.loads(path.read_text(encoding="utf-8"))
        for expr in _exprs(doc):
            for token in _PIPELINE_TOKEN.findall(expr):
                # Fold a histogram's _bucket/_sum/_count back to its base name.
                for base in HISTOGRAM_METRICS:
                    if token.startswith(base):
                        token = base
                        break
                if token in ALL_METRICS:
                    seen.add(token)
    assert seen == set(ALL_METRICS), (
        f"metrics never charted: {sorted(set(ALL_METRICS) - seen)}"
    )


def test_grafana_datasource_provisioning_is_valid_yaml() -> None:
    path = (
        _CONFIG_DIR
        / "grafana" / "provisioning" / "datasources" / "datasources.yaml"
    )
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    names = {ds["name"] for ds in doc["datasources"]}
    assert {"Prometheus", "Jaeger"} <= names
    prometheus = next(d for d in doc["datasources"] if d["name"] == "Prometheus")
    assert prometheus["isDefault"] is True


def test_grafana_dashboard_provisioning_points_at_the_dashboard_dir() -> None:
    path = (
        _CONFIG_DIR
        / "grafana" / "provisioning" / "dashboards" / "dashboards.yaml"
    )
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    provider = doc["providers"][0]
    assert provider["options"]["path"] == "/var/lib/grafana/dashboards"


def test_prometheus_config_scrapes_the_collector() -> None:
    doc = yaml.safe_load(
        (_CONFIG_DIR / "prometheus.yml").read_text(encoding="utf-8")
    )
    targets = [
        target
        for job in doc["scrape_configs"]
        for static in job["static_configs"]
        for target in static["targets"]
    ]
    assert any("otel-collector" in target for target in targets)
    # Phase 6A excludes alerting: there must be no alerting/rules wiring.
    assert "alerting" not in doc
    assert "rule_files" not in doc


def test_collector_has_a_metrics_pipeline_preserving_metric_names() -> None:
    doc = yaml.safe_load(
        (_CONFIG_DIR / "otel-collector.yaml").read_text(encoding="utf-8")
    )
    pipelines = doc["service"]["pipelines"]
    assert "metrics" in pipelines, "collector still has no metrics pipeline"
    assert "prometheus" in pipelines["metrics"]["exporters"]
    # METRIC HONESTY: suffixes off, so series keep their declared names.
    assert doc["exporters"]["prometheus"]["add_metric_suffixes"] is False
