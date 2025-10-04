"""Factory for the FAILURE_TO_FAIL_PROMPT component."""
from __future__ import annotations

from ..factory import component_factory

FAILURE_TO_FAIL_PROMPT = component_factory(__name__, "FAILURE_TO_FAIL_PROMPT", "meta")

__all__ = ["FAILURE_TO_FAIL_PROMPT"]
