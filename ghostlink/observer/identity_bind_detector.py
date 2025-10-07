"""IDENTITY_BIND_DETECTOR component module."""
from __future__ import annotations

from ..blueprint import component_factory


IDENTITY_BIND_DETECTOR = component_factory("IDENTITY_BIND_DETECTOR", "observer", module=__name__)
