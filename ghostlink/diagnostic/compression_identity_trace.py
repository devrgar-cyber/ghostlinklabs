"""COMPRESSION_IDENTITY_TRACE component module."""
from __future__ import annotations

from ..blueprint import create_component


def COMPRESSION_IDENTITY_TRACE() -> dict[str, object]:
    """Return the COMPRESSION_IDENTITY_TRACE component description."""
    return create_component(
        "COMPRESSION_IDENTITY_TRACE",
        "diagnostic",
    )
