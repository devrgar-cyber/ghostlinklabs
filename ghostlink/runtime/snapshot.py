# ghostlink/runtime/snapshot.py
from __future__ import annotations
from pathlib import Path
import json, yaml

def _load(p: Path):
    if not p.exists(): return None
    if p.suffix in {".yaml",".yml",".vault"}:
        return yaml.safe_load(p.read_text())
    if p.suffix == ".json":
        return json.loads(p.read_text())
    return p.read_text(errors="replace")

def snapshot_vault(vault_dir: Path, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    snap = {}
    for name in ["core.vault","macros.vault","memory_layer_01.vault","ghoststate.json"]:
        snap[name] = _load(vault_dir / name)
    (outdir / "snapshot.json").write_text(json.dumps(snap, indent=2, sort_keys=True))
    return str(outdir / "snapshot.json")
