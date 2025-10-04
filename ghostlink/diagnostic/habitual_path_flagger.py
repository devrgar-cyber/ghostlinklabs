"""Factory for the HABITUAL_PATH_FLAGGER component."""
from __future__ import annotations

from ..factory import component_factory

HABITUAL_PATH_FLAGGER = component_factory(__name__, "HABITUAL_PATH_FLAGGER", "diagnostic")

__all__ = ["HABITUAL_PATH_FLAGGER"]
