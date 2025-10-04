# ghostlink/tools/obd_read.py
from __future__ import annotations
from ..runtime.context import Context
from ..runtime.policy import SovereigntyGate

# ELM327/OBDLink via python-OBD (optional)

def main(ctx: Context, pid: str = "SPEED", port: str | None = None):
    SovereigntyGate.require(ctx, "serial")
    try:
        import obd  # type: ignore
    except Exception as e:
        return {"error": "python-OBD not installed", "detail": str(e)}
    conn = obd.OBD(port)  # auto-connect if None
    cmd = getattr(obd.commands, pid, None)
    if not cmd:
        return {"error": "unknown PID", "pid": pid}
    r = conn.query(cmd)
    return {"pid": pid, "value": str(r.value), "status": r.status()}
