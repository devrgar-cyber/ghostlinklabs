"""OPERATOR_SIGNATURE_GATE component module."""
from __future__ import annotations

from ..blueprint import create_component


def OPERATOR_SIGNATURE_GATE() -> dict[str, object]:
    """Return the OPERATOR_SIGNATURE_GATE component description."""
    return create_component(
        "OPERATOR_SIGNATURE_GATE",
        "access",
    )
