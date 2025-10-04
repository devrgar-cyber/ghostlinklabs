# ghostlink/tools/can_read.py
from __future__ import annotations
from ..runtime.context import Context
from ..runtime.policy import SovereigntyGate

# Requires SocketCAN (Linux). Uses python-can if available; else minimal.

def main(ctx: Context, iface: str = "can0", count: int = 10, timeout: float = 1.0):
    SovereigntyGate.require(ctx, "can")
    try:
        import can  # type: ignore
    except Exception as e:
        return {"error": "python-can not installed", "detail": str(e), "iface": iface}
    bus = can.interface.Bus(channel=iface, bustype="socketcan")
    msgs = []
    for _ in range(max(1, int(count))):
        m = bus.recv(timeout)
        if not m: break
        msgs.append({"ts": m.timestamp, "arbid": m.arbitration_id, "dlc": m.dlc, "data": m.data.hex()})
    return {"iface": iface, "frames": msgs, "count": len(msgs)}
