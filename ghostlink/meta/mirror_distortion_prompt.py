"""MIRROR_DISTORTION_PROMPT component module."""
from __future__ import annotations

from ..blueprint import create_component


def MIRROR_DISTORTION_PROMPT() -> dict[str, object]:
    """Return the MIRROR_DISTORTION_PROMPT component description."""
    return create_component(
        "MIRROR_DISTORTION_PROMPT",
        "meta",
    )
