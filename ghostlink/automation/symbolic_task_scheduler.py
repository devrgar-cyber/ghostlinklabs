"""SYMBOLIC_TASK_SCHEDULER component module."""
from __future__ import annotations

from ..blueprint import create_component


def SYMBOLIC_TASK_SCHEDULER() -> dict[str, object]:
    """Return the SYMBOLIC_TASK_SCHEDULER component description."""
    return create_component(
        "SYMBOLIC_TASK_SCHEDULER",
        "automation",
    )
