"""ANOMALY_ENGINE component module."""
from __future__ import annotations

from ..blueprint import create_component


def ANOMALY_ENGINE() -> dict[str, object]:
    """Return the ANOMALY_ENGINE component description."""
    return create_component(
        "ANOMALY_ENGINE",
        "session",
    )
