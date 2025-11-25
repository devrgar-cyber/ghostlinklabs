"""
PDF structure introspection utilities for GLH.

These helpers focus on *structural* comprehension of PDFs so the rest of the
pipeline can reason about why connector geometry appears where it does:
- xref/trailer metadata
- per-page resource summaries (fonts, images, vector draws)
- span-level text breakdown with bounding boxes

The goal is to expose "how the PDF is built" without forcing callers to dig
through raw PyMuPDF dictionaries.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Tuple
import logging

try:
    import fitz  # type: ignore
except Exception:  # ImportError or runtime error
    fitz = None  # type: ignore

log = logging.getLogger("glh.pdf_inspector")


@dataclass
class PDFSpanSummary:
    text: str
    bbox: Tuple[float, float, float, float]
    font: str | None
    size: float | None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "bbox": self.bbox,
            "font": self.font,
            "size": self.size,
        }


@dataclass
class PDFPageSummary:
    page_number: int
    mediabox: Tuple[float, float, float, float]
    text_spans: List[PDFSpanSummary] = field(default_factory=list)
    image_count: int = 0
    drawing_count: int = 0
    font_usage: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_number": self.page_number,
            "mediabox": self.mediabox,
            "text_spans": [s.to_dict() for s in self.text_spans],
            "image_count": self.image_count,
            "drawing_count": self.drawing_count,
            "font_usage": self.font_usage,
        }


@dataclass
class PDFStructureReport:
    path: str
    xref_objects: int
    trailer_keys: List[str]
    metadata: Dict[str, Any]
    pages: List[PDFPageSummary] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "xref_objects": self.xref_objects,
            "trailer_keys": self.trailer_keys,
            "metadata": self.metadata,
            "pages": [p.to_dict() for p in self.pages],
        }


def _summarize_page(page: "fitz.Page") -> PDFPageSummary:
    mediabox = (0.0, 0.0, float(page.rect.width), float(page.rect.height))
    raw = page.get_text("rawdict")

    spans: List[PDFSpanSummary] = []
    font_usage: Dict[str, int] = {}
    for block in raw.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text", "")
                bbox = (
                    float(span.get("bbox", [0, 0, 0, 0])[0]),
                    float(span.get("bbox", [0, 0, 0, 0])[1]),
                    float(span.get("bbox", [0, 0, 0, 0])[2]),
                    float(span.get("bbox", [0, 0, 0, 0])[3]),
                )
                font = span.get("font")
                size = float(span.get("size", 0.0)) if span.get("size") is not None else None
                spans.append(PDFSpanSummary(text=text, bbox=bbox, font=font, size=size))
                if font:
                    font_usage[font] = font_usage.get(font, 0) + 1

    drawings = page.get_drawings()
    images = page.get_images(full=True)

    return PDFPageSummary(
        page_number=page.number + 1,
        mediabox=mediabox,
        text_spans=spans,
        image_count=len(images),
        drawing_count=len(drawings),
        font_usage=dict(sorted(font_usage.items(), key=lambda kv: kv[1], reverse=True)),
    )


def summarize_pdf_structure(pdf_path: Path) -> PDFStructureReport:
    if fitz is None:
        raise RuntimeError("PyMuPDF (fitz) is not installed")
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    doc = fitz.open(pdf_path)
    pages = [_summarize_page(doc.load_page(i)) for i in range(len(doc))]
    report = PDFStructureReport(
        path=str(pdf_path),
        xref_objects=doc.xref_length(),
        trailer_keys=sorted(doc.trailer.keys()) if doc.trailer else [],
        metadata=doc.metadata or {},
        pages=pages,
    )
    doc.close()
    return report


def pretty_print_report(report: PDFStructureReport) -> str:
    lines: List[str] = []
    lines.append(f"PDF: {report.path}")
    lines.append(f"XREF objects: {report.xref_objects}")
    if report.trailer_keys:
        lines.append(f"Trailer keys: {', '.join(report.trailer_keys)}")
    if report.metadata:
        lines.append("Metadata:")
        for k, v in report.metadata.items():
            lines.append(f"  {k}: {v}")

    for page in report.pages:
        lines.append("")
        lines.append(f"Page {page.page_number}: {page.mediabox}")
        lines.append(
            f"  Text spans: {len(page.text_spans)} | Images: {page.image_count} | Drawings: {page.drawing_count}"
        )
        if page.font_usage:
            font_list = ", ".join(f"{name}×{count}" for name, count in page.font_usage.items())
            lines.append(f"  Fonts: {font_list}")
        for span in page.text_spans[:5]:
            excerpt = span.text.replace("\n", " ⏎ ")
            lines.append(f"    [{span.font or '?'} {span.size or 0:.1f}] {excerpt} @ {span.bbox}")
        if len(page.text_spans) > 5:
            lines.append(f"    ... {len(page.text_spans) - 5} more spans")

    return "\n".join(lines)
