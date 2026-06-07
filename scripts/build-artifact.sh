#!/usr/bin/env bash
# StoryTime — deterministic artifact packaging with archive-hygiene excludes.
#
# Phase 13G.1: the Phase 13G artifact accidentally included the runtime SQLite
# database runs/state.db (created by `storytime doctor` in the working tree).
# This script is the canonical packaging path: it tars the repository directory
# with explicit --exclude patterns so runtime database / journal artifacts,
# tool caches, virtualenvs, node_modules, frontend build output, env files, and
# nested review archives can NEVER be packaged again — even if they are present
# in the working tree at build time.
#
# Usage:
#   scripts/build-artifact.sh [OUTPUT.tar.gz]
#
# Defaults to ../storytime-artifact.tar.gz next to the repository directory.
# Deterministic: sorted names, numeric 0:0 owner/group, so identical trees
# produce identical archives.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PARENT_DIR="$(dirname "${REPO_ROOT}")"
REPO_NAME="$(basename "${REPO_ROOT}")"
OUTPUT="${1:-${PARENT_DIR}/storytime-artifact.tar.gz}"

cd "${PARENT_DIR}"

tar \
  --sort=name \
  --owner=0 --group=0 --numeric-owner \
  --exclude="__pycache__" \
  --exclude="*.pyc" \
  --exclude="*.pyo" \
  --exclude=".pytest_cache" \
  --exclude=".ruff_cache" \
  --exclude=".mypy_cache" \
  --exclude=".import_linter_cache" \
  --exclude=".venv" \
  --exclude="venv" \
  --exclude="node_modules" \
  --exclude="${REPO_NAME}/frontend/dist" \
  --exclude="*.tsbuildinfo" \
  --exclude=".git" \
  --exclude=".env" \
  --exclude="*.local.env" \
  --exclude="*.secret.env" \
  --exclude="*.db" \
  --exclude="*.sqlite" \
  --exclude="*.sqlite3" \
  --exclude="*.db-wal" \
  --exclude="*.db-shm" \
  --exclude="${REPO_NAME}/runs" \
  --exclude="${REPO_NAME}/feed" \
  --exclude="${REPO_NAME}/logs" \
  --exclude="${REPO_NAME}/operator-report" \
  --exclude="*.mp3" \
  --exclude="*.wav" \
  --exclude="*.mp4" \
  --exclude="*.tar.gz" \
  --exclude="*.tgz" \
  --exclude="*.zip" \
  -czf "${OUTPUT}" "${REPO_NAME}"

echo "built ${OUTPUT}"
sha256sum "${OUTPUT}"
