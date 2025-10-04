"""Factory for the MIRROR_SHEAR component."""
from __future__ import annotations

from ..factory import component_factory

MIRROR_SHEAR = component_factory(__name__, "MIRROR_SHEAR", "core")

__all__ = ["MIRROR_SHEAR"]
