# scripts/init_vault.py
"""Seed the vault with default files if they do not exist."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"

DEFAULT_CORE = """
version: 1
constants:
  receipts_required: true
  sovereign_default: true
  allowed_outputs: [".txt", ".md", ".json"]
  codex64: "SIGNAL·COMPREHENSION·LINK·MIRROR·FIBER·PROCESSORS·TILE·DRIFT·CONTAINER·SEED·GAPS·TRACE·SCAR·STACK·PATH·MEMORY·FORGE·GRID·CORE·VAULT·WRAP·GATE·ARCHIVE·TUNNEL·FRAME·CURRENT·MARKER·KEY·CHANNEL·OFFSET·THRESHOLD·SHEAR·DUALITY·ECHO·BIND·PRISM·SHADOW·CRYPT·PULSE·CALM·DEPTH·NODE·STATIC·DELTA·SPINE·HARMONY·LENS·LOCK·MIRROR·SIGNAL·LINK·WRAP·PRESSURE·GHOST·SENTINEL·HOST·FORGE·MIRROR·SEED·LINK·EXECUTE·BUILD·KEY·COMPREHENSION"
""".lstrip()

DEFAULT_MACROS = """
version: 1
macros:
  DEEPWALK:
    comment: canonical, offline diagnostic pass
    steps:
      - tool: MAP
        with: { source: "{{file}}" }
      - tool: REFLECT
        with: { data: "{{prev}}" }
      - tool: RECAST
        with: { data: "{{prev}}", to: "json" }
    params:
      required: ["file"]

  SCANFORGE:
    comment: scan a file, render to JSON text, forge artifact
    steps:
      - tool: SCAN
        with: { source: "{{file}}" }
      - tool: RECAST
        with: { data: "{{prev}}", to: "json" }
      - tool: FORGE
        with:
          artifact: "scan_report.json"
          mode: "json"
          content: "{{prev.text}}"
    params:
      required: ["file"]
""".lstrip()

DEFAULT_MEMORY = """
version: 1
notes:
  - "GhostLink vault initialized."
  - "Receipts are append-only in vault/receipts.log"
""".lstrip()

def write_if_missing(path: Path, content: str):
    if not path.exists():
        path.write_text(content, encoding="utf-8")
        print(f"created {path}")
    else:
        print(f"exists  {path}")

if __name__ == "__main__":
    (VAULT / "logs").mkdir(parents=True, exist_ok=True)
    write_if_missing(VAULT / "core.vault", DEFAULT_CORE)
    write_if_missing(VAULT / "macros.vault", DEFAULT_MACROS)
    write_if_missing(VAULT / "memory_layer_01.vault", DEFAULT_MEMORY)
    mf = VAULT / "manifest.json"
    if not mf.exists():
        mf.write_text('{"version":"1.0","hash_algo":"sha256","core":{}}
')
        print(f"created {mf}")
    else:
        print(f"exists  {mf}")
