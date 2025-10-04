"""Factory for the RESIDUAL_COMPRESSION_MAP component."""
from __future__ import annotations

from ..factory import component_factory

RESIDUAL_COMPRESSION_MAP = component_factory(__name__, "RESIDUAL_COMPRESSION_MAP", "ghost")

__all__ = ["RESIDUAL_COMPRESSION_MAP"]
