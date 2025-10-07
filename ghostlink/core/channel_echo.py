"""CHANNEL_ECHO component module."""
from __future__ import annotations

from ..blueprint import component_factory


CHANNEL_ECHO = component_factory("CHANNEL_ECHO", "core", module=__name__)
