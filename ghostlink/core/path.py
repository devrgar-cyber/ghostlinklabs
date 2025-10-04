"""Factory for the PATH component."""
from __future__ import annotations

from ..factory import component_factory

PATH = component_factory(__name__, "PATH", "core")

__all__ = ["PATH"]
