"""Phase 8C / 8C.1 — optional vendor export profile tests.

Static configuration checks (no Docker, no network, no vendor credentials)
enforcing Architecture Baseline Section 23 governance for the optional vendor
export profiles: the default local-only path has no vendor exporter (23.6);
vendor export uses standard otlphttp only (23.4, 23.11); vendor exporters are
resilient (23.10); no real secret, token, or endpoint is committed (23.6, 23.7).

Phase 8C.1 split the original single combined override into two independent,
mutually exclusive per-vendor profiles. Each profile is one override compose
file plus one single-vendor Collector config under config/vendor/.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_DIR = _REPO_ROOT / "config"
_VENDOR_DIR = _CONFIG_DIR / "vendor"

_DEFAULT_COLLECTOR = _CONFIG_DIR / "otel-collector.yaml"
_OBSERVABILITY_COMPOSE = _REPO_ROOT / "docker-compose.observability.yml"
_SECRET_TEMPLATE = _CONFIG_DIR / "vendor.secret.env.example"

# Each vendor profile: (vendor key, collector config, override compose file,
# this profile's own otlphttp exporter, the OTHER vendor's exporter).
_PROFILES = {
    "dynatrace": (
        _VENDOR_DIR / "otel-collector.dynatrace.example.yaml",
        _REPO_ROOT / "docker-compose.vendor.dynatrace.yml",
        "otlphttp/dynatrace",
        "otlphttp/newrelic",
    ),
    "newrelic": (
        _VENDOR_DIR / "otel-collector.newrelic.example.yaml",
        _REPO_ROOT / "docker-compose.vendor.newrelic.yml",
        "otlphttp/newrelic",
        "otlphttp/dynatrace",
    ),
}

_FORBIDDEN = ("datadog", "ddtrace")
_LOCAL_EXPORTERS = {"otlp/jaeger", "prometheus", "otlphttp/loki"}


def _yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


# --- per-vendor collector config checks -------------------------------------


@pytest.mark.parametrize("vendor", sorted(_PROFILES))
def test_vendor_collector_config_is_valid_yaml(vendor: str) -> None:
    config, _, _, _ = _PROFILES[vendor]
    doc = _yaml(config)
    assert "exporters" in doc and "service" in doc


@pytest.mark.parametrize("vendor", sorted(_PROFILES))
def test_vendor_config_ships_exactly_its_own_profile(vendor: str) -> None:
    """Each split config wires its own vendor only — not the other vendor."""
    config, _, own, other = _PROFILES[vendor]
    doc = _yaml(config)
    assert own in doc["exporters"], f"{config.name} missing its exporter {own}"
    assert other not in doc["exporters"], (
        f"{config.name} must wire only {own}, not {other} — profiles are split"
    )


@pytest.mark.parametrize("vendor", sorted(_PROFILES))
def test_vendor_exporters_use_standard_otlphttp_only(vendor: str) -> None:
    """23.4: standard otlphttp only — no proprietary vendor exporter."""
    config, _, _, _ = _PROFILES[vendor]
    doc = _yaml(config)
    for name in doc["exporters"]:
        kind = str(name).split("/", 1)[0]
        assert kind in {"otlp", "otlphttp", "prometheus", "debug"}, (
            f"non-standard exporter type {kind!r} in {config.name}"
        )


@pytest.mark.parametrize("vendor", sorted(_PROFILES))
def test_no_datadog_or_proprietary_exporter_in_vendor_profile(vendor: str) -> None:
    """23.4 / 23.11: no Datadog or proprietary exporter is wired in.

    Structural check on component keys — an explanatory comment may mention
    Datadog (to record it is deferred); no Datadog exporter may be configured.
    """
    config, _, _, _ = _PROFILES[vendor]
    doc = _yaml(config)
    keys = (
        list(doc.get("exporters", {}))
        + list(doc.get("receivers", {}))
        + list(doc.get("processors", {}))
    )
    for key in keys:
        for token in _FORBIDDEN:
            assert token not in str(key).lower(), (
                f"{config.name} wires in a forbidden component: {key!r}"
            )
    assert "ddtrace" not in config.read_text(encoding="utf-8").lower()


@pytest.mark.parametrize("vendor", sorted(_PROFILES))
def test_vendor_exporter_endpoint_and_headers_are_env_placeholders(
    vendor: str,
) -> None:
    """23.6 / 23.7: every vendor value is env-injected, never literal."""
    config, _, own, _ = _PROFILES[vendor]
    cfg = _yaml(config)["exporters"][own]
    assert str(cfg["endpoint"]).startswith("${env:"), (
        f"{own} endpoint is not env-injected"
    )
    for value in cfg["headers"].values():
        assert "${env:" in str(value), f"{own} header carries a non-env value"


@pytest.mark.parametrize("vendor", sorted(_PROFILES))
def test_vendor_exporter_is_resilient(vendor: str) -> None:
    """23.10: bounded retry + sending queue; memory_limiter first; batch."""
    config, _, own, _ = _PROFILES[vendor]
    doc = _yaml(config)
    cfg = doc["exporters"][own]
    retry = cfg["retry_on_failure"]
    assert retry["enabled"] is True
    assert "max_elapsed_time" in retry, (
        f"{own} retry must set a bounded max_elapsed_time"
    )
    assert cfg["sending_queue"]["enabled"] is True
    for name, pipeline in doc["service"]["pipelines"].items():
        processors = pipeline["processors"]
        assert processors[0] == "memory_limiter", (
            f"{config.name} {name} pipeline: memory_limiter must be first"
        )
        assert "batch" in processors


@pytest.mark.parametrize("vendor", sorted(_PROFILES))
def test_vendor_pipelines_fan_out_to_local_and_vendor(vendor: str) -> None:
    """Every pipeline keeps its local leg AND adds this profile's vendor leg."""
    config, _, own, other = _PROFILES[vendor]
    doc = _yaml(config)
    for name, pipeline in doc["service"]["pipelines"].items():
        exporters = set(pipeline["exporters"])
        assert own in exporters, f"{config.name} {name} pipeline missing {own}"
        assert other not in exporters, (
            f"{config.name} {name} pipeline must not fan out to {other}"
        )
        assert _LOCAL_EXPORTERS & exporters, (
            f"{config.name} {name} pipeline lost its local exporter"
        )


# --- per-vendor override compose checks -------------------------------------


@pytest.mark.parametrize("vendor", sorted(_PROFILES))
def test_vendor_override_is_valid_yaml_and_opt_in(vendor: str) -> None:
    config, override, _, _ = _PROFILES[vendor]
    doc = _yaml(override)
    collector = doc["services"]["otel-collector"]
    mounts = [v for v in collector["volumes"] if config.name in v]
    assert mounts, f"{override.name} does not mount {config.name}"
    cmd = " ".join(collector["command"])
    assert f"config-vendor-{vendor}" in cmd, (
        f"{override.name} does not point the collector at its vendor config"
    )
    env_files = collector["env_file"]
    assert any("vendor.secret.env" in f for f in env_files), (
        f"{override.name} must read vendor credentials from a *.secret.env file"
    )


def test_vendor_overrides_target_distinct_configs_and_paths() -> None:
    """The two profiles are independent: distinct configs and distinct paths.

    Mutual exclusivity is documented (a single Collector reads one config and
    Compose's command: is last-write-wins). This test pins the structural half:
    each override targets a different vendor config at a different container
    path, so neither override silently shadows the other's mount.
    """
    dyn = _yaml(_PROFILES["dynatrace"][1])["services"]["otel-collector"]
    nr = _yaml(_PROFILES["newrelic"][1])["services"]["otel-collector"]
    assert " ".join(dyn["command"]) != " ".join(nr["command"])
    dyn_targets = {v.split(":")[-2] for v in dyn["volumes"]}
    nr_targets = {v.split(":")[-2] for v in nr["volumes"]}
    assert dyn_targets.isdisjoint(nr_targets), (
        "the two vendor overrides mount to overlapping container paths"
    )


@pytest.mark.parametrize("vendor", sorted(_PROFILES))
def test_vendor_override_keeps_secrets_out_of_the_file(vendor: str) -> None:
    _, override, _, _ = _PROFILES[vendor]
    raw = override.read_text(encoding="utf-8")
    assert "dt0c01." not in raw and "dt0s01." not in raw


# --- shared default-path and secret-hygiene checks --------------------------


def test_default_collector_config_has_no_vendor_exporter() -> None:
    """23.6: the default local-only collector config has no vendor exporter."""
    raw = _DEFAULT_COLLECTOR.read_text(encoding="utf-8").lower()
    for token in ("dynatrace", "newrelic", "new_relic", "datadog"):
        assert token not in raw, (
            f"the default collector config must not mention {token!r}"
        )


def test_default_observability_compose_stays_local_only() -> None:
    """The base compose still loads the local-only config — no vendor path."""
    base = _yaml(_OBSERVABILITY_COMPOSE)
    base_cmd = " ".join(base["services"]["otel-collector"]["command"])
    assert "config-vendor" not in base_cmd


def test_secret_files_are_git_and_docker_ignored() -> None:
    """The real *.secret.env pattern is git-ignored and docker-ignored."""
    assert "*.secret.env" in (_REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "*.secret.env" in (_REPO_ROOT / ".dockerignore").read_text(
        encoding="utf-8"
    )


def test_vendor_env_example_carries_only_placeholders() -> None:
    """23.6 / 23.7: the committed template has no real value."""
    lines = _SECRET_TEMPLATE.read_text(encoding="utf-8").splitlines()
    value_lines = [
        ln for ln in lines
        if ln.strip() and not ln.lstrip().startswith("#") and "=" in ln
    ]
    assert value_lines, "secret template has no example variables"
    for ln in value_lines:
        value = ln.split("=", 1)[1].strip()
        assert "REPLACE" in value, f"template value is not a placeholder: {ln}"
    # The template is committed (ends .example); the real file is not.
    assert _SECRET_TEMPLATE.name.endswith(".example")
    assert not _SECRET_TEMPLATE.name.endswith(".secret.env")


def test_committed_vendor_files_contain_no_real_vendor_endpoints() -> None:
    """No committed Phase 8C file hardcodes a real vendor hostname."""
    real_hostnames = ("live.dynatrace.com", "otlp.nr-data.net", "nr-data.net")
    committed = [_SECRET_TEMPLATE]
    for config, override, _, _ in _PROFILES.values():
        committed += [config, override]
    for path in committed:
        text = path.read_text(encoding="utf-8").lower()
        for host in real_hostnames:
            assert host not in text, (
                f"{path.name} hardcodes a real vendor hostname ({host})"
            )
