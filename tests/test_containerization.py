"""Phase 7C.1 — optional app containerization, validated as data.

Every test here checks the containerization *configuration* (Dockerfile,
.dockerignore, the app compose file, dependency set, docs) and the stable
telemetry-identity logic. None of them requires Docker to be installed or a
container to be running, so the six quality gates stay Docker-free. A live
container smoke check is documented in docs/deployment-containerized.md as an
optional, manual step.

Coverage maps to the locked Phase 7C / 7C.1 amendment:

* the image build context excludes runs/, feed/, .env, and secret patterns;
* .dockerignore enforces that exclusion;
* the app compose file gives blue and green strictly separate named volumes
  for state and feed, never broadly publishes a port, never host-bind-mounts
  SQLite state, and never containerizes the front door;
* (Phase 7D.1) the app compose builds one shared image from exactly one
  service, both slots run that same image, and the consuming service never
  pulls it — so `docker compose build` and a fresh-cache `up -d` both work;
* no registry/push, Kubernetes, Terraform, Helm, CI/CD image build, or vendor
  telemetry fan-out config is introduced;
* service.instance.id is stable, slot-derived, and identical regardless of
  runtime identity (hostname / PID / container id);
* no OpenTelemetry resource-detector package is added, and the explicitly
  constructed resource is authoritative even against OTEL_RESOURCE_ATTRIBUTES;
* the docs carry the state-divergence warning and the local-only guardrails.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import yaml

from storytime.config import load_config

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DOCKERFILE = _REPO_ROOT / "Dockerfile"
_DOCKERIGNORE = _REPO_ROOT / ".dockerignore"
_APP_COMPOSE = _REPO_ROOT / "docker-compose.app.yml"


# -- helpers -----------------------------------------------------------------

def _dockerfile_copy_sources() -> list[str]:
    """Every source token of every COPY instruction in the Dockerfile.

    A COPY is ``COPY [--flags] src... dest``; the final token is the
    destination, the rest (minus flags) are sources. ``--from=...`` copies
    from another image, not the build context, so its sources are excluded.
    """
    sources: list[str] = []
    for raw in _DOCKERFILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.upper().startswith("COPY "):
            continue
        tokens = line.split()[1:]
        from_other_image = any(t.startswith("--from=") for t in tokens)
        tokens = [t for t in tokens if not t.startswith("--")]
        if from_other_image or len(tokens) < 2:
            continue
        sources.extend(tokens[:-1])
    return sources


def _app_compose() -> dict:
    return yaml.safe_load(_APP_COMPOSE.read_text(encoding="utf-8"))


def _active_volume_entries(service: dict) -> list[str]:
    """The service's volume entries (commented-out examples are not parsed)."""
    return [v for v in service.get("volumes", []) if isinstance(v, str)]


def _read_env_file(name: str) -> dict[str, str]:
    """Parse a `config/deploy/<name>` env file into a {KEY: VALUE} dict."""
    values: dict[str, str] = {}
    path = _REPO_ROOT / "config" / "deploy" / name
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip()
    return values


# -- Dockerfile --------------------------------------------------------------

def test_dockerfile_exists() -> None:
    assert _DOCKERFILE.is_file(), "Phase 7C.1 requires an application Dockerfile"


def test_dockerfile_does_not_copy_runtime_artifacts_or_secrets() -> None:
    """The image build must not bake in runs/, feed/, .env, or secret files."""
    forbidden = ("runs", "feed", ".env", ".local.env", ".secret.env")
    for src in _dockerfile_copy_sources():
        assert src not in (".", "./"), f"Dockerfile must not COPY the whole context ({src!r})"
        low = src.lower()
        for bad in forbidden:
            assert bad not in low, f"Dockerfile COPY must not include {bad!r} (source {src!r})"


def test_dockerfile_runs_as_non_root() -> None:
    text = _DOCKERFILE.read_text(encoding="utf-8")
    assert re.search(r"^USER\s+storytime", text, re.MULTILINE), (
        "Phase 7C.1 prefers a non-root runtime user"
    )


def test_dockerfile_pins_its_base_image() -> None:
    """No floating tags — the base image is pinned to a specific version."""
    for raw in _DOCKERFILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.upper().startswith("FROM "):
            ref = line.split()[1]
            assert ":" in ref, f"FROM image must be tagged/pinned, got {ref!r}"
            assert not ref.endswith(":latest"), f"FROM must not float on :latest ({ref!r})"


# -- .dockerignore -----------------------------------------------------------

def test_dockerignore_excludes_required_paths_and_secrets() -> None:
    assert _DOCKERIGNORE.is_file(), "Phase 7C.1 requires a .dockerignore"
    body = _DOCKERIGNORE.read_text(encoding="utf-8")
    required = [
        "runs/", "feed/", ".env", "*.local.env", "*.secret.env",
        ".venv/", "__pycache__/", ".pytest_cache/", ".mypy_cache/",
        ".ruff_cache/", "build/", "dist/",
    ]
    for pattern in required:
        assert pattern in body, f".dockerignore must exclude {pattern!r}"


# -- app compose: volumes, ports, front door --------------------------------

def test_app_compose_is_valid_yaml_with_two_slot_services() -> None:
    compose = _app_compose()
    services = compose.get("services", {})
    assert set(services) == {"storytime-blue", "storytime-green"}, (
        "the app compose defines exactly the blue and green slots"
    )


def test_app_compose_uses_separate_named_volumes_per_slot() -> None:
    """Blue and green get strictly isolated named volumes for state and feed."""
    compose = _app_compose()
    declared = set(compose.get("volumes", {}) or {})
    expected = {
        "storytime-blue-state", "storytime-blue-feed",
        "storytime-green-state", "storytime-green-feed",
    }
    assert expected <= declared, f"missing top-level named volumes: {expected - declared}"

    services = compose["services"]
    blue = {v.split(":")[0] for v in _active_volume_entries(services["storytime-blue"])}
    green = {v.split(":")[0] for v in _active_volume_entries(services["storytime-green"])}
    assert {"storytime-blue-state", "storytime-blue-feed"} <= blue
    assert {"storytime-green-state", "storytime-green-feed"} <= green
    # No SQLite-bearing volume is shared between slots (no merged state).
    assert blue.isdisjoint(green), f"blue and green must not share a volume: {blue & green}"


def test_app_compose_does_not_host_bind_mount_sqlite_state() -> None:
    """State must live on named volumes, never a cross-platform host bind mount."""
    compose = _app_compose()
    for name, service in compose["services"].items():
        for entry in _active_volume_entries(service):
            source, _, target = entry.partition(":")
            target = target.split(":")[0]
            is_bind = source.startswith((".", "/", "~"))
            if is_bind:
                assert "/app/runs" not in target, (
                    f"{name}: SQLite state ({target}) must not be a host bind mount"
                )
                assert entry.endswith(":ro"), (
                    f"{name}: a host bind mount must be read-only ({entry!r})"
                )


def test_app_compose_never_broadly_publishes_a_port() -> None:
    """Backend ports must be loopback-only — no 0.0.0.0, no bare host:container."""
    compose = _app_compose()
    for name, service in compose["services"].items():
        ports = service.get("ports", [])
        if not ports:
            # No published ports — acceptable only with host networking, where
            # the app itself binds 127.0.0.1 (Architecture Baseline §15).
            assert service.get("network_mode") == "host", (
                f"{name}: with no published ports, network_mode must be host"
            )
            continue
        for entry in ports:
            spec = entry if isinstance(entry, str) else str(entry.get("published", ""))
            assert "0.0.0.0" not in spec, f"{name}: 0.0.0.0 port binding is forbidden"
            assert spec.startswith("127.0.0.1"), (
                f"{name}: published ports must bind 127.0.0.1 only, got {entry!r}"
            )


def test_app_compose_does_not_containerize_the_front_door() -> None:
    """The Phase 7B native Python front door stays a host process."""
    body = _APP_COMPOSE.read_text(encoding="utf-8").lower()
    for service in _app_compose()["services"]:
        assert "frontdoor" not in service and "front-door" not in service
    # No proxy sneaks in as a service image either.
    for proxy in ("nginx", "caddy", "envoy", "traefik", "kong"):
        assert f"image: {proxy}" not in body, f"no {proxy} proxy container in the app compose"


# -- Phase 7D.1 build contract: one build, one image, no parallel-export race -

def test_app_compose_builds_the_image_from_exactly_one_service() -> None:
    """Exactly one service carries a `build:` section.

    Regression guard for the Phase 7D.1 race: when *both* slot services
    declared `build:` and exported the same image tag, a parallel
    `docker compose build` raced on the image export ("image already exists").
    With a single builder there is exactly one export and no race.
    """
    services = _app_compose()["services"]
    builders = [name for name, svc in services.items() if "build" in svc]
    assert len(builders) == 1, (
        f"exactly one service may own `build:` (the shared-image builder); "
        f"found {builders}"
    )


def test_app_compose_both_slots_run_the_same_image() -> None:
    """Blue and green run from one shared local image (constraint: same image)."""
    services = _app_compose()["services"]
    blue_image = services["storytime-blue"].get("image")
    green_image = services["storytime-green"].get("image")
    assert blue_image and green_image, "both slot services must name an `image:`"
    assert blue_image == green_image, (
        f"blue and green must share one image; got {blue_image!r} vs {green_image!r}"
    )


def test_app_compose_consuming_service_never_pulls_the_local_image() -> None:
    """The non-building service must not try to pull the local-only image tag.

    The shared image (`storytime-app:local`) exists only locally — it is built,
    never pushed to a registry. On a fresh Docker cache, `docker compose up -d`
    must not attempt to pull it for the consuming service. `pull_policy: never`
    encodes that: Compose uses the locally built image and never reaches a
    registry. This is the static proxy for "empty-cache `up -d` accounted for".
    """
    services = _app_compose()["services"]
    consumers = [name for name, svc in services.items() if "build" not in svc]
    assert consumers, "expected one consuming (non-building) service"
    for name in consumers:
        policy = services[name].get("pull_policy")
        assert policy == "never", (
            f"{name}: a service consuming the local-only image must set "
            f"`pull_policy: never` so empty-cache `up -d` does not try to pull "
            f"a non-registry tag; got {policy!r}"
        )


def test_app_compose_both_slots_use_host_networking() -> None:
    """Both slots keep `network_mode: host` (loopback-only — §15 preserved)."""
    for name, service in _app_compose()["services"].items():
        assert service.get("network_mode") == "host", (
            f"{name}: network_mode must remain host"
        )
        assert "ports" not in service, (
            f"{name}: no `ports:` mapping — host networking is the strategy"
        )


def test_slot_env_files_bind_loopback_on_distinct_ports() -> None:
    """Blue and green bind 127.0.0.1 on distinct ports — no all-interface bind.

    Ports and the bind host come from the per-slot env files, not the compose
    file. Blue must be 8000, green 8001, both on loopback, and no env value may
    introduce a `0.0.0.0` (all-interface) bind escape hatch.
    """
    blue = _read_env_file("blue.env")
    green = _read_env_file("green.env")
    assert blue.get("STORYTIME_HTTP_HOST") == "127.0.0.1"
    assert green.get("STORYTIME_HTTP_HOST") == "127.0.0.1"
    assert blue.get("STORYTIME_HTTP_PORT") == "8000"
    assert green.get("STORYTIME_HTTP_PORT") == "8001"
    for slot, values in (("blue", blue), ("green", green)):
        for key, value in values.items():
            assert "0.0.0.0" not in value, (
                f"{slot}.env: {key} must not introduce a 0.0.0.0 bind"
            )
    # Telemetry stays opt-out by default in the containerized slots.
    assert blue.get("STORYTIME_TELEMETRY") == "noop"
    assert green.get("STORYTIME_TELEMETRY") == "noop"


# -- scope guards: no registry / k8s / terraform / CI / vendor fan-out -------

def test_no_registry_push_workflow_is_introduced() -> None:
    """Containers are local-daemon only — nothing pushes images anywhere."""
    for path in (_DOCKERFILE, _APP_COMPOSE):
        body = path.read_text(encoding="utf-8").lower()
        assert "docker push" not in body
        assert "docker login" not in body
    for script in (_REPO_ROOT / "scripts").glob("*.sh"):
        body = script.read_text(encoding="utf-8").lower()
        assert "docker push" not in body and "docker login" not in body


def test_no_kubernetes_terraform_or_helm_files() -> None:
    for pattern in ("*.tf", "Chart.yaml", "kustomization.yaml", "kustomization.yml"):
        hits = list(_REPO_ROOT.rglob(pattern))
        assert not hits, f"Phase 7C.1 forbids {pattern} files, found: {hits}"
    assert not (_REPO_ROOT / "k8s").exists()


def test_no_cicd_image_build_workflow_is_introduced() -> None:
    """No CI/CD workflow builds or pushes a container image.

    Phase 7C.1 forbids CI/CD *image build* config (see the module docstring).
    It was originally enforced as "no .github/workflows directory at all"
    because no CI of any kind existed yet. Phase 15C introduces a single
    static-deploy workflow (GitHub Pages) that builds the frontend and
    publishes static files — it builds no container image and pushes to no
    registry. This guard therefore now allows a workflows directory but scans
    every workflow for container-image build/push indicators, which remain
    forbidden. A GitLab image-build pipeline file is still forbidden outright.
    """
    image_build_tokens = (
        "docker build",
        "docker push",
        "docker/build-push-action",
        "build-push-action",
        "buildx",
        "docker/login-action",
        "docker login",
        "ghcr.io",
        "kaniko",
        "podman build",
    )
    workflows_dir = _REPO_ROOT / ".github" / "workflows"
    if workflows_dir.exists():
        for workflow in workflows_dir.rglob("*.y*ml"):
            body = workflow.read_text(encoding="utf-8").lower()
            present = [t for t in image_build_tokens if t in body]
            assert not present, f"{workflow.name} builds/pushes an image: {present}"
    assert not (_REPO_ROOT / ".gitlab-ci.yml").exists()


def test_vendor_export_config_is_confined_to_the_phase8c_optin_files() -> None:
    """Vendor export config exists ONLY in the explicit Phase 8C opt-in files.

    The Phase 7C / 7C.1 section 16 note's blanket "no vendor telemetry fan-out"
    was superseded - narrowly - by the locked Architecture Baseline Section 23
    amendment, and Phase 8C implements it. Vendor export config is now expected
    but must stay confined to the disabled-by-default Phase 8C opt-in files; it
    must not leak into the default local-only path. Datadog stays absent
    everywhere (23.4, 23.11 - deferred).
    """
    phase8c_optin = {
        _REPO_ROOT / "config" / "vendor" / "otel-collector.dynatrace.example.yaml",
        _REPO_ROOT / "config" / "vendor" / "otel-collector.newrelic.example.yaml",
        _REPO_ROOT / "docker-compose.vendor.dynatrace.yml",
        _REPO_ROOT / "docker-compose.vendor.newrelic.yml",
    }
    fanout_vendors = ("dynatrace", "newrelic", "new relic")
    for path in _REPO_ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in {".yml", ".yaml", ".toml", ".env"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        low = "\n".join(line.split("#", 1)[0] for line in text.splitlines()).lower()
        assert "datadog" not in low, f"{path.name} must not configure Datadog"
        if path in phase8c_optin:
            continue
        for vendor in fanout_vendors:
            assert vendor not in low, (
                f"{path.name} configures vendor {vendor!r} outside the "
                "Phase 8C opt-in files - the default path must stay local-only"
            )


def test_no_resource_detector_package_is_added() -> None:
    """No OpenTelemetry resource-detector dependency (would churn instance id)."""
    pyproject = (_REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
    assert "resourcedetector" not in pyproject
    assert "resource-detector" not in pyproject


# -- stable, slot-derived service.instance.id -------------------------------

def test_service_instance_id_is_slot_derived() -> None:
    blue = load_config({"STORYTIME_DEPLOYMENT_SLOT": "blue"})
    green = load_config({"STORYTIME_DEPLOYMENT_SLOT": "green"})
    assert blue.service_instance_id == "storytime-blue"
    assert green.service_instance_id == "storytime-green"


def test_service_instance_id_without_a_slot_is_environment_derived() -> None:
    assert load_config({}).service_instance_id == "storytime-local"
    assert load_config(
        {"STORYTIME_ENVIRONMENT": "demo"}
    ).service_instance_id == "storytime-demo"


def test_service_instance_id_is_identical_bare_metal_and_container_like() -> None:
    """The derivation ignores runtime identity, so it is the same in a container.

    A container sets HOSTNAME to the container id and runs at a different PID;
    none of that may influence the value — only the slot does.
    """
    bare_metal = load_config({"STORYTIME_DEPLOYMENT_SLOT": "blue"})
    container_like = load_config(
        {
            "STORYTIME_DEPLOYMENT_SLOT": "blue",
            "HOSTNAME": "3f9a1c2b7e4d",  # a container-id-shaped hostname
        }
    )
    assert bare_metal.service_instance_id == container_like.service_instance_id == "storytime-blue"


def test_service_instance_id_is_not_runtime_identity() -> None:
    """It is never the hostname or the PID — those churn and fragment entities."""
    config = load_config({"STORYTIME_DEPLOYMENT_SLOT": "blue"})
    assert config.service_instance_id != os.uname().nodename
    assert config.service_instance_id != str(os.getpid())


# -- explicit resource authority over detectors / env -----------------------

def test_otel_resource_uses_the_pinned_instance_id() -> None:
    from opentelemetry.sdk.metrics.export import InMemoryMetricReader
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    from storytime.adapters.telemetry.otel import OTelTelemetry

    exporter = InMemorySpanExporter()
    adapter = OTelTelemetry(
        otlp_endpoint="http://127.0.0.1:4318",
        deployment_slot="blue",
        service_instance_id="storytime-blue",
        span_exporter=exporter,
        metric_reader=InMemoryMetricReader(),
    )
    run = adapter.on_run_started("run-instance", {})
    adapter.on_run_ended(run, "succeeded")
    resource = exporter.get_finished_spans()[0].resource.attributes
    assert resource["service.instance.id"] == "storytime-blue"


def test_explicit_instance_id_wins_over_env_resource_attributes(monkeypatch) -> None:
    """OTEL_RESOURCE_ATTRIBUTES cannot override the pinned service.instance.id.

    This proves the explicitly-constructed resource is authoritative — a
    detector- or env-supplied container identity loses.
    """
    from opentelemetry.sdk.metrics.export import InMemoryMetricReader
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    from storytime.adapters.telemetry.otel import OTelTelemetry

    monkeypatch.setenv(
        "OTEL_RESOURCE_ATTRIBUTES", "service.instance.id=ephemeral-container-id"
    )
    exporter = InMemorySpanExporter()
    adapter = OTelTelemetry(
        otlp_endpoint="http://127.0.0.1:4318",
        deployment_slot="blue",
        service_instance_id="storytime-blue",
        span_exporter=exporter,
        metric_reader=InMemoryMetricReader(),
    )
    run = adapter.on_run_started("run-authority", {})
    adapter.on_run_ended(run, "succeeded")
    resource = exporter.get_finished_spans()[0].resource.attributes
    assert resource["service.instance.id"] == "storytime-blue", (
        "the explicit, slot-derived instance id must win over the env detector"
    )


def test_config_module_does_not_import_opentelemetry() -> None:
    """OpenTelemetry import isolation: the instance-id change stays OTel-free.

    (The lint-imports gate enforces this repo-wide; this is a fast local guard
    on the module the Phase 7C.1 change touched.)
    """
    source = (_REPO_ROOT / "src" / "storytime" / "config.py").read_text(encoding="utf-8")
    assert "import opentelemetry" not in source
    assert "from opentelemetry" not in source


# -- documentation honesty --------------------------------------------------

def test_docs_carry_the_blue_green_state_divergence_warning() -> None:
    doc = (_REPO_ROOT / "docs" / "deployment-containerized.md").read_text(encoding="utf-8")
    low = doc.lower()
    assert "isolated state" in low or "state divergence" in low
    assert "does not" in low and ("merge" in low or "migrate" in low)


def test_docs_carry_the_containerization_guardrails() -> None:
    doc = (_REPO_ROOT / "docs" / "deployment-containerized.md").read_text(encoding="utf-8").lower()
    for guardrail in ("optional", "loopback", "named volume", "no registry", "bare-metal"):
        assert guardrail in doc, f"deployment-containerized.md must state: {guardrail!r}"
