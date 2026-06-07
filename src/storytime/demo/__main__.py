"""``python -m storytime.demo`` — run the observability demo harness.

CLI-adjacent on purpose: this is a developer/demo tool, kept out of the locked
``storytime`` command surface. It drives the same public pipeline entry points
the real CLI uses.

Typical use::

    docker compose -f docker-compose.observability.yml up -d
    python -m storytime.demo --log-dir logs
    # open Grafana at http://127.0.0.1:3000 — traces, metrics, and logs

``--log-dir`` (Phase 8B) writes a structured JSON-lines log file the Collector
``filelog`` receiver tails on its way to Loki. With ``--telemetry noop`` it
runs every scenario with telemetry disabled and needs no Docker — that is the
mode the test suite uses.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from storytime.demo.harness import SCENARIO_NAMES, format_report, run_demo


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, run the demo, print the report; return an exit code."""
    parser = argparse.ArgumentParser(
        prog="python -m storytime.demo",
        description="Run real StoryTime scenarios to populate local telemetry.",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path("demo-data"),
        help="Directory the demo writes into (created if absent). "
        "Default: ./demo-data",
    )
    parser.add_argument(
        "--telemetry",
        choices=("otel", "noop"),
        default="otel",
        help="Telemetry adapter. 'otel' exports real telemetry to the "
        "collector; 'noop' runs the same scenarios with telemetry off. "
        "Default: otel",
    )
    parser.add_argument(
        "--otlp-endpoint",
        default="http://127.0.0.1:4318",
        help="OTLP/HTTP endpoint of the local collector. "
        "Default: http://127.0.0.1:4318",
    )
    parser.add_argument(
        "--scenario",
        action="append",
        choices=SCENARIO_NAMES,
        metavar="NAME",
        help="Run only this scenario (repeatable). Default: all scenarios.",
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=None,
        help="If set, write a structured JSON-lines log file here (Phase 8B). "
        "This directory is what docker-compose.observability.yml mounts into "
        "the OpenTelemetry Collector for the filelog -> Loki path; use "
        "'--log-dir logs'. Default: off (no log file written).",
    )
    args = parser.parse_args(argv)

    scenarios = tuple(args.scenario) if args.scenario else None
    result = run_demo(
        workspace=args.workspace,
        telemetry=args.telemetry,
        otlp_endpoint=args.otlp_endpoint,
        scenarios=scenarios,
        log_dir=args.log_dir,
    )
    print(format_report(result))
    if args.log_dir is not None:
        print(
            f"  logs      : structured demo log written under {args.log_dir} "
            "(routed to Loki by the Collector filelog receiver)"
        )
    return 0 if result.ok else 1


if __name__ == "__main__":  # pragma: no cover - module entry point
    sys.exit(main())
