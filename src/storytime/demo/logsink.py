"""Structured JSON-lines log sink for the Phase 8B local log-routing demo.

ARCH-LOCK: Log sink is plain structured file logging — NOT OTLP log export
DO NOT REFACTOR: Phase 8B routes logs to Loki via the OpenTelemetry Collector
``filelog`` receiver, not via Python OTLP log export (Architecture Baseline
Section 23.9 / 23.13). This module therefore only writes JSON lines to a local
file; it imports no ``opentelemetry`` and opens no network connection. It is
the demo's log *source*; the Collector is the router.

Data hygiene (Architecture Baseline Section 23.8): every field written here is
control-plane metadata — scenario name (a closed set), pipeline run id (a
ULID), status strings, the service version, booleans, and a short bounded
message. Raw story text, generated narration, RSS XML, source payloads, and
secrets are never placed in a log record.

The file is one JSON object per line (JSON Lines), append-only, so repeated
demo runs accumulate and the Collector ``filelog`` receiver can tail it.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from storytime.demo.harness import DemoResult, DemoScenarioResult

# The single demo log file. docker-compose.observability.yml mounts the
# directory holding it into the collector at /var/log/storytime, and the
# collector's filelog receiver tails ``*.log``.
DEMO_LOG_FILENAME = "storytime-demo.log"

# Bound for the free-text ``message`` field. The structured fields are all
# closed-set / identifier values; only ``message`` is composed text, and it is
# kept short so a log line can never carry a payload.
_MAX_MESSAGE_LEN = 200


def _utc_now() -> str:
    """Return the current UTC time as a fixed, unambiguous ISO-8601 string."""
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _bounded(text: str) -> str:
    """Return *text* truncated to the message length bound."""
    if len(text) <= _MAX_MESSAGE_LEN:
        return text
    return text[:_MAX_MESSAGE_LEN]


def scenario_record(
    scenario: DemoScenarioResult, *, service_version: str, environment: str
) -> dict[str, object]:
    """Build the control-plane-only log record for one demo scenario."""
    return {
        "timestamp": _utc_now(),
        "level": "info" if scenario.ok else "error",
        "logger": "storytime.demo",
        "service.name": "storytime",
        "service.version": service_version,
        "deployment.environment": environment,
        "event": "demo.scenario",
        "scenario": scenario.name,
        "pipeline.run_id": scenario.pipeline_run_id or "",
        "status": scenario.actual,
        "expected": scenario.expected,
        "ok": scenario.ok,
        "message": _bounded(
            f"demo scenario {scenario.name}: expected {scenario.expected}, "
            f"got {scenario.actual}"
        ),
    }


def summary_record(
    result: DemoResult, *, service_version: str
) -> dict[str, object]:
    """Build the control-plane-only summary log record for a demo run."""
    return {
        "timestamp": _utc_now(),
        "level": "info" if result.ok else "error",
        "logger": "storytime.demo",
        "service.name": "storytime",
        "service.version": service_version,
        "deployment.environment": "demo",
        "event": "demo.summary",
        "scenario_count": len(result.scenarios),
        "ok": result.ok,
        "message": _bounded(
            f"demo run finished: {len(result.scenarios)} scenarios, "
            f"{'all met expectations' if result.ok else 'with failures'}"
        ),
    }


def write_demo_log(
    log_dir: Path, result: DemoResult, *, service_version: str
) -> Path:
    """Append the demo run's structured log lines to ``<log_dir>/<file>``.

    Writes one JSON line per scenario plus one summary line. *log_dir* is
    created if absent. Returns the path written. The file is opened in append
    mode so successive demo runs accumulate, which is what the Collector
    ``filelog`` receiver expects to tail.
    """
    log_dir = log_dir.resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / DEMO_LOG_FILENAME

    records: list[dict[str, object]] = [
        scenario_record(
            scenario,
            service_version=service_version,
            environment="demo",
        )
        for scenario in result.scenarios
    ]
    records.append(summary_record(result, service_version=service_version))

    with path.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
    return path


__all__ = [
    "DEMO_LOG_FILENAME",
    "scenario_record",
    "summary_record",
    "write_demo_log",
]
