"""
Ground-truth generation from hand-authored GLH DSL seed files.
Produces one JSON per connector for use in validation and self-healing DBs.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional
import argparse
import json
import logging

from glh.glh_pipeline import GLHDocument, Connector, ConnectorGeometry, Pin, parse_glh_blocks

log = logging.getLogger("glh.ground_truth")


def _connector_to_json(conn: Connector) -> Dict:
    geom = None
    if conn.geometry:
        geom = {"rows": conn.geometry.rows, "cols": conn.geometry.cols, "cavities": conn.geometry.cavities}
    pins = {
        label: {
            "color_primary": pin.color_primary,
            "color_secondary": pin.color_secondary,
            "function": pin.function,
        }
        for label, pin in conn.pins.items()
    }
    return {
        "connector_id": conn.connector_id,
        "geometry": geom,
        "pins": pins,
    }


def generate_ground_truth(dsl_dir: Path, out_dir: Path, page_map_csv: Optional[Path] = None) -> Dict[str, Path]:
    """Parse every DSL file in `dsl_dir` and write per-connector JSON to `out_dir`.

    Returns a mapping of connector_id -> JSON file path.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    cid_to_path: Dict[str, Path] = {}

    for path in sorted(dsl_dir.glob("*")):
        if not path.suffix.lower() in {".txt", ".glh"}:
            continue
        text = path.read_text(encoding="utf-8")
        doc = parse_glh_blocks(text)
        for cid, conn in doc.connectors.items():
            json_data = _connector_to_json(conn)
            out_path = out_dir / f"{cid}.json"
            out_path.write_text(json.dumps(json_data, indent=2), encoding="utf-8")
            cid_to_path[cid] = out_path
            log.info("Wrote GT for %s -> %s", cid, out_path)

    return cid_to_path


def load_ground_truth_cache(cache_dir: Path) -> GLHDocument:
    """Hydrate all JSON connector files in ``cache_dir`` into a GLHDocument."""
    doc = GLHDocument()
    for json_path in sorted(cache_dir.glob("*.json")):
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        cid = data.get("connector_id")
        if not cid:
            continue
        geom_data = data.get("geometry") or {}
        geom = None
        if geom_data:
            geom = ConnectorGeometry(
                rows=geom_data.get("rows", 0),
                cols=geom_data.get("cols", 0),
                cavities=geom_data.get("cavities", {}),
            )
        conn = Connector(connector_id=cid, geometry=geom)
        for label, info in (data.get("pins") or {}).items():
            conn.pins[label] = Pin(
                label=label,
                color_primary=info.get("color_primary"),
                color_secondary=info.get("color_secondary"),
                function=info.get("function"),
            )
        doc.connectors[cid] = conn
    return doc


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Generate per-connector ground truth JSON from GLH DSL seeds.")
    parser.add_argument("--dsl-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--page-map", type=Path, default=None, help="Optional page mapping CSV (reserved for future use)")
    args = parser.parse_args()

    generate_ground_truth(args.dsl_dir, args.out_dir, args.page_map)


if __name__ == "__main__":
    _cli()
