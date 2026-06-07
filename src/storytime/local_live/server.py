"""Phase 14A.1 — local-live loopback HTTP API.

A tiny standard-library (`http.server`) loopback service that exposes
backend-owned durable SQLite state to the operator console's Live Proof Loop
surface, plus one controlled proof-run action. No web framework is added; this
reuses the Phase 13 local-bridge security posture:

- binds **loopback only** (`127.0.0.1` / `localhost` / `::1`); a non-loopback
  bind is refused via :func:`storytime.http.server.validate_bind_host`,
- enforces a **strict origin allowlist** (loopback on the bound port plus the
  Vite dev origins on :5173); a request whose ``Origin`` is not allowlisted is
  ``403`` and **no wildcard** ``Access-Control-Allow-Origin`` is ever sent,
- serves **read-only** endpoints plus one controlled ``POST /api/proof-runs``
  that accepts only an allowlisted fixture id — never arbitrary text, paths,
  URLs, providers, or credentials.

Routes:
    GET  /health
    GET  /api/runs
    GET  /api/runs/{run_id}
    GET  /api/runs/{run_id}/artifacts
    GET  /api/runs/{run_id}/events
    POST /api/proof-runs        body: {} or {"fixture": "<allowlisted id>"}
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from storytime.http.server import validate_bind_host
from storytime.local_live import read_model, recovery
from storytime.local_live.observability import (
    WORK_ENQUEUED,
    NullQueueWorkerObserver,
    QueueWorkerEventSink,
    emit,
)
from storytime.local_live.proof_run import (
    APPROVED_FIXTURES,
    APPROVED_SCENARIOS,
    ProofRunError,
    default_fixtures_dir,
    reserve_proof_run,
    resolve_scenario,
)
from storytime.local_live.queue import SqliteWorkQueue
from storytime.local_live.worker import BackgroundWorker, LocalWorker
from storytime.state.store import StateStore

# Work-item ids share the proof run-id shape (opaque, safe character class).
_WORK_ID_PREFIX = "work-"

_LOOPBACK_CLIENTS = frozenset({"127.0.0.1", "::1", "::ffff:127.0.0.1"})

# Largest POST body accepted on the controlled action endpoint. The only valid
# body is a tiny JSON object, so anything larger is rejected outright.
_MAX_BODY_BYTES = 4096

# A run id is an opaque token; restrict to a safe character class so a path
# segment can never carry traversal or injection into a store lookup.
_RUN_ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,128}$")


def default_allowed_origins(port: int) -> frozenset[str]:
    """Loopback origins on the bound port plus the Vite dev origins (:5173)."""
    return frozenset(
        {
            f"http://127.0.0.1:{port}",
            f"http://localhost:{port}",
            "http://127.0.0.1:5173",
            "http://localhost:5173",
        }
    )


@dataclass(frozen=True, slots=True)
class LocalLiveService:
    """Backend-owned operations over the durable SQLite state store.

    A fresh :class:`StateStore` connection is opened per call so the service is
    safe to use from :class:`ThreadingHTTPServer` worker threads (a SQLite
    connection is single-thread). All state is durable; nothing is held in
    process memory.
    """

    db_path: Path
    runs_dir: Path
    fixtures_dir: Path
    mode: str = "local-live"
    observer: QueueWorkerEventSink = field(default_factory=NullQueueWorkerObserver)

    def health(self) -> tuple[int, dict[str, Any]]:
        run_count = 0
        queue_counts: dict[str, int] = {}
        db_present = self.db_path.is_file()
        if db_present:
            with StateStore.open(self.db_path) as store:
                run_count = len(store.list_runs())
                for item in store.list_work_items():
                    queue_counts[item.state] = queue_counts.get(item.state, 0) + 1
        return (
            200,
            {
                "status": "ok",
                "mode": self.mode,
                "loopbackOnly": True,
                "wildcardOriginAllowed": False,
                "stateOwner": "backend-sqlite",
                "stateStore": "sqlite",
                "dbName": self.db_path.name,
                "dbPresent": db_present,
                "runCount": run_count,
                "browserAuthority": "request-only",
                "persistence": "survives-local-server-restart",
                "scenarios": list(APPROVED_SCENARIOS),
                "execution": "queued-then-local-worker",
                "queueCounts": queue_counts,
            },
        )

    def list_runs(self) -> tuple[int, dict[str, Any]]:
        if not self.db_path.is_file():
            return (200, {"runs": [], "stateOwner": "backend-sqlite"})
        with StateStore.open(self.db_path) as store:
            runs = read_model.list_run_summaries(store)
        return (
            200,
            {"runs": [r.to_dict() for r in runs], "stateOwner": "backend-sqlite"},
        )

    def run_detail(self, run_id: str) -> tuple[int, dict[str, Any]]:
        if not self.db_path.is_file():
            return (404, {"error": "no_runs", "message": "no durable state yet"})
        with StateStore.open(self.db_path) as store:
            detail = read_model.get_run_detail(store, run_id, self.runs_dir)
            if detail is None:
                return (404, {"error": "not_found", "message": "run not found"})
            body = detail.to_dict()
            # Phase 14C.5.1: attach durable recovery lineage for this run (empty
            # unless recovery has been requested/evaluated). Backend-owned; the
            # recovery_action table is the source of truth, not observer events.
            actions = store.list_recovery_actions_for_run(run_id)
            body["recoveryActions"] = [
                read_model.map_recovery_action(a).to_dict() for a in actions
            ]
        return (200, body)

    def recovery_for_run(self, run_id: str) -> tuple[int, dict[str, Any]]:
        """Return the durable recovery lineage for an original run."""
        if not self.db_path.is_file():
            return (404, {"error": "no_runs", "message": "no durable state yet"})
        with StateStore.open(self.db_path) as store:
            if store.get_run(run_id) is None:
                return (404, {"error": "not_found", "message": "run not found"})
            actions = store.list_recovery_actions_for_run(run_id)
            body = {
                "originalRunId": run_id,
                "recoveryActions": [
                    read_model.map_recovery_action(a).to_dict() for a in actions
                ],
                "stateOwner": "backend-sqlite",
            }
        return (200, body)

    def request_recovery(self, payload: Any) -> tuple[int, dict[str, Any]]:
        """Operator-triggered recovery request for a failed run (backend-decided).

        The backend decides eligibility; the caller cannot. Returns the durable
        recovery action (HTTP 201 when a recovery execution was created, 200 when
        the request was durably rejected with a bounded decision).
        """
        if not isinstance(payload, dict):
            return (400, {"error": "bad_request", "message": "payload must be JSON"})
        original_run_id = payload.get("runId") or payload.get("originalRunId")
        if not isinstance(original_run_id, str) or not original_run_id.strip():
            return (
                400,
                {"error": "bad_request", "message": "runId is required"},
            )
        requested_by = payload.get("requestedBy")
        if not isinstance(requested_by, str) or not requested_by.strip():
            requested_by = "operator"
        reason = payload.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            reason = "operator-requested local recovery"
        if not self.db_path.is_file():
            return (404, {"error": "no_runs", "message": "no durable state yet"})
        with StateStore.open(self.db_path) as store:
            action = recovery.request_recovery(
                store,
                original_run_id,
                requested_by=requested_by,
                reason=reason,
                runs_dir=self.runs_dir,
                fixtures_dir=self.fixtures_dir,
            )
            view = read_model.map_recovery_action(action).to_dict()
        status = 201 if action.status == recovery.STATUS_CREATED else 200
        return (status, view)

    def run_artifacts(self, run_id: str) -> tuple[int, dict[str, Any]]:
        status, detail = self.run_detail(run_id)
        if status != 200:
            return (status, detail)
        return (200, {"runId": run_id, "artifacts": detail.get("artifacts", [])})

    def run_events(self, run_id: str) -> tuple[int, dict[str, Any]]:
        status, detail = self.run_detail(run_id)
        if status != 200:
            return (status, detail)
        return (200, {"runId": run_id, "events": detail.get("events", [])})

    def create_proof_run(self, payload: Any) -> tuple[int, dict[str, Any]]:
        """Validate the controlled action body and run a durable proof scenario.

        Accepts only ``{}`` or an object with any of the allowed keys
        ``fixture`` / ``fixtureId`` (the fixture id; ``fixture`` is a back-compat
        alias for ``fixtureId``) and ``scenario`` (an allowlisted scenario id).
        Any other shape, key, fixture, or scenario is rejected — the browser
        cannot submit free text, paths, URLs, providers, credentials, failure
        messages, or custom stage definitions.
        """
        fixture_id: str | None = None
        scenario: str | None = None
        if payload not in (None, {}):
            if not isinstance(payload, dict):
                return (
                    400,
                    {"error": "invalid_body", "message": "body must be a JSON object"},
                )
            allowed_keys = {"fixture", "fixtureId", "scenario"}
            extra = set(payload) - allowed_keys
            if extra:
                return (
                    400,
                    {
                        "error": "unexpected_fields",
                        "message": (
                            f"only {sorted(allowed_keys)} are accepted; "
                            f"got extra {sorted(extra)}"
                        ),
                    },
                )
            raw_fixture = payload.get("fixtureId", payload.get("fixture"))
            if raw_fixture is not None and not isinstance(raw_fixture, str):
                return (
                    400,
                    {"error": "invalid_fixture", "message": "fixture must be a string"},
                )
            fixture_id = raw_fixture
            raw_scenario = payload.get("scenario")
            if raw_scenario is not None and not isinstance(raw_scenario, str):
                return (
                    400,
                    {"error": "invalid_scenario", "message": "scenario must be a string"},
                )
            scenario = raw_scenario
        # Request acceptance reserves a durable run and enqueues a work item;
        # it does NOT execute inline. A local worker claims and executes the
        # queued item, so request acceptance is separated from execution.
        try:
            with StateStore.open(self.db_path) as store:
                run_id = reserve_proof_run(
                    store,
                    runs_dir=self.runs_dir,
                    fixture_id=fixture_id,
                    scenario=scenario,
                    fixtures_dir=self.fixtures_dir,
                )
                resolved_scenario = resolve_scenario(scenario)
                queue = SqliteWorkQueue(store)
                work_id = f"{_WORK_ID_PREFIX}{run_id}"
                resolved_fixture = self._resolved_fixture(fixture_id)
                queue.enqueue(
                    work_id=work_id,
                    pipeline_run_id=run_id,
                    scenario=resolved_scenario,
                    fixture_id=resolved_fixture,
                )
                store._conn.commit()  # noqa: SLF001 - persist enqueue durably
                run = store.get_run(run_id)
                work = queue.get(work_id)
            emit(
                self.observer,
                WORK_ENQUEUED,
                run_id=run_id,
                work_item_id=work_id,
                status="queued",
            )
        except ProofRunError as exc:
            return (
                400,
                {
                    "error": "rejected",
                    "message": str(exc),
                    "allowedFixtures": sorted(APPROVED_FIXTURES),
                    "allowedScenarios": list(APPROVED_SCENARIOS),
                },
            )
        status_value = run.status if run is not None else "queued"
        work_state = work.state if work is not None else "queued"
        return (
            202,
            {
                "runId": run_id,
                "workId": work_id,
                "status": status_value,
                "queueState": work_state,
                "scenario": resolve_scenario(scenario),
                "source": "approved-fixture",
                "stateOwner": "backend-sqlite",
                "accepted": True,
            },
        )

    @staticmethod
    def _resolved_fixture(fixture_id: str | None) -> str:
        from storytime.local_live.proof_run import resolve_fixture

        return resolve_fixture(fixture_id)

    def drain_queue(self, *, max_items: int = 64) -> int:
        """Synchronously drain the durable queue with a local worker.

        Returns the number of work items processed. Used by the running server's
        background worker and by tests (which drive draining deterministically
        rather than relying on the background thread's timing).
        """
        worker = LocalWorker(
            db_path=self.db_path,
            runs_dir=self.runs_dir,
            fixtures_dir=self.fixtures_dir,
            observer=self.observer,
        )
        return worker.drain(max_items=max_items)


class _LocalLiveHandler(BaseHTTPRequestHandler):
    """Loopback-only handler translating HTTP to :class:`LocalLiveService`."""

    # Injected by make_server via a subclass closure.
    service: LocalLiveService
    allowed_origins: frozenset[str]
    server_version = "StoryTimeLocalLive/1.0"

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        # Quiet by default; the operator sees the request in the browser.
        return

    # -- origin / loopback enforcement ------------------------------------

    def _client_is_loopback(self) -> bool:
        return self.client_address[0] in _LOOPBACK_CLIENTS

    def _origin_ok(self) -> bool:
        origin = self.headers.get("Origin")
        return origin is None or origin in self.allowed_origins

    def _send(self, status: int, body: dict[str, Any]) -> None:
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        origin = self.headers.get("Origin")
        if origin is not None and origin in self.allowed_origins:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(payload)

    def _reject(self, status: int, code: str, message: str) -> None:
        self._send(status, {"error": code, "message": message})

    def _guard(self) -> bool:
        if not self._client_is_loopback():
            self._reject(403, "non_loopback_client", "loopback clients only")
            return False
        if not self._origin_ok():
            self._reject(403, "forbidden_origin", "origin not allowlisted")
            return False
        return True

    # -- dispatch ----------------------------------------------------------

    def do_OPTIONS(self) -> None:  # noqa: N802 - dispatch name
        if not self._client_is_loopback():
            self._reject(403, "non_loopback_client", "loopback clients only")
            return
        if not self._origin_ok():
            self._reject(403, "forbidden_origin", "origin not allowlisted")
            return
        self._send(204, {})

    def do_GET(self) -> None:  # noqa: N802 - dispatch name
        if not self._guard():
            return
        path = self.path.split("?", 1)[0].rstrip("/")
        if path in ("", "/health"):
            self._respond(self.service.health())
            return
        if path == "/api/runs":
            self._respond(self.service.list_runs())
            return
        detail = re.fullmatch(r"/api/runs/([^/]+)", path)
        if detail:
            run_id = self._safe_run_id(detail.group(1))
            if run_id is None:
                return
            self._respond(self.service.run_detail(run_id))
            return
        artifacts = re.fullmatch(r"/api/runs/([^/]+)/artifacts", path)
        if artifacts:
            run_id = self._safe_run_id(artifacts.group(1))
            if run_id is None:
                return
            self._respond(self.service.run_artifacts(run_id))
            return
        events = re.fullmatch(r"/api/runs/([^/]+)/events", path)
        if events:
            run_id = self._safe_run_id(events.group(1))
            if run_id is None:
                return
            self._respond(self.service.run_events(run_id))
            return
        self._reject(404, "not_found", "unknown route")

    def do_POST(self) -> None:  # noqa: N802 - dispatch name
        if not self._guard():
            return
        path = self.path.split("?", 1)[0].rstrip("/")
        if path != "/api/proof-runs":
            self._reject(404, "not_found", "unknown route")
            return
        length_raw = self.headers.get("Content-Length", "0")
        try:
            length = int(length_raw)
        except ValueError:
            self._reject(400, "invalid_length", "bad Content-Length")
            return
        if length > _MAX_BODY_BYTES:
            self._reject(413, "body_too_large", "proof action body too large")
            return
        payload: Any = {}
        if length > 0:
            raw = self.rfile.read(length)
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                self._reject(400, "invalid_json", "body must be JSON")
                return
        self._respond(self.service.create_proof_run(payload))

    # -- helpers -----------------------------------------------------------

    def _safe_run_id(self, raw: str) -> str | None:
        if not _RUN_ID_RE.fullmatch(raw):
            self._reject(400, "invalid_run_id", "malformed run id")
            return None
        return raw

    def _respond(self, result: tuple[int, dict[str, Any]]) -> None:
        status, body = result
        self._send(status, body)


def make_server(
    service: LocalLiveService,
    *,
    host: str = "127.0.0.1",
    port: int = 8770,
    allowed_origins: frozenset[str] | None = None,
    start_worker: bool = False,
) -> ThreadingHTTPServer:
    """Build a loopback-bound ThreadingHTTPServer for the local-live API.

    When ``start_worker`` is True a single local background worker thread is
    attached to drain the durable queue on a bounded interval (used by the
    running ``storytime local-live`` server). Tests default to
    ``start_worker=False`` and drive draining synchronously via
    :meth:`LocalLiveService.drain_queue` for determinism.
    """
    bind_host = validate_bind_host(host)
    origins = allowed_origins or default_allowed_origins(port)

    class _Handler(_LocalLiveHandler):
        pass

    _Handler.service = service
    _Handler.allowed_origins = origins
    httpd = ThreadingHTTPServer((bind_host, port), _Handler)
    if start_worker:
        worker = LocalWorker(
            db_path=service.db_path,
            runs_dir=service.runs_dir,
            fixtures_dir=service.fixtures_dir,
        )
        background = BackgroundWorker(worker)
        background.start()
        # Stash so the caller (serve) can stop it cleanly on shutdown.
        httpd.storytime_background_worker = background  # type: ignore[attr-defined]
    return httpd


def serve(
    *,
    db_path: Path,
    runs_dir: Path,
    fixtures_dir: Path | None = None,
    host: str = "127.0.0.1",
    port: int = 8770,
) -> None:
    """Blocking entry point used by the ``storytime local-live`` command."""
    service = LocalLiveService(
        db_path=db_path,
        runs_dir=runs_dir,
        fixtures_dir=fixtures_dir or default_fixtures_dir(),
    )
    httpd = make_server(service, host=host, port=port, start_worker=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        background = getattr(httpd, "storytime_background_worker", None)
        if background is not None:
            background.stop()
        httpd.server_close()
