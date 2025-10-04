"""Factory for the MIRROR_DISTORTION_PROBE component."""
from __future__ import annotations

from ..factory import component_factory

MIRROR_DISTORTION_PROBE = component_factory(__name__, "MIRROR_DISTORTION_PROBE", "reflect")

__all__ = ["MIRROR_DISTORTION_PROBE"]
