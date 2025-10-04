"""MIRROR_DISTORTION_PROBE component module."""
from __future__ import annotations

from ..blueprint import create_component


def MIRROR_DISTORTION_PROBE() -> dict[str, object]:
    """Return the MIRROR_DISTORTION_PROBE component description."""
    return create_component(
        "MIRROR_DISTORTION_PROBE",
        "reflect",
    )
