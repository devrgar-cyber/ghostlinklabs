"""
Fast-path PDF ingestion with optional pixel parsing hooks.
This module wraps extraction results into the shared GLHDocument
so downstream validation and rendering can reuse the same IR.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List
import logging

from glh.glh_pipeline import (
    GLHDocument,
    Connector,
    ConnectorGeometry,
    ConnectorMention,
    build_connector_index,
    extract_text_blocks_from_pdf,
)

log = logging.getLogger("glh.vision_fast")


def _ingest_core(pdf_path: str, max_workers: int = 4) -> Dict[str, Connector]:
    """Lightweight connector harvest using text indexing.

    This intentionally leans on text-first extraction for speed and
    reliability in environments without OpenCV/PyMuPDF. If heavier
    pixel geometry is desired, plug it in where indicated.
    """
    connectors: Dict[str, Connector] = {}
    try:
        blocks = extract_text_blocks_from_pdf(pdf_path)
    except Exception as exc:
        log.warning("Text extraction failed for %s: %s", pdf_path, exc)
        return connectors

    index = build_connector_index(blocks)

    def _build_connector(cid: str, mentions: List[ConnectorMention]) -> tuple[str, Connector]:
        conn = Connector(connector_id=cid)
        conn.sources.extend({"page": m.page, "context": m.context} for m in mentions)
        # Geometry placeholder: fill from pixel/vector if available later.
        if mentions and mentions[0].bbox:
            conn.geometry = ConnectorGeometry(rows=0, cols=0)
        return cid, conn

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        for cid, connector in pool.map(lambda item: _build_connector(*item), index.items()):
            connectors[cid] = connector

    return connectors


def ingest_pdf_connectors_ultrafast(pdf_path: str, max_workers: int = 4) -> GLHDocument:
    """Public entry: return a GLHDocument from a PDF ingest.

    This wraps `_ingest_core` output in a GLHDocument to stay consistent
    with the rest of the pipeline.
    """
    connectors = _ingest_core(pdf_path, max_workers=max_workers)
    return GLHDocument(connectors=connectors)


__all__ = [
    "ingest_pdf_connectors_ultrafast",
]
