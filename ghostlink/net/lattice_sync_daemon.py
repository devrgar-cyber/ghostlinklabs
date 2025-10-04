"""Factory for the LATTICE_SYNC_DAEMON component."""
from __future__ import annotations

from ..factory import component_factory

LATTICE_SYNC_DAEMON = component_factory(__name__, "LATTICE_SYNC_DAEMON", "net")

__all__ = ["LATTICE_SYNC_DAEMON"]
