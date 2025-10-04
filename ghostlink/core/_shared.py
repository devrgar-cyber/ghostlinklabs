"""Shared utilities for GhostLink core tooling."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ToolResponse:
    """Canonical response envelope returned by GhostLink tooling.

    The bootstrap process and higher-level orchestration layers rely on a
    predictable payload structure so that symbolic tools can be combined
    without tightly coupling their implementations.  Each tool returns its
    identity, the signal that was processed, and optional diagnostic notes.
    """

    name: str
    context: Dict[str, Any] = field(default_factory=dict)
    status: str = "ready"
    notes: Optional[str] = None


def build_response(name: str, *, context: Optional[Dict[str, Any]] = None,
                   status: str = "ready", notes: Optional[str] = None) -> ToolResponse:
    """Construct a :class:`ToolResponse` for a symbolic tool invocation."""
    return ToolResponse(name=name, context=context or {}, status=status, notes=notes)
