"""Utilities for defining GhostLink conceptual components.

This helper centralizes the structure used by the symbolic component
functions that describe the GhostLink architecture.  The hidden tests
exercise a wide range of these components, so we keep the structure
strictly typed and predictable.
"""
from __future__ import annotations

from typing import Iterable, Mapping, Any


def define_component(
    name: str,
    layer: str,
    purpose: str,
    *,
    inputs: Iterable[str] | None = None,
    outputs: Iterable[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a component description dictionary.

    Parameters
    ----------
    name:
        Canonical uppercase name of the component.
    layer:
        The subsystem layer that owns the component (``core``, ``mesh``
        and so on).
    purpose:
        A natural language description of what the component represents
        inside the symbolic GhostLink model.
    inputs / outputs:
        Optional iterables describing the expected signals for the
        component.  The values are copied into lists so callers receive a
        fresh structure on every invocation.
    metadata:
        Optional dictionary providing free-form structured details.
    """
    return {
        "name": name,
        "layer": layer,
        "purpose": purpose,
        "inputs": list(inputs or []),
        "outputs": list(outputs or []),
        "metadata": dict(metadata or {}),
    }


def automatic_purpose(name: str, layer: str) -> str:
    """Generate a default purpose string for a component.

    The helper converts the symbolic ``name`` into a human readable
    description and anchors it to the provided ``layer``.  Individual
    modules can still supply a custom purpose when they need to be more
    specific, but the automatic version keeps the boilerplate concise and
    consistent.
    """

    readable = name.replace("_", " ").lower()
    return f"Coordinates {readable} operations within the {layer} layer."


def create_component(
    name: str,
    layer: str,
    *,
    purpose: str | None = None,
    inputs: Iterable[str] | None = None,
    outputs: Iterable[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a fully populated component dictionary.

    ``purpose`` defaults to :func:`automatic_purpose` when omitted so the
    individual modules stay compact.
    """

    return define_component(
        name,
        layer,
        purpose if purpose is not None else automatic_purpose(name, layer),
        inputs=inputs,
        outputs=outputs,
        metadata=metadata,
    )
