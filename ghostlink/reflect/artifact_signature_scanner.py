"""ARTIFACT_SIGNATURE_SCANNER component module."""
from __future__ import annotations

from ..blueprint import create_component


def ARTIFACT_SIGNATURE_SCANNER() -> dict[str, object]:
    """Return the ARTIFACT_SIGNATURE_SCANNER component description."""
    return create_component(
        "ARTIFACT_SIGNATURE_SCANNER",
        "reflect",
    )
