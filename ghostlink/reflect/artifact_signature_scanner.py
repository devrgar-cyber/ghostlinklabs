"""Factory for the ARTIFACT_SIGNATURE_SCANNER component."""
from __future__ import annotations

from ..factory import component_factory

ARTIFACT_SIGNATURE_SCANNER = component_factory(__name__, "ARTIFACT_SIGNATURE_SCANNER", "reflect")

__all__ = ["ARTIFACT_SIGNATURE_SCANNER"]
