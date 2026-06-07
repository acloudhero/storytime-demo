"""Import-boundary enforcement.

ARCH-LOCK: Telemetry Import Boundary Test
DO NOT REFACTOR: This test fails if any module other than
adapters/telemetry/otel.py imports opentelemetry. Do not relax it.
Rationale: Hard decision 2 of the Architecture Baseline. This is the test
referenced by Round 8 deliverable 27 and ARCH-LOCK location 9.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src" / "storytime"
_PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"

# The single module permitted to import opentelemetry.
_ALLOWED = _SRC / "adapters" / "telemetry" / "otel.py"


def _imports_opentelemetry(source: str) -> bool:
    """True if *source* contains a Python import of the opentelemetry package."""
    for raw in source.splitlines():
        line = raw.strip()
        if line.startswith("import opentelemetry") or line.startswith("from opentelemetry"):
            return True
    return False


def test_opentelemetry_is_confined_to_the_otel_adapter() -> None:
    offenders: list[str] = []
    for path in _SRC.rglob("*.py"):
        if path == _ALLOWED:
            continue
        if _imports_opentelemetry(path.read_text(encoding="utf-8")):
            offenders.append(str(path.relative_to(_SRC)))
    assert offenders == [], f"opentelemetry imported outside the telemetry adapter: {offenders}"


def test_the_otel_adapter_does_import_opentelemetry() -> None:
    # Confirms the boundary is meaningful: the one allowed module really uses it.
    assert _imports_opentelemetry(_ALLOWED.read_text(encoding="utf-8"))


def test_detector_flags_a_synthetic_violation() -> None:
    # Negative control: proves the scanner would catch a real violation.
    assert _imports_opentelemetry("from opentelemetry import trace")
    assert _imports_opentelemetry("import opentelemetry.sdk")
    assert not _imports_opentelemetry("import storytime.events  # opentelemetry word only")


def _otel_confinement_source_modules() -> list[str]:
    """Return source_modules of the import-linter OpenTelemetry-confinement contract."""
    config = tomllib.loads(_PYPROJECT.read_text(encoding="utf-8"))
    contracts = config["tool"]["importlinter"]["contracts"]
    for contract in contracts:
        if contract.get("forbidden_modules") == ["opentelemetry"]:
            return list(contract["source_modules"])
    raise AssertionError("OpenTelemetry-confinement contract not found in pyproject.toml")


def test_import_linter_contract_covers_storytime_pipeline() -> None:
    # The composition root must be a named source of the OTel-confinement
    # contract, so `lint-imports` — not only the source scan above — enforces
    # that storytime.pipeline never directly imports opentelemetry.
    assert "storytime.pipeline" in _otel_confinement_source_modules()


def test_pipeline_module_does_not_import_opentelemetry() -> None:
    # Behavioural counterpart to the contract check above.
    pipeline = _SRC / "pipeline.py"
    assert pipeline.is_file()
    assert not _imports_opentelemetry(pipeline.read_text(encoding="utf-8"))
