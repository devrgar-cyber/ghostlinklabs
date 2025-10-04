"""DISCONNECT_SIGNATURE_DETECTOR component module."""
from __future__ import annotations

from ..blueprint import create_component


def DISCONNECT_SIGNATURE_DETECTOR() -> dict[str, object]:
    """Return the DISCONNECT_SIGNATURE_DETECTOR component description."""
    return create_component(
        "DISCONNECT_SIGNATURE_DETECTOR",
        "diagnostic",
    )
