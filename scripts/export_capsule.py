# scripts/export_capsule.py
from __future__ import annotations
from pathlib import Path
import json, zipfile

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT/"vault"

capsule = {
  "version": 1,
  "tools": [p.name for p in (ROOT/"ghostlink"/"tools").glob("*.py")],
  "macros": json.loads((VAULT/"macros.vault").read_text()) if (VAULT/"macros.vault").exists() else {}
}

out = ROOT/"capsule.zip"
with zipfile.ZipFile(out, "w") as z:
  z.writestr("capsule.json", json.dumps(capsule, indent=2, sort_keys=True))
print(f"wrote {out}")
