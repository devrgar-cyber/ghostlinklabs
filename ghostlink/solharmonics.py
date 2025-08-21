"""Utilities for routing GhostLink utterances to Sol Harmonics packs and
handling the return payload."""
from __future__ import annotations

from typing import Dict, List
from urllib.parse import quote

# Mapping of keywords to Sol Harmonics pack identifiers
PACK_KEYWORDS: Dict[str, List[str]] = {
    "DOWNSHIFT": ["sleep", "tired", "2am", "insomnia"],
    "ATTENTION_RESET": ["focus", "scroll", "can't think"],
    "NERVE_QUIET": ["anxious", "panic", "overwhelm"],
    "IGNITION": ["stuck", "procrastinate", "can't start"],
    "DECOMPRESSION": ["angry", "resentment", "conflict"],
    "GROUND": ["money", "spend", "stress bills"],
}

# Moves corresponding to each pack
MOVES: Dict[str, str] = {
    "DOWNSHIFT": "kill screens for 30 minutes. dark room. breathe 4-7-8 x 8.",
    "ATTENTION_RESET": "set a 15-minute timer. one task. no tabs. start now.",
    "NERVE_QUIET": "feet on floor. inhale 4, hold 4, exhale 8, x10. then text one sentence of truth.",
    "IGNITION": "ship the ugly first version to one person before midnight.",
    "DECOMPRESSION": "write the unsent message in notes. do not send.",
    "GROUND": "cancel one non-essential charge today. screenshot = done.",
    "ILLUMINATOR": "name the price you'll pay in the next 20 minutes. then pay it.",
}

MIRRORS: List[str] = [
    "scan: repetition > intent. you named it three times. that's rehearsal, not change.",
    "scan: contradiction. you want the result while dodging the price.",
    "scan: avoidance. a question isn't a choice. name the choice.",
    "scan: clarity. your ask is buried in filler. say it in ten words.",
    "scan: leverage. one hinge moves this: {hinge}. do that first.",
]

CONSEQUENCE = "if you skip this, the loop resets and costs you tomorrow, too."
CHECKPOINT = {
    "prompt": "did you do it?",
    "yes": "done. raise the bar next.",
    "no": "not yet. tomorrow we shrink the slice.",
}


def route_pack(utterance: str) -> str:
    """Return the pack identifier for the given utterance."""
    text = utterance.lower()
    for pack, keywords in PACK_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return pack
    return "ILLUMINATOR"


def build_deeplink(pack: str, summary: str) -> str:
    note = quote(summary)
    return f"solharmonics://run?pack={pack}&mode=diagnostic&note={note}"


def build_web_fallback(pack: str) -> str:
    return f"https://www.quantisophy.com/sol-harmonics?pack={pack}"


def summarize(utterance: str, limit: int = 20) -> str:
    words = utterance.split()
    return " ".join(words[:limit])


def choose_mirror(utterance: str) -> str:
    # Deterministic choice based on hash of utterance
    idx = hash(utterance) % len(MIRRORS)
    return MIRRORS[idx]


def return_payload(pack: str, utterance: str = "", hinge: str | None = None) -> Dict[str, str]:
    mirror = choose_mirror(utterance)
    if "{hinge}" in mirror:
        mirror = mirror.format(hinge=hinge or "")
    move = MOVES.get(pack, MOVES["ILLUMINATOR"])
    payload = {
        "mirror": mirror,
        "move": move,
        "consequence": CONSEQUENCE,
        "checkpoint_prompt": CHECKPOINT["prompt"],
        "checkpoint_yes": CHECKPOINT["yes"],
        "checkpoint_no": CHECKPOINT["no"],
    }
    return payload
