"""Process configuration.

Configuration is loaded once at CLI entry from environment variables (with
safe defaults) into an immutable StoryTimeConfig. It is then carried by the
frozen RunnerContext. Nothing here is a secret; StoryTime is local-first and
makes no authenticated API calls.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

VALID_TELEMETRY = ("noop", "otel")

# ARCH-LOCK: Deployment slot is a path segment (Phase 7A)
# DO NOT REFACTOR: Phase 7A makes ``deployment_slot`` derive the per-slot state
# and feed roots (runs/<slot>, feed/<slot>) so blue and green never share a
# SQLite DB or feed by accident. Because the slot now influences filesystem
# paths it MUST be a single safe path segment — no slashes, no leading dot, no
# traversal. This pattern is the mechanical guard; load_config rejects anything
# else fail-fast at startup.
# Rationale: Phase 7A hard constraint 5 (honest blue/green state separation).
_SLOT_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def is_valid_slot_name(name: str) -> bool:
    """True if *name* is a safe deployment-slot identifier.

    A safe slot is a short lowercase token matching ``[a-z0-9][a-z0-9._-]*``:
    no slashes, no leading dot, no whitespace, no shell metacharacters, no
    path traversal. ``load_config`` (Phase 7A) and the Phase 7B front-door
    active-slot pointer share this single rule so a slot value can never
    escape a workspace path or be unsafe to embed in a command.
    """
    return bool(_SLOT_PATTERN.fullmatch(name))


@dataclass(frozen=True, slots=True)
class StoryTimeConfig:
    """Immutable process configuration.

    ARCH-LOCK: Immutable Config
    DO NOT REFACTOR: Keep this frozen. Configuration must not be mutated after
    load; the RunnerContext depends on it being a stable orchestration value.

    Phase 5 added two telemetry-resource fields, ``environment`` and
    ``deployment_slot``. They are deliberately generic, defaulted, and
    environment-driven: telemetry resource identity must never hard-code
    "local only" or bind to a host/path, so a blue/green deployment can
    attribute traces by environment and slot without touching business logic.
    ``deployment_slot`` is empty by default (no slot).

    Phase 7A (blue/green Option A) gives ``deployment_slot`` a second job: when
    it is set, the per-run state root and the feed root default to slot-scoped
    sub-directories (``runs/<slot>`` and ``feed/<slot>``), so two slots on one
    host get independent SQLite databases and feeds without the operator having
    to remember to override both paths. An explicit ``STORYTIME_RUNS_DIR`` /
    ``STORYTIME_FEED_DIR`` still wins — sharing state between slots is possible
    but only as a visible, deliberate override, never the silent default.
    """

    runs_dir: Path
    feed_dir: Path
    telemetry: str
    otlp_endpoint: str
    http_host: str
    http_port: int
    environment: str = "local"
    deployment_slot: str = ""
    # Phase 9B (Architecture Baseline §24.9): path to the local, inspectable
    # blocked-source config. Defaulted and repo-relative; an absent file simply
    # means an empty deny-list (the loader tolerates that). Overridable via
    # STORYTIME_BLOCKED_SOURCES so a test or an operator can point at another
    # file without touching code.
    governance_blocked_sources_path: Path = Path("config/governance/blocked-sources.yaml")

    @property
    def service_version(self) -> str:
        """The service version reported as a telemetry resource attribute."""
        from storytime import __version__

        return __version__

    @property
    def deployment_label(self) -> str:
        """Human-facing ``environment[/slot]`` identity of this deployment.

        ``"local"`` with no slot; ``"staging/blue"`` for environment
        ``staging``, slot ``blue``. Used by the CLI deployment banner and the
        Phase 7A documentation; it is presentation only and never a path.
        """
        if self.deployment_slot:
            return f"{self.environment}/{self.deployment_slot}"
        return self.environment

    @property
    def service_instance_id(self) -> str:
        """Stable, slot-derived OpenTelemetry ``service.instance.id``.

        ARCH-LOCK: Resource Identity Contract (Phase 7C / 7C.1 amendment)
        DO NOT REFACTOR: This value is derived ONLY from the deployment slot
        (or, with no slot, the environment) so it is byte-identical whether
        StoryTime runs bare-metal or inside a container. It is deliberately
        NOT a container ID, PID, hostname, IP address, random value, or start
        timestamp: those churn on every rebuild/restart and would fragment a
        slot into many short-lived telemetry entities. ``storytime-blue`` /
        ``storytime-green`` keep each slot a single, stable instance across
        restarts and across the bare-metal/container boundary. Derived, not
        configurable, on purpose — there is no env knob that could be pointed
        at an unstable runtime value.
        """
        if self.deployment_slot:
            return f"storytime-{self.deployment_slot}"
        return f"storytime-{self.environment}"

    @property
    def state_db_path(self) -> Path:
        """Path to the SQLite state database inside the runs directory."""
        return self.runs_dir / "state.db"

    def run_dir(self, pipeline_run_id: str) -> Path:
        """Working directory for a single pipeline run."""
        return self.runs_dir / pipeline_run_id


def load_config(environ: dict[str, str] | None = None) -> StoryTimeConfig:
    """Build a StoryTimeConfig from *environ* (defaults to os.environ).

    Raises ValueError on an invalid telemetry selection, a non-integer port, or
    an unsafe deployment slot, so misconfiguration fails fast at startup rather
    than mid-run.

    Phase 7A path resolution: ``deployment_slot`` scopes the *default* state and
    feed roots. With no slot the defaults are ``runs`` / ``feed`` exactly as
    before. With ``STORYTIME_DEPLOYMENT_SLOT=blue`` the defaults become
    ``runs/blue`` / ``feed/blue``. An explicit ``STORYTIME_RUNS_DIR`` or
    ``STORYTIME_FEED_DIR`` always overrides the slot-scoped default — so the
    safe, separated layout is the default and a shared layout is only ever a
    deliberate, visible override.
    """
    env = dict(os.environ) if environ is None else environ

    telemetry = env.get("STORYTIME_TELEMETRY", "noop").strip().lower()
    if telemetry not in VALID_TELEMETRY:
        raise ValueError(
            f"STORYTIME_TELEMETRY must be one of {VALID_TELEMETRY}, got {telemetry!r}"
        )

    port_raw = env.get("STORYTIME_HTTP_PORT", "8000").strip()
    try:
        http_port = int(port_raw)
    except ValueError as exc:
        raise ValueError(f"STORYTIME_HTTP_PORT must be an integer, got {port_raw!r}") from exc

    # Generic, configurable telemetry-resource identity. Defaults keep the
    # local-first experience intact; a blue/green rollout sets these without
    # changing any business logic.
    environment = env.get("STORYTIME_ENVIRONMENT", "local").strip() or "local"
    deployment_slot = env.get("STORYTIME_DEPLOYMENT_SLOT", "").strip()
    if deployment_slot and not is_valid_slot_name(deployment_slot):
        # The slot is now a filesystem path segment (runs/<slot>); a value with
        # a slash, a leading dot, or traversal could escape the workspace.
        raise ValueError(
            "STORYTIME_DEPLOYMENT_SLOT must be a short lowercase identifier "
            "matching [a-z0-9][a-z0-9._-]* (e.g. 'blue', 'green') — no slashes "
            f"or path traversal, got {deployment_slot!r}"
        )

    # Slot-scoped defaults: with a slot, runs/<slot> and feed/<slot> keep blue
    # and green on independent state. An explicit override (key present) always
    # wins so a shared layout stays possible but never accidental.
    default_runs = Path("runs") / deployment_slot if deployment_slot else Path("runs")
    default_feed = Path("feed") / deployment_slot if deployment_slot else Path("feed")
    runs_dir = (
        Path(env["STORYTIME_RUNS_DIR"])
        if "STORYTIME_RUNS_DIR" in env
        else default_runs
    )
    feed_dir = (
        Path(env["STORYTIME_FEED_DIR"])
        if "STORYTIME_FEED_DIR" in env
        else default_feed
    )

    # Phase 9B (§24.9): the local blocked-source config path. The default is
    # repo-relative; STORYTIME_BLOCKED_SOURCES overrides it. The loader treats
    # an absent file as an empty deny-list, so a non-repo working directory is
    # safe — it never makes the fail-closed gate fail open.
    governance_blocked_sources_path = Path(
        env.get(
            "STORYTIME_BLOCKED_SOURCES",
            "config/governance/blocked-sources.yaml",
        )
    )

    return StoryTimeConfig(
        runs_dir=runs_dir,
        feed_dir=feed_dir,
        telemetry=telemetry,
        otlp_endpoint=env.get("STORYTIME_OTLP_ENDPOINT", "http://127.0.0.1:4318"),
        http_host=env.get("STORYTIME_HTTP_HOST", "127.0.0.1"),
        http_port=http_port,
        environment=environment,
        deployment_slot=deployment_slot,
        governance_blocked_sources_path=governance_blocked_sources_path,
    )


def deployment_summary(config: StoryTimeConfig) -> list[str]:
    """Return the operator-facing deployment-identity banner lines.

    Phase 7A: ``storytime doctor`` prints this so an operator can confirm which
    blue/green slot a process is configured for, and which state/feed roots it
    will touch, before running anything. Presentation only — it derives every
    line from the immutable config and changes no behaviour.
    """
    return [
        f"deployment:    {config.deployment_label}",
        f"  environment: {config.environment}",
        f"  slot:        {config.deployment_slot or '(none)'}",
        f"  instance id: {config.service_instance_id}",
        f"  state root:  {config.runs_dir}",
        f"  state db:    {config.state_db_path}",
        f"  feed root:   {config.feed_dir}",
        f"  telemetry:   {config.telemetry}",
    ]
