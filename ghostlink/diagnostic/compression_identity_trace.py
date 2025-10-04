"""COMPRESSION_IDENTITY_TRACE component module."""
from __future__ import annotations

from ..blueprint import component_factory


COMPRESSION_IDENTITY_TRACE = component_factory("COMPRESSION_IDENTITY_TRACE", "diagnostic", module=__name__)
