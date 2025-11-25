"""
Self-healing ground-truth database backed by JSONL files.

This module wires the ground-truth DB into the GLH pipeline by allowing
connectors extracted from PDFs, hand-written DSL, or manual annotations
to be appended as JSONL records, then hydrated back into ``GLHDocument``
objects for validation and active learning.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import json
import logging

from glh.glh_pipeline import (
    Connector,
    ConnectorGeometry,
    GLHDocument,
    Pin,
    parse_glh_blocks,
)
from glh.glh_validation import validate_extraction
from glh.glh_vision_fast import ingest_pdf_connectors_ultrafast

log = logging.getLogger("glh.gt_db")

GT_DB_PATH = Path("gt_db/glh_ground_truth_db.jsonl")
GT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def _load_lines() -> List[Dict[str, Any]]:
    if not GT_DB_PATH.exists():
        return []
    lines = []
    for raw in GT_DB_PATH.read_text(encoding="utf-8").splitlines():
        try:
            lines.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return lines


def _append_entry(entry: Dict[str, Any]) -> None:
    with GT_DB_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def _connector_entry(
    connector: Connector,
    source: str,
    pdf_path: str | None = None,
    page: int | None = None,
    confidence: float | None = None,
) -> Dict[str, Any]:
    return {
        "id": f"gt_{connector.connector_id}_{int(datetime.now().timestamp())}",
        "connector_id": connector.connector_id,
        "source": source,
        "created": datetime.now().isoformat(),
        "pdf": pdf_path,
        "page": page,
        "confidence": confidence,
        "geometry": {
            "rows": connector.geometry.rows if connector.geometry else 0,
            "cols": connector.geometry.cols if connector.geometry else 0,
            "cavities": connector.geometry.cavities if connector.geometry else {},
        },
        "pins": {
            label: {
                "color_primary": pin.color_primary,
                "color_secondary": pin.color_secondary,
                "function": pin.function,
            }
            for label, pin in connector.pins.items()
        },
    }


def generate_gt_from_dsl(dsl_text: str, source_name: str = "manual") -> List[Dict[str, Any]]:
    """Parse DSL text into GT entries and persist them.

    Returns the list of entries that were appended to the DB so callers can
    inspect or log them.
    """
    doc = parse_glh_blocks(dsl_text)
    entries: List[Dict[str, Any]] = []
    for connector in doc.connectors.values():
        entry = _connector_entry(connector, source=source_name)
        _append_entry(entry)
        entries.append(entry)
        log.info("Saved DSL GT for %s", connector.connector_id)
    return entries


def bless_extraction_as_gt(connector: Connector, pdf_path: str, page_num: int, confidence: float = 0.95) -> None:
    entry = _connector_entry(
        connector,
        source=f"auto_blessed_conf{confidence:.0%}",
        pdf_path=pdf_path,
        page=page_num,
        confidence=confidence,
    )
    _append_entry(entry)
    log.info("Blessed connector %s into GT DB", connector.connector_id)


def get_all_gt() -> List[Dict[str, Any]]:
    return _load_lines()


def gt_db_to_document() -> GLHDocument:
    doc = GLHDocument()
    for entry in get_all_gt():
        cid = entry.get("connector_id")
        if not cid:
            continue
        geom_data = entry.get("geometry") or {}
        geom = ConnectorGeometry(
            rows=geom_data.get("rows", 0),
            cols=geom_data.get("cols", 0),
            cavities=geom_data.get("cavities", {}),
        )
        conn = Connector(connector_id=cid, geometry=geom)
        for label, info in (entry.get("pins") or {}).items():
            conn.pins[label] = Pin(
                label=label,
                color_primary=info.get("color_primary"),
                color_secondary=info.get("color_secondary"),
                function=info.get("function"),
            )
        doc.connectors[cid] = conn
    return doc


def export_gt_to_dsl() -> str:
    """Quick dump of DB contents to a DSL-like text blob."""
    lines: List[str] = []
    for entry in get_all_gt():
        cid = entry.get("connector_id")
        if not cid:
            continue
        lines.append("```connector")
        lines.append(f"id={cid}")
        geom = entry.get("geometry") or {}
        if geom:
            lines.append(f"rows: {geom.get('rows', 0)}")
            lines.append(f"cols: {geom.get('cols', 0)}")
        for label, info in (entry.get("pins") or {}).items():
            color = info.get("color_primary")
            if info.get("color_secondary"):
                color = f"{color}/{info['color_secondary']}" if color else info['color_secondary']
            fn = info.get("function")
            tail = f", {fn}" if fn else ""
            lines.append(f"{label}: {color or ''}{tail}")
        lines.append("```")
    return "\n".join(lines)


def interactive_annotate_connector(pdf_path: str, page_num: int, connector_id: str) -> None:
    """Minimal CLI-based annotator for environments without GUI support."""

    def _prompt_pin() -> Tuple[str, Dict[str, Optional[str]]]:
        label = input("Pin label (e.g. A1, blank to finish): ").strip().upper()
        if not label:
            return "", {}
        color = input("  Color (RD/WH, optional): ").strip().upper() or None
        function = input("  Function (optional): ").strip() or None
        color_primary = None
        color_secondary = None
        if color:
            if "/" in color:
                color_primary, color_secondary = color.split("/", 1)
            else:
                color_primary = color
        return label, {
            "color_primary": color_primary,
            "color_secondary": color_secondary,
            "function": function,
        }

    print(f"Annotating {connector_id} on page {page_num} from {pdf_path}")
    try:
        rows = int(input("Rows (integer, default 0): ") or 0)
        cols = int(input("Cols (integer, default 0): ") or 0)
    except ValueError:
        rows = cols = 0

    pins: Dict[str, Dict[str, Optional[str]]] = {}
    while True:
        label, info = _prompt_pin()
        if not label:
            break
        pins[label] = info

    connector = Connector(
        connector_id=connector_id,
        geometry=ConnectorGeometry(rows=rows, cols=cols),
    )
    for label, info in pins.items():
        connector.pins[label] = Pin(
            label=label,
            color_primary=info.get("color_primary"),
            color_secondary=info.get("color_secondary"),
            function=info.get("function"),
        )

    entry = _connector_entry(
        connector,
        source="human_click",
        pdf_path=pdf_path,
        page=page_num,
    )
    _append_entry(entry)
    log.info("Annotation saved for %s", connector_id)


def active_learning_cycle(pdf_path: str, top_k: int = 3) -> None:
    """Run ingest + validation and prompt for annotations on low performers."""

    extracted_doc = ingest_pdf_connectors_ultrafast(pdf_path)
    gt_doc = gt_db_to_document()

    if not gt_doc.connectors:
        log.info("GT DB is empty; run manual annotation first.")
        return

    metrics = validate_extraction(extracted_doc, gt_doc)
    log.info("Current accuracy %.1f%%; selecting worst %d connectors", metrics.overall_score, top_k)

    ranked: List[Tuple[str, Dict[str, int]]] = sorted(
        metrics.details.items(),
        key=lambda kv: kv[1]["tp"] / max(1, kv[1]["tp"] + kv[1]["fp"] + kv[1]["fn"]),
    )

    for cid, stats in ranked[:top_k]:
        page_guess = 1
        conn = extracted_doc.connectors.get(cid)
        if conn and conn.sources:
            page_guess = conn.sources[0].get("page", 1)
        log.info(
            "Annotating %s (tp=%d fp=%d fn=%d) guessed page %s", cid, stats["tp"], stats["fp"], stats["fn"], page_guess
        )
        interactive_annotate_connector(pdf_path, page_guess, cid)
        log.info("Blessing corrected %s into DB", cid)
        if conn:
            bless_extraction_as_gt(conn, pdf_path, page_guess, confidence=0.95)

    log.info("Active learning cycle complete; rerun validation when ready.")


__all__ = [
    "GT_DB_PATH",
    "bless_extraction_as_gt",
    "generate_gt_from_dsl",
    "gt_db_to_document",
    "get_all_gt",
    "interactive_annotate_connector",
    "export_gt_to_dsl",
    "active_learning_cycle",
]
