"""Factory for the FALSE_PASS_FILTER component."""
from __future__ import annotations

from ..factory import component_factory

FALSE_PASS_FILTER = component_factory(__name__, "FALSE_PASS_FILTER", "diagnostic")

__all__ = ["FALSE_PASS_FILTER"]
