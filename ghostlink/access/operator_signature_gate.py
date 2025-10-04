"""Operator signature validation."""
from __future__ import annotations

from typing import Dict

from ghostlink.core import ToolResponse
from ghostlink.core._shared import build_response


def OPERATOR_SIGNATURE_GATE(signature: Dict[str, str] | None = None) -> ToolResponse:
    """Validate operator sovereignty prior to tool execution."""
    context = {"signature": signature or {}, "validated": bool(signature)}
    status = "granted" if context["validated"] else "rejected"
    return build_response("OPERATOR_SIGNATURE_GATE", context=context, status=status)
