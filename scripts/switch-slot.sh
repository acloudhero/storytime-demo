#!/usr/bin/env bash
# StoryTime — active-slot switch (Phase 7B, Option B1).
#
# Points the front door at a slot by updating the active-slot pointer. The
# running front door reads that pointer on every request, so the switch takes
# effect for the next request — no proxy reload, no front-door restart.
#
# ROLLBACK is the same command targeting the previously-active slot:
#   scripts/switch-slot.sh green     # switch blue -> green
#   scripts/switch-slot.sh blue      # roll back  green -> blue
#
# This only updates the pointer file; it never touches runs/ or feed/, so the
# inactive slot is preserved untouched.
#
# This script installs nothing and downloads nothing.
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "usage: scripts/switch-slot.sh <slot>" >&2
  echo "  e.g. scripts/switch-slot.sh green" >&2
  exit 2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

if ! command -v uv >/dev/null 2>&1; then
  echo "switch-slot.sh: 'uv' was not found on PATH." >&2
  echo "  Install uv (https://docs.astral.sh/uv/) to run StoryTime." >&2
  exit 2
fi

exec uv run python -m storytime.frontdoor switch "$@"
