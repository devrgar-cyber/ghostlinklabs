# ghostlink/tools/cleanse_pii.py
from __future__ import annotations
import re
from ..runtime.context import Context

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"\b(?:\+?\d[ -.]*)?(?:\(\d{3}\)|\d{3})[ -.]?\d{3}[ -.]?\d{4}\b")
VIN = re.compile(r"\b[ABCDEFGHJKLMNPRSTUVWXYZ0-9]{17}\b")

_DEF = [(EMAIL, "<email>"),(PHONE, "<phone>"),(VIN, "<vin>")]

def main(ctx: Context, text: str):
    red = text
    for rx, repl in _DEF:
        red = rx.sub(repl, red)
    return {"redacted": red}
