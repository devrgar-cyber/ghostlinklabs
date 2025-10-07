"""ANOMALY_ENGINE component module."""
from __future__ import annotations

from ..blueprint import component_factory


ANOMALY_ENGINE = component_factory("ANOMALY_ENGINE", "session", module=__name__)
