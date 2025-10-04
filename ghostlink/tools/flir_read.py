# ghostlink/tools/flir_read.py
from __future__ import annotations
from ..runtime.context import Context
from ..runtime.policy import SovereigntyGate

def main(ctx: Context):
    SovereigntyGate.require(ctx, "gpio")
    return {"error": "FLIR Lepton driver not implemented in this bundle"}
