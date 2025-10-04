"""SUMMARY_REPORT component module."""
from __future__ import annotations

from ..blueprint import create_component


def SUMMARY_REPORT() -> dict[str, object]:
    """Return the SUMMARY_REPORT component description."""
    return create_component(
        "SUMMARY_REPORT",
        "session",
    )
