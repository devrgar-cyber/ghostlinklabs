"""HABITUAL_PATH_FLAGGER component module."""
from __future__ import annotations

from ..blueprint import create_component


def HABITUAL_PATH_FLAGGER() -> dict[str, object]:
    """Return the HABITUAL_PATH_FLAGGER component description."""
    return create_component(
        "HABITUAL_PATH_FLAGGER",
        "diagnostic",
    )
