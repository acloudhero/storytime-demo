#!/usr/bin/env bash
# StoryTime — blue/green front-door launcher (Phase 7B, Option B1).
#
# Starts the native StoryTime front door: a loopback-only reverse proxy that
# routes a single stable port to whichever slot the active-slot pointer names.
#
# NO EXTERNAL PROXY BINARY. The front door is native Python (standard library
# only) — there is no Caddy/nginx/Envoy to install. The only requirement is
# Python + uv, which are already required to run StoryTime at all. This script
# therefore never downloads or installs anything.
#
# Usage:
#   scripts/run-frontdoor.sh                       # 127.0.0.1:8080
#   scripts/run-frontdoor.sh --port 8080
#   scripts/run-frontdoor.sh --deploy-dir config/deploy
#
# Switch which slot it serves with:  scripts/switch-slot.sh <blue|green>
# (the running front door picks up the change on the next request).
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

# Fail clearly if the runtime is missing. There is no proxy binary to check —
# the front door IS Python — so the only dependency is uv/Python itself.
if ! command -v uv >/dev/null 2>&1; then
  echo "run-frontdoor.sh: 'uv' was not found on PATH." >&2
  echo "  Install uv (https://docs.astral.sh/uv/) to run StoryTime." >&2
  echo "  Note: the front door is native Python — there is no separate proxy" >&2
  echo "  binary to install, and this script will not download one." >&2
  exit 2
fi

exec uv run python -m storytime.frontdoor serve "$@"
