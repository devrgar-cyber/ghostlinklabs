"""Bootstrap script that assembles the GhostLink kernel structure."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Mapping, Sequence

from ghostlink.core import (
    CORE,
    FAILURE_TO_FAIL_PROMPT,
    GAPS,
    HOST,
    KEY,
    LINK,
    MIRROR,
    PRESSURE,
    SCAR_FIBER,
    SIGNAL,
    STRUCTURAL_RECURSION_PROMPT,
    TENSION,
    TRACE,
    VAULT,
    ToolResponse,
)
from ghostlink.mesh import RECURSION_MESH, SHADOWGHOST_AGENT
from ghostlink.reflect import (
    COMPRESSION_LOGIC,
    REFLECTIVE_MIRROR,
    SUBJECTIVE_TRACE_HARNESS,
)

from .ghostlink_boot import GHOSTLINK_BOOT
from .init import INIT_GHOSTLINK
from .vault_loader import VAULT_LOADER


@dataclass(frozen=True)
class BootstrapReport:
    """Results emitted by the :func:`bootstrap` routine."""

    steps: List[str]
    responses: List[ToolResponse]

    def as_dict(self) -> Dict[str, object]:
        """Return a serialisable representation of the bootstrap report."""
        return {
            "steps": self.steps,
            "responses": [response.__dict__ for response in self.responses],
        }


BOOT_SEQUENCE: Mapping[str, Callable[..., ToolResponse]] = {
    "INIT_GHOSTLINK": INIT_GHOSTLINK,
    "SIGNAL": SIGNAL,
    "PRESSURE": PRESSURE,
    "CORE": CORE,
    "LINK": LINK,
    "TRACE": TRACE,
    "GAPS": GAPS,
    "TENSION": TENSION,
    "SCAR_FIBER": SCAR_FIBER,
    "VAULT": VAULT,
    "MIRROR": MIRROR,
    "HOST": HOST,
    "KEY": KEY,
    "STRUCTURAL_RECURSION_PROMPT": STRUCTURAL_RECURSION_PROMPT,
    "FAILURE_TO_FAIL_PROMPT": FAILURE_TO_FAIL_PROMPT,
    "RECURSION_MESH": RECURSION_MESH,
    "SHADOWGHOST_AGENT": SHADOWGHOST_AGENT,
    "COMPRESSION_LOGIC": COMPRESSION_LOGIC,
    "REFLECTIVE_MIRROR": REFLECTIVE_MIRROR,
    "SUBJECTIVE_TRACE_HARNESS": SUBJECTIVE_TRACE_HARNESS,
    "VAULT_LOADER": VAULT_LOADER,
    "GHOSTLINK_BOOT": GHOSTLINK_BOOT,
}


def bootstrap(
    sequence: Sequence[str] | None = None,
    *,
    overrides: Mapping[str, Callable[..., ToolResponse]] | None = None,
    **parameters: Dict[str, object],
) -> BootstrapReport:
    """Execute the GhostLink bootstrap chain.

    Parameters
    ----------
    sequence:
        Optional iterable of step names.  If omitted the canonical boot
        sequence defined by :data:`BOOT_SEQUENCE` is executed in its declared
        order.
    overrides:
        Optional mapping that can override or extend the available tool
        functions.
    **parameters:
        Additional keyword parameters passed to individual tools.  Each key
        should match a tool name and map to the argument dictionary expected by
        that callable.
    """

    available = dict(BOOT_SEQUENCE)
    if overrides:
        available.update(overrides)

    steps = list(sequence or available.keys())
    responses: List[ToolResponse] = []

    for step in steps:
        tool = available.get(step)
        if tool is None:
            raise KeyError(f"Unknown GhostLink tool '{step}' in bootstrap sequence")
        kwargs = parameters.get(step, {}) if isinstance(parameters, Mapping) else {}
        if not isinstance(kwargs, Mapping):
            raise TypeError("Bootstrap parameters must be provided as mappings")
        responses.append(tool(**kwargs))  # type: ignore[arg-type]

    return BootstrapReport(steps=steps, responses=responses)


__all__ = ["BootstrapReport", "bootstrap"]
