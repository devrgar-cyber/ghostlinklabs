# ghostlink/tools/gpio_read.py
from __future__ import annotations
from ..runtime.context import Context
from ..runtime.policy import SovereigntyGate

def main(ctx: Context, pin: int, chip: str | None = None):
    SovereigntyGate.require(ctx, "gpio")
    try:
        import gpiod  # type: ignore
        chip = chip or "/dev/gpiochip0"
        c = gpiod.Chip(chip)
        line = c.get_line(pin)
        line.request(consumer="ghostlink", type=gpiod.LINE_REQ_DIR_IN)
        val = line.get_value()
        line.release(); c.close()
        return {"chip": chip, "pin": pin, "value": int(val)}
    except Exception as e:
        return {"error": "libgpiod not available", "detail": str(e), "pin": pin}
