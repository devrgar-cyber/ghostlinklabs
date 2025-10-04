"""FRACTURE_MIRROR_PROMPT component module."""
from __future__ import annotations

from ..blueprint import create_component


def FRACTURE_MIRROR_PROMPT() -> dict[str, object]:
    """Return the FRACTURE_MIRROR_PROMPT component description."""
    return create_component(
        "FRACTURE_MIRROR_PROMPT",
        "meta",
    )
