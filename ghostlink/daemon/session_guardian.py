"""SESSION_GUARDIAN component module."""
from __future__ import annotations

from ..blueprint import component_factory


SESSION_GUARDIAN = component_factory("SESSION_GUARDIAN", "daemon", module=__name__)
