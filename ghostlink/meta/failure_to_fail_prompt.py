"""FAILURE_TO_FAIL_PROMPT component module."""
from __future__ import annotations

from ..blueprint import create_component


def FAILURE_TO_FAIL_PROMPT() -> dict[str, object]:
    """Return the FAILURE_TO_FAIL_PROMPT component description."""
    return create_component(
        "FAILURE_TO_FAIL_PROMPT",
        "meta",
    )
