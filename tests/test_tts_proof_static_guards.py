"""Phase 13I — governed local TTS proof static / structural guards.

These prove the *negative-space* invariants that keep the proof a backend/local
boundary: it adds no local bridge action, no frontend TTS trigger, and no
network dependency; its artifacts default under the archive-excluded ``runs/``
tree and are excluded from the packaged artifact; and the CLI surface exposes
exactly the one backend-only command.
"""

from __future__ import annotations

import re
import subprocess
import tarfile
from pathlib import Path

from typer.testing import CliRunner

from storytime.cli.app import app
from storytime.tts_proof.config import DEFAULT_ARTIFACT_DIR

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC = _REPO_ROOT / "src" / "storytime"
_TTS_PROOF = _SRC / "tts_proof"
_FRONTEND_SRC = _REPO_ROOT / "frontend" / "src"
_BUILD_SCRIPT = _REPO_ROOT / "scripts" / "build-artifact.sh"

runner = CliRunner()


def _py_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.py"))


# ── no new local bridge action ────────────────────────────────────────────────


def test_tts_proof_package_does_not_import_local_bridge() -> None:
    for path in _py_files(_TTS_PROOF):
        text = path.read_text(encoding="utf-8")
        assert "local_bridge" not in text, f"{path} references local_bridge"


def test_no_new_bridge_action_literal_in_local_bridge() -> None:
    actions = (_SRC / "local_bridge" / "actions.py").read_text(encoding="utf-8")
    lowered = actions.lower()
    for forbidden in ("generate_tts", "tts_proof", '"tts"', "'tts'", "generate_audio"):
        assert forbidden not in lowered, (
            f"local_bridge/actions.py unexpectedly mentions {forbidden!r}"
        )


def test_no_tts_or_generate_http_route_in_backend() -> None:
    pattern = re.compile(r"(POST\s+/tts|POST\s+/generate|/tts\b|/generate\b)")
    offenders: list[str] = []
    for path in _py_files(_SRC):
        # The tts_proof package legitimately names itself; scan the bridge/http
        # surfaces for any new generation route.
        if "local_bridge" not in str(path) and "http" not in str(path):
            continue
        if pattern.search(path.read_text(encoding="utf-8")):
            offenders.append(str(path))
    assert not offenders, f"unexpected TTS/generate HTTP route in: {offenders}"


# ── no frontend TTS trigger ───────────────────────────────────────────────────


def test_frontend_has_no_tts_generation_control() -> None:
    # Phase 13J adds sanctioned READ-ONLY TTS understanding to the frontend, so
    # the mere word "tts" is now expected. What must never appear is a TTS
    # *generation* control: a generate_tts action, a Generate-audio affordance,
    # or a fetch/POST to a TTS generation route. (The Phase 13J operator-GUI
    # guard, test_frontend_operator_gui_polish, additionally locks the read-only
    # framing of that TTS copy.)
    if not _FRONTEND_SRC.is_dir():  # pragma: no cover - frontend always present
        return
    offenders: list[str] = []
    for path in (*_FRONTEND_SRC.rglob("*.ts"), *_FRONTEND_SRC.rglob("*.tsx")):
        lowered = path.read_text(encoding="utf-8").lower()
        if (
            "generate_tts" in lowered
            or "generateaudio" in lowered
            or "generate audio" in lowered
        ):
            offenders.append(str(path))
    assert not offenders, f"frontend unexpectedly adds a TTS generation control: {offenders}"


# ── no network dependency in the package ──────────────────────────────────────


def test_tts_proof_package_imports_no_network_libraries() -> None:
    forbidden = (
        "import requests",
        "import httpx",
        "import urllib",
        "urllib.request",
        "http.client",
        "import socket",
        "import boto3",
        "google.cloud",
        "import aiohttp",
    )
    for path in _py_files(_TTS_PROOF):
        text = path.read_text(encoding="utf-8")
        for needle in forbidden:
            assert needle not in text, f"{path} imports network lib {needle!r}"


# ── artifact directory is archive-clean by construction ───────────────────────


def test_default_artifact_dir_is_under_runs() -> None:
    parts = DEFAULT_ARTIFACT_DIR.parts
    assert parts and parts[0] == "runs", (
        "the default TTS artifact dir must live under runs/ so it is git- and "
        f"archive-excluded; got {DEFAULT_ARTIFACT_DIR}"
    )


def test_packaged_archive_excludes_generated_tts_artifacts(tmp_path: Path) -> None:
    """Planting audio/manifest/audit under runs/tts-proof, the built archive
    must exclude them — proving generated runtime output never leaks."""
    run_dir = _REPO_ROOT / "runs" / "tts-proof" / "PROBE0000000000000000000000"
    planted = [
        run_dir / "audio.wav",
        run_dir / "manifest.json",
        run_dir / "audit.jsonl",
    ]
    try:
        run_dir.mkdir(parents=True, exist_ok=True)
        for p in planted:
            p.write_bytes(b"planted-tts-runtime-output")

        output = tmp_path / "tts-hygiene-probe.tar.gz"
        result = subprocess.run(  # noqa: S603 - fixed, trusted local script
            ["bash", str(_BUILD_SCRIPT), str(output)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, f"packaging script failed: {result.stderr}"
        with tarfile.open(output, "r:gz") as tar:
            members = tar.getnames()
        leaked = [
            m
            for m in members
            if "tts-proof" in m
            or m.endswith("audio.wav")
            or m.endswith(("manifest.json", "audit.jsonl"))
            and "runs/" in m
        ]
        assert not leaked, f"archive leaked generated TTS artifacts: {leaked[:5]}"
    finally:
        for p in planted:
            p.unlink(missing_ok=True)
        for d in (run_dir, run_dir.parent):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
        runs = _REPO_ROOT / "runs"
        if runs.is_dir() and not any(runs.iterdir()):
            runs.rmdir()


# ── CLI surface ────────────────────────────────────────────────────────────────


def test_tts_proof_command_is_present_and_runs(tmp_path: Path) -> None:
    listing = runner.invoke(app, ["--help"])
    assert listing.exit_code == 0
    assert "tts-proof" in listing.output

    help_result = runner.invoke(app, ["tts-proof", "--help"])
    assert help_result.exit_code == 0
    assert "--fixture-id" in help_result.output
    # It must NOT accept arbitrary text / file / URL input.
    lowered = help_result.output.lower()
    assert "--text" not in lowered
    assert "--file" not in lowered
    assert "--url" not in lowered

    # Running it (mock default, artifact dir pointed at a temp location) succeeds.
    env = {"STORYTIME_TTS_ARTIFACT_DIR": str(tmp_path / "tts")}
    run_result = runner.invoke(app, ["tts-proof"], env=env)
    assert run_result.exit_code == 0, run_result.output
    assert "tts proof OK" in run_result.output
