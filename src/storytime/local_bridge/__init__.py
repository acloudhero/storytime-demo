"""StoryTime local bridge (Phase 13G — runtime).

The first runtime implementation of the loopback-only local bridge whose
architecture, DTO contract, command-pattern router, queue-observability model,
and execution-timing policy were locked in Phase 13F. This phase is a minimal,
gated, safety-first bridge: loopback-only binding, strict origin policy,
allowlisted command-pattern routing, a single-concurrency observable in-memory
queue, and exactly one controlled real action (``retry_failed_stage``) that runs
only against an explicitly-configured (in tests, temporary) workspace.

It is NOT full Local mode, NOT Cloud/Distributed mode, has no frontend wiring,
no provider integrations, no persistent / external queue, and no browser durable
storage.
"""

from __future__ import annotations

from storytime.local_bridge.action_queue import (
    DEFAULT_CAPACITY,
    ActionQueue,
    Job,
    QueueFull,
)
from storytime.local_bridge.actions import (
    BridgeContext,
    WorkspaceMismatch,
    execute_retry_failed_stage,
    plan_route,
)
from storytime.local_bridge.dto import (
    ALLOWLISTED_ACTIONS,
    DEFERRED_ACTIONS,
    SCHEMA_VERSION,
    ValidatedRequest,
    ValidationError,
    validate_audit_shape,
    validate_request,
    validate_response_shape,
)
from storytime.local_bridge.responses import (
    build_accepted_response,
    build_audit_record,
    build_deduplicated_response,
    build_rejected_response,
    build_validated_response,
)
from storytime.local_bridge.server import (
    BRIDGE_VERSION,
    Bridge,
    LocalBridgeServer,
    default_allowed_origins,
)

__all__ = [
    "ALLOWLISTED_ACTIONS",
    "BRIDGE_VERSION",
    "Bridge",
    "BridgeContext",
    "DEFAULT_CAPACITY",
    "DEFERRED_ACTIONS",
    "ActionQueue",
    "Job",
    "LocalBridgeServer",
    "QueueFull",
    "SCHEMA_VERSION",
    "ValidatedRequest",
    "ValidationError",
    "WorkspaceMismatch",
    "build_accepted_response",
    "build_audit_record",
    "build_deduplicated_response",
    "build_rejected_response",
    "build_validated_response",
    "default_allowed_origins",
    "execute_retry_failed_stage",
    "plan_route",
    "validate_audit_shape",
    "validate_request",
    "validate_response_shape",
]
