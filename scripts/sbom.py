# scripts/sbom.py
from __future__ import annotations
from pathlib import Path
import json, hashlib

ROOT = Path(__file__).resolve().parents[1]
FILES = [p for p in ROOT.rglob("*.py") if "/venv/" not in str(p)]

comps = []
for p in FILES:
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    comps.append({"name": p.as_posix(), "hashes": [{"alg":"SHA-256","content": h}]})

sbom = {"bomFormat":"CycloneDX","specVersion":"1.5","components": comps}
print(json.dumps(sbom, indent=2))
