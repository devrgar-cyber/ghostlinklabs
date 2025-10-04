"""SESSION_TRACKER component module."""
from __future__ import annotations

from ..blueprint import component_factory


SESSION_TRACKER = component_factory("SESSION_TRACKER", "session", module=__name__)
