# StoryTime application image — Phase 7C.1 (a.k.a. Phase 7D) optional local
# app containerization, under the locked Phase 7C / 7C.1 Architecture Baseline
# amendment.
#
# SCOPE LOCK: This image is for OPTIONAL, LOCAL, SINGLE-HOST, DEMO-GRADE use
# only. It is built on the developer's local Docker daemon and is never pushed
# to any registry (no Docker Hub / ECR / GHCR / GCP Artifact Registry / ACR).
# Bare-metal local Python (`uv run storytime ...`) remains the DEFAULT and
# fully supported way to run StoryTime; Docker is optional and is never
# required by the six quality gates. No cloud, no Kubernetes, no Terraform,
# no production server, no vendor telemetry — see docs/deployment-containerized.md.
#
# The image runs the existing StoryTime CLI unchanged: pipeline commands write
# the SQLite state of truth, and `serve` runs the loopback-only feed server.

# Pinned base — a specific patch tag, not a floating tag.
FROM python:3.12.3-slim-bookworm

# ffmpeg: the only system dependency — the MP3 assembly stage uses it, and
# `storytime doctor` reports it. Installed with --no-install-recommends and
# the apt lists removed to keep the image lean. No other apt packages.
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# uv — pinned to the version the project's tooling uses. Copied from the
# official uv image at a fixed tag (build-time pull of a base image; this is
# not registry publishing). uv installs ONLY the locked dependency set.
COPY --from=ghcr.io/astral-sh/uv:0.11.7 /uv /uvx /usr/local/bin/

# Never reach out to download a Python runtime at build or run time; use the
# interpreter already in the base image. Copy link mode avoids cross-filesystem
# hardlink warnings.
ENV UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/app/.venv/bin:${PATH}"

WORKDIR /app

# Only the files needed to build and install the project. runs/, feed/, .env,
# secrets, caches, and local artifacts are excluded by .dockerignore and must
# never enter the build context or the image.
COPY pyproject.toml uv.lock README.md ./
COPY src ./src

# Install the locked runtime dependency set + the storytime package itself.
# --frozen: fail rather than silently re-resolve, so the image matches uv.lock
# exactly. --no-dev: dev tooling (pytest/ruff/mypy/import-linter) is not in the
# runtime image. No unpinned dependency is installed.
RUN uv sync --frozen --no-dev

# Non-root runtime user with a fixed UID for predictable volume ownership.
# The per-slot named volumes mount at /app/runs and /app/feed; pre-creating and
# chowning those directories in the image means a freshly-created named volume
# inherits non-root ownership on first mount, so the app can write its SQLite
# state and feed without running as root. (Phase 7C.1: prefer non-root.)
RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin storytime \
 && mkdir -p /app/runs /app/feed \
 && chown -R storytime:storytime /app/runs /app/feed

USER storytime

# `storytime` is the installed console script. The compose file runs `serve`
# for a live feed slot; pipeline commands are run with `docker compose exec`.
# This is a local CLI/feed runtime, not a production server.
ENTRYPOINT ["storytime"]
CMD ["--help"]
