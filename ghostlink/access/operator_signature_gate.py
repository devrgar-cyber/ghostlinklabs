"""Factory for the OPERATOR_SIGNATURE_GATE component."""
from __future__ import annotations

from ..factory import component_factory

OPERATOR_SIGNATURE_GATE = component_factory(__name__, "OPERATOR_SIGNATURE_GATE", "access")

__all__ = ["OPERATOR_SIGNATURE_GATE"]
