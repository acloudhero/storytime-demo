"""Phase 13E data-integrity assertions for the Action Preview adapter.

Phase 13E adds a static, demo-mode Action Preview system implemented in
``frontend/src/data/actionPreviewAdapter.ts``. Each preview names a
target object — a pipeline run id, a stage id, or a visibly-disabled
future-action id — that must exist in the committed Phase 13C static
export (``frontend/src/data/storytime-demo-export.json``). If those ids
ever drift, the previews start pointing at runs and stages the GUI
cannot otherwise show, the data-source guarantee fails silently, and a
reviewer following the operator-intent narrative would see references
to objects that don't exist in the export they're looking at.

This test enforces the integrity. It opens both files (the export as
JSON, the adapter as text), extracts every ``run-YYYY-MMDD-<slug>``
identifier the adapter mentions, and asserts:

1. At a minimum, the two well-known stable run ids — ``run-2026-0518-golden``
   (the golden-path run) and ``run-2026-0520-review`` (the
   needs-review run) — appear in both the adapter and the export.
2. Every ``run-...`` token the adapter mentions corresponds to a run id
   that exists in the export (under ``runs[].id``).
3. Every ``run-...:<stage>`` stage / disabled-action id the adapter
   mentions corresponds to a real stage id or disabled-action id in the
   export.

This is a Phase 13E-style integrity check: no new test framework
dependency, no runtime JS execution, no parsing of the TypeScript AST.
The adapter source is treated as text on purpose — it's the
*concrete reference* a reviewer sees, and ensuring those concrete
references are real is precisely what's at stake. The strategy mirrors
``test_failure_mode_regression`` in that it reads committed files
directly and asserts contiguous-token presence.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_EXPORT_PATH = (
    _REPO_ROOT / "frontend" / "src" / "data" / "storytime-demo-export.json"
)
_ADAPTER_PATH = (
    _REPO_ROOT / "frontend" / "src" / "data" / "actionPreviewAdapter.ts"
)

# Well-known stable run ids the adapter is expected to reference.
_EXPECTED_RUN_IDS: tuple[str, ...] = (
    "run-2026-0518-golden",
    "run-2026-0520-review",
)

# Token pattern. Matches:
#   run-YYYY-MMDD-<lowercase-slug>            (e.g. run-2026-0520-review)
#   run-YYYY-MMDD-<lowercase-slug>:<segment>  (e.g. run-2026-0520-review:retry)
# Where <segment> is a lowercase ``-``/``_`` segment such as
# ``governance-gate``, ``open-review``, or ``retry``.
_RUN_TOKEN_RE = re.compile(
    r"\brun-(?:\d{4})-(?:\d{4})-[a-z][a-z0-9-]*"
    r"(?::[a-z][a-z0-9_-]*)?"
)


def _load_export() -> dict[str, object]:
    """Load the committed static export as a dict."""
    with _EXPORT_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict), (
        f"{_EXPORT_PATH.name} did not deserialize to a JSON object"
    )
    return data


def _adapter_source() -> str:
    """Read the action-preview adapter source as text."""
    return _ADAPTER_PATH.read_text(encoding="utf-8")


def _extract_export_run_ids(export: dict[str, object]) -> set[str]:
    """Return the set of stable run ids declared by the export."""
    runs = export.get("runs", [])
    assert isinstance(runs, list), "export.runs is not a list"
    ids: set[str] = set()
    for run in runs:
        assert isinstance(run, dict), "export.runs[*] is not an object"
        run_id = run.get("id")
        assert isinstance(run_id, str), "export.runs[*].id is not a string"
        ids.add(run_id)
    return ids


def _extract_export_stage_and_action_ids(export: dict[str, object]) -> set[str]:
    """Return every nested id of the form ``<runId>:<segment>``.

    This includes stage ids (``stages[].id``) and disabled-action ids
    (``disabledActions[].id``).
    """
    runs = export.get("runs", [])
    assert isinstance(runs, list)
    ids: set[str] = set()
    for run in runs:
        assert isinstance(run, dict)
        for stage in run.get("stages", []) or []:
            assert isinstance(stage, dict)
            stage_id = stage.get("id")
            if isinstance(stage_id, str):
                ids.add(stage_id)
        for action in run.get("disabledActions", []) or []:
            assert isinstance(action, dict)
            action_id = action.get("id")
            if isinstance(action_id, str):
                ids.add(action_id)
    return ids


def _extract_adapter_tokens(source: str) -> set[str]:
    """Return every ``run-...`` token the adapter mentions."""
    return set(_RUN_TOKEN_RE.findall(source))


def test_adapter_source_is_readable() -> None:
    """Sanity: the adapter source file exists and isn't empty."""
    src = _adapter_source()
    assert src.strip(), f"{_ADAPTER_PATH.name} is empty"


def test_export_source_is_readable() -> None:
    """Sanity: the static export deserializes."""
    export = _load_export()
    assert "runs" in export, "static export is missing 'runs'"


@pytest.mark.parametrize("run_id", _EXPECTED_RUN_IDS)
def test_expected_run_id_present_in_export(run_id: str) -> None:
    """Every well-known run id is declared in the committed export."""
    export = _load_export()
    ids = _extract_export_run_ids(export)
    assert run_id in ids, (
        f"static export does not declare run {run_id!r}; the Action "
        f"Preview adapter cannot reference it safely"
    )


@pytest.mark.parametrize("run_id", _EXPECTED_RUN_IDS)
def test_expected_run_id_referenced_by_adapter(run_id: str) -> None:
    """Every well-known run id appears in the adapter source.

    This is the inverse direction: if the adapter ever drops the
    canonical stable ids, the previews stop being concrete and the
    test catches it.
    """
    src = _adapter_source()
    assert run_id in src, (
        f"{_ADAPTER_PATH.name} no longer references the canonical "
        f"stable run id {run_id!r}; preview targets would silently drift"
    )


def test_every_adapter_run_id_token_exists_in_export() -> None:
    """Every ``run-...`` token the adapter mentions resolves into the export.

    A token can be either a plain run id (``run-YYYY-MMDD-<slug>``) or a
    composite stage / disabled-action id (``<runId>:<segment>``). Each
    must exist in the export — plain run ids against ``runs[].id``,
    composite ids against ``stages[].id`` or ``disabledActions[].id``
    on the matching run.
    """
    export = _load_export()
    src = _adapter_source()

    export_run_ids = _extract_export_run_ids(export)
    export_composite_ids = _extract_export_stage_and_action_ids(export)
    adapter_tokens = _extract_adapter_tokens(src)

    assert adapter_tokens, (
        "actionPreviewAdapter.ts mentions no run-* tokens; either the "
        "adapter is no longer a real adapter or the token regex drifted"
    )

    missing: list[str] = []
    for token in adapter_tokens:
        if ":" in token:
            if token not in export_composite_ids:
                missing.append(token)
        else:
            if token not in export_run_ids:
                missing.append(token)

    assert not missing, (
        "actionPreviewAdapter.ts references run / stage / disabled-action "
        f"ids that do not exist in the committed static export: {sorted(missing)!r}"
    )


def test_review_run_disabled_actions_present_in_export() -> None:
    """The two review-run disabled-action ids the adapter targets exist.

    Phase 13E previews two future Local-mode actions on the
    review-required run: ``run-2026-0520-review:open-review`` (record
    a review decision) and ``run-2026-0520-review:retry`` (retry after
    review). Both correspond to visibly-disabled action ids the locked
    Phase 13C export declares on that run. If either disappears from
    the export, the preview's ``relatedDisabledActionId`` reference is
    pointing at nothing — catch it here.
    """
    export = _load_export()
    composite_ids = _extract_export_stage_and_action_ids(export)
    for action_id in (
        "run-2026-0520-review:open-review",
        "run-2026-0520-review:retry",
    ):
        assert action_id in composite_ids, (
            f"static export no longer declares disabled action {action_id!r}; "
            f"Phase 13E action-preview targets would drift"
        )


def test_review_run_governance_gate_stage_present_in_export() -> None:
    """The blocked Governance Gate stage targeted by the retry preview exists.

    The retry-failed-stage preview targets
    ``run-2026-0520-review:governance-gate`` — the blocked governance
    gate on the review-required run. If the export ever drops that
    stage, the preview is pointing at a stage that no longer exists.
    """
    export = _load_export()
    composite_ids = _extract_export_stage_and_action_ids(export)
    target = "run-2026-0520-review:governance-gate"
    assert target in composite_ids, (
        f"static export no longer declares stage {target!r}; the "
        f"Phase 13E retry-failed-stage preview target would drift"
    )
