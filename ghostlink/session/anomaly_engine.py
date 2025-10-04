"""Factory for the ANOMALY_ENGINE component."""
from __future__ import annotations

from ..factory import component_factory

ANOMALY_ENGINE = component_factory(__name__, "ANOMALY_ENGINE", "session")

__all__ = ["ANOMALY_ENGINE"]
