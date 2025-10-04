# scripts/attest_stub.py
from __future__ import annotations
from pathlib import Path
import json, time, hashlib

ROOT = Path(__file__).resolve().parents[1]
manifest = (ROOT/"vault"/"manifest.json").read_text() if (ROOT/"vault"/"manifest.json").exists() else "{}"
att = {
  "issuer": "ghostlink-local",
  "ts": time.time(),
  "manifest_sha256": hashlib.sha256(manifest.encode()).hexdigest()
}
print(json.dumps(att, indent=2))
