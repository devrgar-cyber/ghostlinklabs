# scripts/hash_manifest.py
"""
Compute SHA-256 hashes for core GhostLink files and write vault/manifest.json.
Usage:
  python scripts/hash_manifest.py            # dry-run, prints JSON to stdout
  python scripts/hash_manifest.py --write    # writes vault/manifest.json
"""
from __future__ import annotations
import argparse, json, hashlib, sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"

GLOBS: List[str] = [
    "ghostlink/runtime/*.py",
    "ghostlink/tools/*.py",
    "ghostlink/boot/*.py",
    "ghostlink/dreamshell.py",
    "ghostlink/__init__.py",
]

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def collect() -> Dict[str, str]:
    core: Dict[str, str] = {}
    for pattern in GLOBS:
        for p in ROOT.glob(pattern):
            rel = p.relative_to(ROOT).as_posix()
            core[rel] = sha256_file(p)
    return core

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write vault/manifest.json")
    args = parser.parse_args()

    core = collect()
    manifest = {"version": "1.0", "hash_algo": "sha256", "core": dict(sorted(core.items()))}

    if args.write:
        VAULT.mkdir(parents=True, exist_ok=True)
        out = VAULT / "manifest.json"
        out.write_text(json.dumps(manifest, indent=2, sort_keys=True))
        print(f"wrote {out}")
    else:
        json.dump(manifest, sys.stdout, indent=2, sort_keys=True); print()

if __name__ == "__main__":
    main()
