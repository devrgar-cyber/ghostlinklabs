"""TEST_SIGNAL_INJECTION component module."""
from __future__ import annotations

from ..blueprint import component_factory


TEST_SIGNAL_INJECTION = component_factory("TEST_SIGNAL_INJECTION", "sandbox", module=__name__)
