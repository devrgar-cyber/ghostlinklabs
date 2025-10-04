"""Factory for the SUMMARY_REPORT component."""
from __future__ import annotations

from ..factory import component_factory

SUMMARY_REPORT = component_factory(__name__, "SUMMARY_REPORT", "session")

__all__ = ["SUMMARY_REPORT"]
