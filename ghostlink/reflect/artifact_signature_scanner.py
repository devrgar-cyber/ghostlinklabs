"""ARTIFACT_SIGNATURE_SCANNER component module."""
from __future__ import annotations

from ..blueprint import component_factory


ARTIFACT_SIGNATURE_SCANNER = component_factory("ARTIFACT_SIGNATURE_SCANNER", "reflect", module=__name__)
