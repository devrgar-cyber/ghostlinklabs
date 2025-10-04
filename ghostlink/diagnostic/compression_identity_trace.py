"""Factory for the COMPRESSION_IDENTITY_TRACE component."""
from __future__ import annotations

from ..factory import component_factory

COMPRESSION_IDENTITY_TRACE = component_factory(__name__, "COMPRESSION_IDENTITY_TRACE", "diagnostic")

__all__ = ["COMPRESSION_IDENTITY_TRACE"]
