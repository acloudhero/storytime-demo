"""StoryTime command-line interface.

The CLI is built with Typer (typed command signatures over Click). It exposes
environment diagnostics, manifest validation, the vertical-slice `run` command
(with the approval gates and resume), run-status inspection over the local
SQLite state database, and the canonical per-stage command surface (`ingest`,
`approve`, `synthesize`, `assemble`, `publish`).

Phase 4 made the per-stage commands real (docs/open-issues.md, OI-12), backed
by the persisted approval gate (OI-9) and resume/rehydration (OI-10). Phase 4.1
wires the audio approval gate as a second, independent gate (OI-13): `run` and
`ingest` accept `--require-audio-approval`, and `approve` accepts
`--stage audio`. A run that reaches any gate pauses and exits cleanly — it
never hangs.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

import typer

from storytime import __version__
from storytime.adapters.storage import LocalFilesystemStorage
from storytime.approval import ApprovalError, apply_approval_decision
from storytime.config import deployment_summary, load_config
from storytime.doctor import run_doctor
from storytime.http import LocalFeedServer, UnsafeBindError
from storytime.http.server import validate_bind_host
from storytime.local_live import serve as serve_local_live
from storytime.local_live.proof_run import default_fixtures_dir
from storytime.manifest import ManifestValidationError, load_manifest
from storytime.operator_export import (
    DEFAULT_EXPORT_RELPATH,
    write_static_demo_export,
)
from storytime.operator_queue import (
    DEFAULT_LIMIT,
    QueueStatusError,
    collect_queue,
    render_json,
    render_table,
)
from storytime.operator_rerun import (
    perform_rerun,
    render_rerun_json,
    render_rerun_text,
)
from storytime.pipeline import (
    SliceOutcome,
    build_runtime_context,
    resume_run,
    run_vertical_slice,
)
from storytime.reporting import generate_report
from storytime.runner import RehydrationError
from storytime.state import StateStore
from storytime.tts_proof import (
    DEFAULT_FIXTURE_ID,
    load_tts_proof_config,
    run_tts_proof,
)
from storytime.util.clock import SystemClock, to_iso

app = typer.Typer(
    name="storytime",
    help="StoryTime — local-first, observability-native content-to-audio pipeline.",
    no_args_is_help=True,
    add_completion=False,
)


@app.command()
def version() -> None:
    """Print the StoryTime version."""
    typer.echo(f"storytime {__version__}")


@app.command()
def doctor() -> None:
    """Check the local environment and report dependency status.

    Phase 7A: the report opens with a deployment-identity banner — the
    resolved environment, blue/green slot, and the state/feed roots this
    process is configured for — so an operator can confirm which slot they are
    about to act on. A configuration error is shown in the banner but does not
    suppress the dependency checks below it.
    """
    try:
        config = load_config()
    except ValueError as exc:
        typer.echo(f"deployment:    configuration error — {exc}")
    else:
        for line in deployment_summary(config):
            typer.echo(line)
    typer.echo("")

    report = run_doctor()
    for check in report.checks:
        mark = "ok " if check.ok else ("MISSING" if not check.required else "FAIL")
        tag = "" if check.required else " (optional)"
        typer.echo(f"[{mark:>7}] {check.name}{tag}: {check.detail}")
    if report.healthy:
        typer.echo("environment: healthy")
    else:
        typer.echo("environment: required checks failed")
        raise typer.Exit(code=1)


@app.command(name="validate-manifest")
def validate_manifest_cmd(
    manifest: Annotated[
        Path, typer.Argument(help="Path to a source manifest JSON file.")
    ],
) -> None:
    """Validate a source manifest against the closed schema."""
    try:
        parsed = load_manifest(manifest)
    except ManifestValidationError as exc:
        typer.echo(f"INVALID: {manifest}")
        for message in exc.messages:
            typer.echo(f"  - {message}")
        raise typer.Exit(code=1) from exc
    typer.echo(
        f"VALID: {manifest} (source_id={parsed.source_id}, license={parsed.license})"
    )


# --------------------------------------------------------------------------
# Shared outcome reporting.
# --------------------------------------------------------------------------

def _report_outcome(outcome: SliceOutcome) -> None:
    """Print a SliceOutcome and exit non-zero on a failure outcome.

    A run that pauses at an approval gate is NOT a failure: it prints the
    awaiting-approval guidance and exits cleanly (code 0).
    """
    run_id = outcome.pipeline_run_id

    if outcome.status == "rejected":
        typer.echo("REJECTED: manifest failed pre-flight validation.")
        for message in outcome.messages:
            typer.echo(f"  - {message}")
        raise typer.Exit(code=1)

    if outcome.status == "failed":
        if outcome.failed_stage in ("approve_text", "approve_audio"):
            gate = outcome.failed_stage.removeprefix("approve_")
            typer.echo(
                f"REJECTED: run {run_id} — the {gate} was rejected at the "
                "approval gate."
            )
            typer.echo(f"  {outcome.error_message}")
        else:
            typer.echo(
                f"FAILED: run {run_id} failed at stage '{outcome.failed_stage}'"
            )
            typer.echo(f"  {outcome.error_kind}: {outcome.error_message}")
        raise typer.Exit(code=1)

    if outcome.status == "awaiting_approval":
        gate = outcome.awaiting_gate or "text"
        typer.echo(
            f"AWAITING APPROVAL: run {run_id} paused at the {gate} approval gate."
        )
        typer.echo("  The run state is persisted; this process exited cleanly.")
        typer.echo(
            f"  Approve with: storytime approve {run_id} "
            f"--stage {gate} --decision approve"
        )
        typer.echo(f"  Then resume:  storytime run --resume {run_id}")
        return

    if outcome.status == "stage_completed":
        typer.echo(f"STAGE COMPLETE: run {run_id} — '{outcome.last_stage}' finished.")
        # `run --resume` continues correctly whatever comes next — a further
        # stage or a pause at the next gate — so it is the safe suggestion.
        typer.echo(f"  continue with: storytime run --resume {run_id}")
        typer.echo(f"  inspect with:  storytime status {run_id}")
        return

    # completed
    typer.echo(f"COMPLETED: run {run_id}")
    typer.echo(f"  episode_guid: {outcome.episode_guid}")
    typer.echo(f"  feed:         {outcome.feed_path}")
    typer.echo(f"  inspect with: storytime status {run_id}")


# --------------------------------------------------------------------------
# run — the vertical-slice convenience wrapper (fresh run or resume).
# --------------------------------------------------------------------------

@app.command()
def run(
    manifest: Annotated[
        Path | None,
        typer.Option(
            "--manifest", "-m", help="Path to a source manifest JSON file."
        ),
    ] = None,
    resume: Annotated[
        str | None,
        typer.Option("--resume", help="A pipeline_run_id of a paused run to continue."),
    ] = None,
    require_approval: Annotated[
        bool,
        typer.Option(
            "--require-approval",
            "-A",
            help="Insert the persisted text approval gate; pause for an operator.",
        ),
    ] = False,
    require_audio_approval: Annotated[
        bool,
        typer.Option(
            "--require-audio-approval",
            help="Insert the persisted audio approval gate (after synthesis); "
            "pause for an operator before assembly.",
        ),
    ] = False,
    auto_approve: Annotated[
        bool,
        typer.Option(
            "--auto-approve",
            help="Insert the text gate but satisfy every gate automatically "
            "(records real approval decisions). Local convenience; never a "
            "silent bypass.",
        ),
    ] = False,
) -> None:
    """Run the vertical slice, or resume a paused run.

    Without flags this is the Phase 3 slice end to end: ingest -> synthesize
    -> assemble -> publish. --require-approval inserts the text approval gate
    (after ingest); --require-audio-approval inserts the audio approval gate
    (after synthesis); the two are independent. The run pauses at each gate and
    exits cleanly; continue it later with --resume RUN_ID.
    """
    if resume is not None and manifest is not None:
        typer.echo("ERROR: pass either --manifest (fresh run) or --resume, not both.")
        raise typer.Exit(code=1)
    if resume is None and manifest is None:
        typer.echo("ERROR: provide --manifest PATH for a new run, or --resume RUN_ID.")
        raise typer.Exit(code=1)

    config = load_config()
    ctx = build_runtime_context(config)
    try:
        if resume is not None:
            outcome = resume_run(ctx, resume)
        else:
            assert manifest is not None
            outcome = run_vertical_slice(
                ctx,
                manifest,
                require_approval=require_approval,
                require_audio_approval=require_audio_approval,
                auto_approve=auto_approve,
            )
    except RehydrationError as exc:
        typer.echo(f"ERROR: {exc}")
        raise typer.Exit(code=1) from exc
    finally:
        ctx.state.close()

    _report_outcome(outcome)


# --------------------------------------------------------------------------
# Canonical per-stage command surface (real behaviour).
#
# The Product Charter and Architecture Baseline define a granular command for
# each pipeline stage. `ingest` starts a fresh run that pauses at the text
# approval gate; `approve` records an operator decision (text or audio gate);
# `synthesize`, `assemble`, and `publish` rehydrate the run from SQLite and
# carry it forward. Each is honest: it does real work, or stops cleanly at a
# gate, or fails with a clear message — never a silent no-op.
# --------------------------------------------------------------------------

@app.command()
def ingest(
    manifest: Annotated[
        Path,
        typer.Option("--manifest", "-m", help="Path to a source manifest JSON file."),
    ],
    require_audio_approval: Annotated[
        bool,
        typer.Option(
            "--require-audio-approval",
            help="Also insert the audio approval gate after synthesis.",
        ),
    ] = False,
) -> None:
    """Ingest a source text and pause at the text approval gate (canonical stage 1).

    Creates a pipeline run, validates and ingests the manifest's text, then
    pauses at the persisted text approval gate. Approve with `storytime
    approve`, then carry the run forward with `synthesize` / `assemble` /
    `publish` or `run --resume`. With --require-audio-approval the run will
    also pause at the audio gate after synthesis.
    """
    config = load_config()
    ctx = build_runtime_context(config)
    try:
        outcome = run_vertical_slice(
            ctx,
            manifest,
            require_approval=True,
            require_audio_approval=require_audio_approval,
        )
    finally:
        ctx.state.close()
    _report_outcome(outcome)


@app.command()
def approve(
    pipeline_run_id: Annotated[
        str, typer.Argument(help="The pipeline_run_id of the run awaiting approval.")
    ],
    stage: Annotated[
        str,
        typer.Option("--stage", help="Approval gate to decide: 'text' or 'audio'."),
    ] = "text",
    decision: Annotated[
        str,
        typer.Option("--decision", help="Operator decision: 'approve' or 'reject'."),
    ] = "approve",
    operator: Annotated[
        str, typer.Option("--operator", help="Name recorded as the deciding operator.")
    ] = "operator",
    notes: Annotated[
        str, typer.Option("--notes", help="Optional free-text review notes.")
    ] = "",
) -> None:
    """Record an operator approval decision for a pending run (canonical stage 2).

    --stage selects the gate: 'text' (after ingest) or 'audio' (after
    synthesis). The decision is persisted as an approval row plus a
    TextApproved/TextRejected or AudioApproved/AudioRejected event in one
    transaction. A rejection moves the run to a failed state and blocks every
    downstream stage.
    """
    if stage not in ("text", "audio"):
        typer.echo(
            f"ERROR: --stage must be 'text' or 'audio', got {stage!r}."
        )
        raise typer.Exit(code=1)
    if decision not in ("approve", "reject"):
        typer.echo(f"ERROR: --decision must be 'approve' or 'reject', got {decision!r}.")
        raise typer.Exit(code=1)
    normalised = "approved" if decision == "approve" else "rejected"

    config = load_config()
    ctx = build_runtime_context(config)
    try:
        result = apply_approval_decision(
            ctx,
            pipeline_run_id=pipeline_run_id,
            gate=stage,
            decision=normalised,
            operator=operator,
            notes=notes or None,
        )
    except ApprovalError as exc:
        typer.echo(f"ERROR: {exc}")
        raise typer.Exit(code=1) from exc
    finally:
        ctx.state.close()

    if result.decision == "approved":
        typer.echo(
            f"APPROVED: run {pipeline_run_id} — {stage} gate approved by {operator}."
        )
        typer.echo(f"  resume with: storytime run --resume {pipeline_run_id}")
    else:
        typer.echo(
            f"REJECTED: run {pipeline_run_id} — {stage} gate rejected by {operator}."
        )
        typer.echo("  the run is now failed; downstream stages are blocked.")


def _resume_to(stage_name: str, pipeline_run_id: str) -> None:
    """Shared body for the synthesize / assemble / publish stage commands."""
    config = load_config()
    ctx = build_runtime_context(config)
    try:
        outcome = resume_run(ctx, pipeline_run_id, stop_after=stage_name)
    except RehydrationError as exc:
        typer.echo(f"ERROR: {exc}")
        raise typer.Exit(code=1) from exc
    finally:
        ctx.state.close()
    _report_outcome(outcome)


@app.command()
def synthesize(
    pipeline_run_id: Annotated[
        str, typer.Argument(help="The pipeline_run_id to carry forward.")
    ],
) -> None:
    """Synthesize audio for an approved, ingested run (canonical stage 3).

    Rehydrates the run from SQLite and runs up to and including synthesize. If
    the text approval gate is still undecided the run pauses cleanly instead.
    """
    _resume_to("synthesize", pipeline_run_id)


@app.command()
def assemble(
    pipeline_run_id: Annotated[
        str, typer.Argument(help="The pipeline_run_id to carry forward.")
    ],
) -> None:
    """Assemble an MP3 episode for a synthesized run (canonical stage 4).

    Rehydrates the run from SQLite and runs up to and including assemble. If
    the run has an undecided audio approval gate it pauses cleanly instead.
    """
    _resume_to("assemble", pipeline_run_id)


@app.command()
def publish(
    pipeline_run_id: Annotated[
        str, typer.Argument(help="The pipeline_run_id to carry forward.")
    ],
) -> None:
    """Publish the RSS feed for an assembled run (canonical stage 5).

    Rehydrates the run from SQLite and runs through publish, completing the run.
    """
    _resume_to("publish", pipeline_run_id)


@app.command()
def status(
    pipeline_run_id: Annotated[
        str | None,
        typer.Argument(help="A pipeline_run_id to inspect. Omit to list all runs."),
    ] = None,
) -> None:
    """Show pipeline run status from the local SQLite state database."""
    config = load_config()
    with StateStore.open(config.state_db_path) as store:
        if pipeline_run_id is None:
            runs = store.list_runs()
            if not runs:
                typer.echo("no pipeline runs recorded yet.")
                return
            typer.echo(f"{len(runs)} run(s):")
            for listed in runs:
                typer.echo(
                    f"  {listed.pipeline_run_id}  {listed.status:>16}  "
                    f"stage={listed.current_stage}  created={listed.created_at}"
                )
            return

        record = store.get_run(pipeline_run_id)
        if record is None:
            typer.echo(f"no run found with pipeline_run_id={pipeline_run_id}")
            raise typer.Exit(code=1)

        typer.echo(f"run {record.pipeline_run_id}")
        typer.echo(f"  status:        {record.status}")
        typer.echo(f"  current stage: {record.current_stage}")
        typer.echo(f"  created:       {record.created_at}")
        typer.echo(f"  updated:       {record.updated_at}")
        typer.echo(
            f"  gates:         {', '.join(record.gates) if record.gates else 'none'}"
        )

        # Manifest provenance approval (recorded by ingest, stage_name
        # "ingest") — distinct from the operator gate decisions below.
        provenance = store.latest_approval(pipeline_run_id, "ingest")
        if provenance is not None:
            typer.echo(
                f"  manifest approval: {provenance.decision} by "
                f"{provenance.operator} (rights clearance from the manifest)"
            )

        # Phase 9B: the governance Trust Envelope decision (Architecture
        # Baseline §24.6/§24.15). This is the queryable SQLite projection; the
        # durable Trust Envelope artifact remains the governance source of
        # truth. The status enum (APPROVED / REJECTED / BLOCKED / NEEDS_REVIEW)
        # is shown as recorded — never presented as a legal certification.
        governance = store.latest_trust_envelope(pipeline_run_id)
        if governance is not None:
            line = (
                f"  governance:    {governance.decision} "
                f"(licence {governance.license_type}, "
                f"by {governance.approver_id})"
            )
            if governance.blocked_reason:
                line += f" — {governance.blocked_reason}"
            typer.echo(line)

        # Operator approval gate decisions, one line per configured gate.
        for gate_label in record.gates:
            gate_stage = f"approve_{gate_label}"
            decision = store.latest_approval(pipeline_run_id, gate_stage)
            if decision is not None:
                typer.echo(
                    f"  {gate_label} gate:    {decision.decision} by "
                    f"{decision.operator} at {decision.decided_at}"
                )
            elif record.status == "awaiting_approval" and (
                record.current_stage == gate_stage
            ):
                typer.echo(
                    f"  {gate_label} gate:    awaiting an operator decision"
                )
            else:
                typer.echo(f"  {gate_label} gate:    pending")

        typer.echo("  stages:")
        for execution in store.list_stage_executions(pipeline_run_id):
            note = "" if execution.error_kind is None else f"  [{execution.error_kind}]"
            typer.echo(f"    {execution.stage_name:>12}: {execution.status}{note}")
        typer.echo("  events:")
        for event_type in store.event_types(pipeline_run_id):
            typer.echo(f"    {event_type}")


@app.command()
def queue(
    status: Annotated[
        str | None,
        typer.Option(
            "--status",
            help=(
                "Filter by attention reason: 'failed', 'blocked', "
                "'needs-review', or 'awaiting-approval'."
            ),
        ),
    ] = None,
    run_id: Annotated[
        str | None,
        typer.Option("--run-id", help="Restrict the queue to a single run."),
    ] = None,
    limit: Annotated[
        int,
        typer.Option("--limit", help="Maximum runs to show (bounded; default 20)."),
    ] = DEFAULT_LIMIT,
    as_json: Annotated[
        bool,
        typer.Option("--json", help="Emit deterministic machine-readable JSON."),
    ] = False,
) -> None:
    """Show pipeline runs that need operator attention.

    A read-only failure / review queue: a bounded, deterministic view over the
    local SQLite state of runs that are failed, blocked by governance, marked
    needs-review, or awaiting an operator approval decision. For each run it
    shows why it needs attention and which existing command, report, or
    artifact to inspect next. It is a viewer only — it changes no state and
    runs no other command. Output is most-recently-updated first.
    """
    config = load_config()
    with StateStore.open(config.state_db_path) as store:
        if run_id is not None and store.get_run(run_id) is None:
            typer.echo(f"no run found with run_id={run_id}")
            raise typer.Exit(code=1)
        try:
            items = collect_queue(
                store, status=status, run_id=run_id, limit=limit
            )
        except (QueueStatusError, ValueError) as exc:
            typer.echo(f"ERROR: {exc}")
            raise typer.Exit(code=1) from exc

    if as_json:
        typer.echo(render_json(items))
        return
    if run_id is not None and not items:
        typer.echo(
            f"run {run_id} is not currently in the failure/review queue."
        )
        return
    typer.echo(render_table(items))


@app.command()
def rerun(
    pipeline_run_id: Annotated[
        str, typer.Argument(help="The pipeline_run_id of a failed run to re-run.")
    ],
    from_stage: Annotated[
        str | None,
        typer.Option(
            "--from-stage",
            help=(
                "Explicitly confirm the stage to re-run from; must be the "
                "stage the run failed at."
            ),
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Preview eligibility only; change no state.",
        ),
    ] = False,
    as_json: Annotated[
        bool,
        typer.Option("--json", help="Emit deterministic machine-readable JSON."),
    ] = False,
) -> None:
    """Re-run a failed pipeline run, if it is provably safe to do so.

    This is an explicit operator mutation. It checks that the run exists, is
    failed because of a genuine stage failure (not an operator approval-gate
    rejection), and carries an APPROVED Trust Envelope; if so, it resets the
    run's status to the resumable state and records an audit event. It then
    tells you to run `storytime run --resume RUN_ID` to re-execute the run.
    With --dry-run it only previews the decision and changes nothing. An
    ineligible run is rejected with a clear reason and exits non-zero.
    """
    config = load_config()
    with StateStore.open(config.state_db_path) as store:
        result = perform_rerun(
            store,
            SystemClock(),
            pipeline_run_id,
            requested_from_stage=from_stage,
            dry_run=dry_run,
        )

    if as_json:
        typer.echo(render_rerun_json(result))
    else:
        typer.echo(render_rerun_text(result))
    if not result.decision.eligible:
        raise typer.Exit(code=1)


@app.command()
def serve(
    port: Annotated[
        int | None,
        typer.Option(
            "--port", "-p",
            help="Port to bind on loopback. Defaults to the configured HTTP port.",
        ),
    ] = None,
) -> None:
    """Serve the feed directory over a local, range-capable HTTP server.

    Binds 127.0.0.1 only (Architecture Baseline section 15): the feed is for
    the local operator, never the network. The server honours HTTP byte-range
    requests, so a podcast client can stream and seek within episode audio.
    Press Ctrl+C to stop.
    """
    config = load_config()
    bind_port = port if port is not None else config.http_port

    try:
        server = LocalFeedServer(
            host=config.http_host, port=bind_port, directory=config.feed_dir
        )
    except UnsafeBindError as exc:
        typer.echo(f"ERROR: {exc}")
        raise typer.Exit(code=1) from exc

    if not config.feed_dir.exists():
        typer.echo(
            f"note: feed directory {config.feed_dir} does not exist yet — "
            "run the pipeline through 'publish' first; requests will 404 until then."
        )
    typer.echo(
        f"serving {config.feed_dir} at "
        f"http://{server.bind_host}:{bind_port}/feed.xml"
    )
    typer.echo("press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:  # pragma: no cover - interactive stop
        typer.echo("\nstopped.")


_LOCAL_LIVE_DEFAULT_PORT = 8770


@app.command(name="local-live")
def local_live_cmd(
    host: Annotated[
        str,
        typer.Option("--host", help="Loopback host to bind. Defaults to 127.0.0.1."),
    ] = "127.0.0.1",
    port: Annotated[
        int | None,
        typer.Option(
            "--port", "-p",
            help="Loopback port. Defaults to STORYTIME_LOCAL_LIVE_PORT or 8770.",
        ),
    ] = None,
) -> None:
    """Serve the local-live proof-loop API over a loopback-only HTTP service.

    Phase 14A.1. Exposes backend-owned durable SQLite state (runs, stages,
    artifacts, events) read-only to the operator console's Live Proof Loop
    surface, plus one controlled POST /api/proof-runs action that runs an
    approved, deterministic, local-safe proof fixture and persists it durably.

    Binds 127.0.0.1 only and enforces a strict loopback + Vite-dev origin
    allowlist (no wildcard CORS). It starts no provider, no ffmpeg, and no
    network egress. Press Ctrl+C to stop.
    """
    config = load_config()
    env_port = os.environ.get("STORYTIME_LOCAL_LIVE_PORT", "").strip()
    if port is not None:
        bind_port = port
    elif env_port:
        try:
            bind_port = int(env_port)
        except ValueError:
            typer.echo(f"ERROR: STORYTIME_LOCAL_LIVE_PORT must be an integer, got {env_port!r}")
            raise typer.Exit(code=1) from None
    else:
        bind_port = _LOCAL_LIVE_DEFAULT_PORT

    try:
        bind_host = validate_bind_host(host)
    except UnsafeBindError as exc:
        typer.echo(f"ERROR: {exc}")
        raise typer.Exit(code=1) from exc

    # Ensure the runs directory and the SQLite schema exist before serving, so
    # the first request (and the first proof run) find a migrated durable store.
    config.runs_dir.mkdir(parents=True, exist_ok=True)
    with StateStore.open(config.state_db_path):
        pass

    typer.echo(
        f"local-live API on http://{bind_host}:{bind_port} "
        f"(state: {config.state_db_path}, loopback-only)"
    )
    typer.echo(
        "routes: GET /health, GET /api/runs, GET /api/runs/{id}, "
        ".../artifacts, .../events, POST /api/proof-runs"
    )
    typer.echo("press Ctrl+C to stop.")
    try:
        serve_local_live(
            db_path=config.state_db_path,
            runs_dir=config.runs_dir,
            fixtures_dir=default_fixtures_dir(),
            host=bind_host,
            port=bind_port,
        )
    except KeyboardInterrupt:  # pragma: no cover - interactive stop
        typer.echo("\nstopped.")


# --------------------------------------------------------------------------
# Phase 10B: the `report` command group — generate the static operator report.
#
# `storytime report generate` writes a static, local, read-only HTML operator
# report under the locked Architecture Baseline Section 25. It starts no
# server, adds no dependency, and changes no state — it reads the SQLite state
# database and the on-disk artifacts (which remain the source of truth) and
# writes inert HTML/CSS files a local operator can open directly in a browser.
# --------------------------------------------------------------------------
report_app = typer.Typer(
    name="report",
    help="Generate the static, local, read-only operator report.",
    no_args_is_help=True,
    add_completion=False,
)
app.add_typer(report_app)


@report_app.command("generate")
def report_generate(
    output: Annotated[
        Path,
        typer.Option(
            "--output", "-o",
            help="Directory to write the static report into.",
        ),
    ] = Path("operator-report"),
) -> None:
    """Generate the static local HTML operator report.

    Reads the local SQLite state database and on-disk artifacts and writes a
    self-contained, air-gapped HTML report (``index.html``, ``runs.html``, one
    ``run-<run_id>.html`` per run, and a local ``style.css``) into the output
    directory. The report is read-only: it renders past runs and governance
    decisions and contains no control that changes state. It needs no web
    server — open ``index.html`` directly in a browser.
    """
    config = load_config()
    storage = LocalFilesystemStorage(config.runs_dir)

    # Observability links are optional references only (§25.14): a Jaeger
    # trace link is emitted only when STORYTIME_JAEGER_BASE_URL is configured
    # AND a run has a recorded trace id. With nothing configured the report is
    # still complete. No observability backend is ever queried.
    observability: dict[str, str] = {}
    jaeger_base = os.environ.get("STORYTIME_JAEGER_BASE_URL", "").strip()
    if jaeger_base:
        observability["jaeger_trace_base_url"] = jaeger_base

    generated_at = to_iso(SystemClock().now())
    with StateStore.open(config.state_db_path) as store:
        result = generate_report(
            store,
            storage,
            output,
            generated_at=generated_at,
            feed_reference="feed.xml",
            observability=observability,
        )

    typer.echo(
        f"generated operator report for {result.run_count} run(s): "
        f"{len(result.files)} file(s) under {result.output_dir}"
    )
    typer.echo(f"open {result.index_path} in a browser (no server required).")


@app.command(name="export-demo-ui")
def export_demo_ui(
    output: Annotated[
        Path,
        typer.Option(
            "--output", "-o",
            help="Path to write the static demo UI export JSON into.",
        ),
    ] = Path(DEFAULT_EXPORT_RELPATH),
) -> None:
    """Write the deterministic, read-only static demo export for the frontend.

    Produces the backend-defined static data export the Phase 13 frontend
    (the portfolio website and operator GUI shell) consumes. The export is
    built entirely from fixed demo data — fixed ids, fixed timestamps, fixed
    ordering — so it is deterministic: running this command twice writes
    byte-identical JSON. It is read-only: it performs no pipeline action, no
    mutation, and no network call, and it queries no live backend state. The
    output carries a top-level ``schemaVersion``. See
    ``docs/frontend-static-export-contract.md``.
    """
    target = output.resolve()
    if not target.parent.is_dir():
        typer.echo(f"output directory does not exist: {target.parent}")
        raise typer.Exit(code=1)
    write_static_demo_export(target)
    typer.echo(f"wrote deterministic static demo export to {target}")


@app.command(name="tts-proof")
def tts_proof(
    fixture_id: Annotated[
        str,
        typer.Option(
            "--fixture-id",
            help="Allowlisted approved fixture id to synthesize.",
        ),
    ] = DEFAULT_FIXTURE_ID,
) -> None:
    """Run the Phase 13I governed local TTS proof on an approved fixture.

    Backend/CLI-only. Reads ``STORYTIME_TTS_*`` config from the environment,
    drives the approved fixture through the governance/cost guard and the
    deterministic mock provider, writes an atomic audio artifact, a manifest,
    and an audit log under the controlled artifact directory (default under
    ``runs/``, which is git- and archive-excluded), and prints an
    observability-safe summary — never the raw fixture text. No network and no
    credentials are required; a non-mock provider fails closed unless explicitly
    enabled, and no real adapter is bundled in this phase.

    This command adds no local bridge action and triggers no browser behaviour.
    """
    config = load_tts_proof_config()
    result = run_tts_proof(config, fixture_id=fixture_id, clock=SystemClock())
    if result.ok:
        typer.echo(
            f"tts proof OK — provider={result.provider} "
            f"mode={result.provider_mode} run={result.proof_run_id} "
            f"chars={result.character_count} bytes={result.output_bytes} "
            f"audio_sha256={result.audio_sha256}"
        )
        typer.echo(f"artifact: {result.artifact_path}")
        typer.echo(f"manifest: {result.manifest_path}")
        return
    typer.echo(
        f"tts proof REJECTED — reason={result.failure_reason} "
        f"provider={result.provider} mode={result.provider_mode}: {result.message}"
    )
    raise typer.Exit(code=1)


def main() -> None:
    """Console-script entry point (see [project.scripts] in pyproject.toml)."""
    app()
