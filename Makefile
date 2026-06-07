# StoryTime developer tasks. Run `make help` for the list.
.PHONY: help sync test lint typecheck imports check run-doctor clean \
	logs-dir observability-up observability-down demo

help:
	@echo "make sync            install runtime + dev dependencies (uv)"
	@echo "make test            run the pytest suite"
	@echo "make lint            run ruff"
	@echo "make typecheck       run mypy (strict)"
	@echo "make imports         run import-linter contracts"
	@echo "make check           lint + typecheck + imports + test"
	@echo "make run-doctor      run the environment doctor"
	@echo "make clean           remove tooling caches"
	@echo "make observability-up    create ./logs, then start the observability stack"
	@echo "make observability-down  stop the observability stack"
	@echo "make demo            create ./logs, then run the observability demo"

sync:
	uv sync --extra dev

test:
	uv run pytest -q

lint:
	uv run ruff check .

typecheck:
	uv run mypy

imports:
	uv run lint-imports

check: lint typecheck imports test

run-doctor:
	uv run storytime doctor

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache

# --- Observability stack (Docker; optional) -------------------------------
# Preflight: `./logs` must exist BEFORE `docker compose up`, because
# docker-compose.observability.yml bind-mounts it into the Collector. If Docker
# created it instead, it could be root-owned and the local Python demo could
# not write logs/storytime-demo.log. `logs-dir` creates it as the current user
# first; observability-up and demo both depend on it.
logs-dir:
	mkdir -p logs

observability-up: logs-dir
	docker compose -f docker-compose.observability.yml up -d

observability-down:
	docker compose -f docker-compose.observability.yml down

demo: logs-dir
	uv run python -m storytime.demo --log-dir logs
