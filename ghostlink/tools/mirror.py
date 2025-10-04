# ghostlink/tools/mirror.py
from __future__ import annotations
import re
from ..runtime.context import Context

def main(ctx: Context, text: str):
    """MIRROR {text}: structured echo; surfaces patterns without suggestion."""
    tokens = re.findall(r"\w+", text, flags=re.UNICODE)
    lower = [t.lower() for t in tokens]
    freq = {}
    for t in lower: freq[t] = freq.get(t, 0) + 1
    repeats = sorted([t for t,c in freq.items() if c > 2])[:50]
    contradictions = []
    if "always" in lower and "never" in lower: contradictions.append("always↔never")
    if "true" in lower and "false" in lower:   contradictions.append("true↔false")
    if "yes" in lower and "no" in lower:       contradictions.append("yes↔no")
    return {
        "length": len(text),
        "tokens": len(tokens),
        "high_repeats": repeats,
        "contradiction_signals": contradictions
    }
