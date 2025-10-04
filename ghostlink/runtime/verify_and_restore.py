# ghostlink/runtime/verify_and_restore.py
import json, hashlib
from pathlib import Path

def _h(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_manifest(manifest_path: Path):
    if not manifest_path.exists():
        raise RuntimeError("manifest.json missing")
    m = json.loads(manifest_path.read_text())
    base = manifest_path.parent.parent
    for rel, ref in (m.get("core", {}) or {}).items():
        p = base / rel
        if not p.exists(): raise RuntimeError(f"missing: {rel}")
        if _h(p) != ref:  raise RuntimeError(f"integrity failure: {rel}")
    return True
