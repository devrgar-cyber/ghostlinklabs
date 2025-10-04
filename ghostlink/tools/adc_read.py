# ghostlink/tools/adc_read.py
from __future__ import annotations
from ..runtime.context import Context
from ..runtime.policy import SovereigntyGate

def main(ctx: Context, channel: int = 0, i2c_bus: int = 1, address: int = 0x48):
    SovereigntyGate.require(ctx, "gpio")
    try:
        import Adafruit_ADS1x15 as ADS  # type: ignore
    except Exception as e:
        return {"error": "ADS1x15 lib not installed", "detail": str(e)}
    adc = ADS.ADS1115(address=address, busnum=i2c_bus)
    value = adc.read_adc(channel, gain=1)
    return {"channel": channel, "raw": value}
