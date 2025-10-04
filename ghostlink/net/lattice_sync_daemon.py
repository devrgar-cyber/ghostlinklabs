"""LATTICE_SYNC_DAEMON component module."""
from __future__ import annotations

from ..blueprint import component_factory


LATTICE_SYNC_DAEMON = component_factory("LATTICE_SYNC_DAEMON", "net", module=__name__)
