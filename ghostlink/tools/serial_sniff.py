# ghostlink/tools/serial_sniff.py
from __future__ import annotations
from ..runtime.context import Context
from ..runtime.policy import SovereigntyGate


def main(ctx: Context, port: str, baud: int = 115200, seconds: int = 3):
    SovereigntyGate.require(ctx, "serial")
    try:
        import serial  # type: ignore
    except Exception as e:
        return {"error": "pyserial not installed", "detail": str(e)}
    ser = serial.Serial(port, baud, timeout=1)
    data = ser.read(max(1, seconds) * baud // 10)
    ser.close()
    return {"port": port, "bytes": len(data), "preview": data[:64].hex()}
