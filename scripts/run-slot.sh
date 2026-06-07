#!/usr/bin/env bash
# StoryTime — blue/green Option A slot launcher (Phase 7A).
#
# Loads a per-slot environment file from config/deploy/<slot>.env and runs the
# storytime CLI inside it. This is the lean Option A "deployment unit": a
# storytime process configured for one slot. There is no container, no
# orchestrator, and no traffic switch — that bounded simplicity is the whole
# point of Option A (see docs/deployment-bluegreen-option-a.md).
#
# Usage:
#   scripts/run-slot.sh <slot> <storytime args...>
#
# Examples:
#   scripts/run-slot.sh blue  doctor
#   scripts/run-slot.sh green run --manifest sources/the-raven.json
#   scripts/run-slot.sh blue  serve            # serves feed/blue on its port
#
# The slot env file sets STORYTIME_DEPLOYMENT_SLOT, so the state root
# (runs/<slot>) and feed root (feed/<slot>) are separated automatically. No
# secret is read or required; StoryTime is local-first.
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "usage: scripts/run-slot.sh <slot> <storytime args...>" >&2
  echo "  e.g. scripts/run-slot.sh blue doctor" >&2
  exit 2
fi

slot="$1"
shift

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
env_file="${repo_root}/config/deploy/${slot}.env"

if [ ! -f "${env_file}" ]; then
  echo "run-slot.sh: no env file for slot '${slot}' at ${env_file}" >&2
  echo "  available slots:" >&2
  ls -1 "${repo_root}/config/deploy/" 2>/dev/null | sed 's/\.env$//; s/^/    /' >&2
  exit 2
fi

# Export every assignment in the slot env file, then run storytime in it.
set -a
# shellcheck disable=SC1090
. "${env_file}"
set +a

cd "${repo_root}"
exec uv run storytime "$@"
