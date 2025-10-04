"""Factory for the BIOLOGICAL_TRACE_INTEGRATOR component."""
from __future__ import annotations

from ..factory import component_factory

BIOLOGICAL_TRACE_INTEGRATOR = component_factory(__name__, "BIOLOGICAL_TRACE_INTEGRATOR", "bio")

__all__ = ["BIOLOGICAL_TRACE_INTEGRATOR"]
