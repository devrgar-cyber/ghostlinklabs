"""
GhostLink Harness (GLH) – Upfitter Brain Pipeline
=================================================

Pipeline summary:
1. PDF ingestion (page + line level) and connector mention indexing.
2. GLH DSL parsing (legend, connector, harness, void).
3. Fusion of PDF-derived mentions with DSL-defined connectors.
4. Geometry extraction hooks (vector + pixel; pixel implemented with PyMuPDF + OpenCV + Tesseract when available).
5. Rule engine checks (AWG vs. current, CAN tap guardrails).
6. ASCII renderers for connectors and harness netlists.
7. UpfitSkillAgent wrapper for orchestration and a simple CLI demo.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from collections import Counter
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
import argparse
import importlib.util
import logging
import re

# Optional heavy dependencies
try:
    import pdfplumber  # type: ignore
except Exception:  # ImportError, etc.
    pdfplumber = None  # type: ignore

try:
    import fitz  # type: ignore
except Exception:  # ImportError, etc.
    fitz = None  # type: ignore

try:
    import cv2  # type: ignore
    import numpy as np  # type: ignore
except Exception:  # ImportError, etc.
    cv2 = None  # type: ignore
    np = None  # type: ignore

try:
    import pytesseract  # type: ignore
except Exception:  # ImportError, etc.
    pytesseract = None  # type: ignore

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("glh")


# =========================
# 1. Core IR / Schema
# =========================

class SignalType(Enum):
    POWER = auto()
    GROUND = auto()
    DATA = auto()
    SENSE = auto()
    CONTROL = auto()
    UNKNOWN = auto()


@dataclass
class VehiclePlatform:
    make: str
    model: str
    year: int
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConnectorGeometry:
    rows: int
    cols: int
    cavities: Dict[Tuple[int, int], str] = field(default_factory=dict)


@dataclass
class Pin:
    label: str
    row: Optional[int] = None
    col: Optional[int] = None
    color_primary: Optional[str] = None
    color_secondary: Optional[str] = None
    awg: Optional[int] = None
    function: Optional[str] = None
    signal_type: SignalType = SignalType.UNKNOWN
    page: Optional[int] = None
    x: Optional[float] = None
    y: Optional[float] = None


@dataclass
class Connector:
    connector_id: str
    description: Optional[str] = None
    location: Optional[str] = None
    geometry: Optional[ConnectorGeometry] = None
    pins: Dict[str, Pin] = field(default_factory=dict)
    sources: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class WireNet:
    net_id: str
    from_connector: str
    from_pin: str
    to_connector: str
    to_pin: str
    awg: Optional[int] = None
    length_ft: Optional[float] = None
    color_primary: Optional[str] = None
    color_secondary: Optional[str] = None
    category: Optional[str] = None


@dataclass
class Load:
    load_id: str
    description: str
    continuous_current_a: float
    peak_current_a: float
    location: Optional[str] = None
    priority: Optional[int] = None


@dataclass
class Rule:
    rule_id: str
    description: str
    severity: str
    source: str


@dataclass
class Harness:
    harness_id: str
    connectors: Dict[str, Connector] = field(default_factory=dict)
    nets: List[WireNet] = field(default_factory=list)
    loads: Dict[str, Load] = field(default_factory=dict)


@dataclass
class GLHDocument:
    platform: Optional[VehiclePlatform] = None
    legend: Dict[str, str] = field(default_factory=dict)
    connectors: Dict[str, Connector] = field(default_factory=dict)
    harnesses: Dict[str, Harness] = field(default_factory=dict)
    voids: List[Dict[str, Any]] = field(default_factory=list)


# =========================
# 2. DSL Parsing
# =========================

FENCE_RE = re.compile(r"```(\w+)(.*?)```", re.DOTALL)
PIN_LABEL_RE = re.compile(r"^([A-Z]+)(\d+)$")


def parse_glh_blocks(text: str) -> GLHDocument:
    doc = GLHDocument()

    for match in FENCE_RE.finditer(text):
        block_type = match.group(1).strip().lower()
        body = match.group(2).strip()

        if block_type == "legend":
            _parse_legend_block(doc, body)
        elif block_type == "connector":
            _parse_connector_block(doc, body)
        elif block_type == "harness":
            _parse_harness_block(doc, body)
        elif block_type == "void":
            _parse_void_block(doc, body)
        else:
            log.warning("Unknown GLH block type: %s", block_type)

    return doc


def _parse_legend_block(doc: GLHDocument, body: str) -> None:
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        doc.legend[key.strip()] = val.strip()


def _parse_connector_block(doc: GLHDocument, body: str) -> None:
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    header: Dict[str, str] = {}
    pin_lines: List[str] = []

    pin_pattern = re.compile(r"^[A-Z]?\d+\s*:")
    for line in lines:
        if pin_pattern.match(line):
            pin_lines.append(line)
        else:
            if "=" in line:
                k, v = line.split("=", 1)
                header[k.strip().lower()] = v.strip()
            elif ":" in line:
                k, v = line.split(":", 1)
                header[k.strip().lower()] = v.strip()

    connector_id = header.get("id") or header.get("connector_id")
    if not connector_id:
        log.warning("Connector block without id; skipping")
        return

    rows = int(header.get("rows", "0") or 0)
    cols = int(header.get("cols", "0") or 0)
    geom = ConnectorGeometry(rows=rows, cols=cols)

    conn = Connector(
        connector_id=connector_id,
        description=header.get("description"),
        location=header.get("location"),
        geometry=geom,
    )

    for pline in pin_lines:
        label, rest = pline.split(":", 1)
        label = label.strip()
        rest = rest.strip()

        color_primary = None
        color_secondary = None
        function = None

        if rest:
            parts = [p.strip() for p in rest.split(",")]
            if parts:
                color_part = parts[0]
                if "/" in color_part:
                    c1, c2 = color_part.split("/", 1)
                    color_primary = c1.strip()
                    color_secondary = c2.strip()
                else:
                    color_primary = color_part
                if len(parts) > 1:
                    function = ", ".join(parts[1:])

        pin = Pin(
            label=label,
            color_primary=color_primary,
            color_secondary=color_secondary,
            function=function,
        )
        conn.pins[label] = pin

        r, c = _parse_pin_row_col(label)
        if r is not None and c is not None:
            geom.cavities[(r, c)] = label
            pin.row = r
            pin.col = c

    doc.connectors[connector_id] = conn


def _parse_harness_block(doc: GLHDocument, body: str) -> None:
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    header: Dict[str, str] = {}
    net_lines: List[str] = []
    load_lines: List[str] = []

    for line in lines:
        if line.lower().startswith("net "):
            net_lines.append(line)
        elif line.lower().startswith("load "):
            load_lines.append(line)
        else:
            if "=" in line:
                k, v = line.split("=", 1)
                header[k.strip().lower()] = v.strip()

    harness_id = header.get("id") or header.get("harness_id")
    if not harness_id:
        log.warning("Harness block without id; skipping")
        return

    harness = Harness(harness_id=harness_id)

    net_re = re.compile(
        r"^net\s+(\S+)\s*:\s*(\S+)\.(\S+)\s*->\s*(\S+)\.(\S+)\s*,\s*(\d+)AWG\s*,\s*(\S+)",
        re.IGNORECASE,
    )

    for nline in net_lines:
        m = net_re.match(nline)
        if not m:
            log.warning("Could not parse net line: %s", nline)
            continue
        net_id, c1, p1, c2, p2, awg_str, cat = m.groups()
        net = WireNet(
            net_id=net_id,
            from_connector=c1,
            from_pin=p1,
            to_connector=c2,
            to_pin=p2,
            awg=int(awg_str),
            category=cat,
        )
        harness.nets.append(net)

    load_re = re.compile(
        r'^load\s+(\S+)\s*:\s*"(.*?)"\s*,\s*([\d.]+)A\s*,\s*([\d.]+)A_peak\s*,\s*(.*)$',
        re.IGNORECASE,
    )

    for lline in load_lines:
        m = load_re.match(lline)
        if not m:
            log.warning("Could not parse load line: %s", lline)
            continue
        load_id, desc, cont_str, peak_str, tail = m.groups()
        location = None
        priority = None
        parts = [p.strip() for p in tail.split(",") if p.strip()]
        for part in parts:
            if part.lower().startswith("priority="):
                try:
                    priority = int(part.split("=", 1)[1])
                except ValueError:
                    priority = None
            else:
                location = part

        load = Load(
            load_id=load_id,
            description=desc,
            continuous_current_a=float(cont_str),
            peak_current_a=float(peak_str),
            location=location,
            priority=priority,
        )
        harness.loads[load_id] = load

    doc.harnesses[harness_id] = harness


def _parse_void_block(doc: GLHDocument, body: str) -> None:
    entry: Dict[str, Any] = {}
    for line in body.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        k, v = line.split(":", 1)
        entry[k.strip()] = v.strip()
    if entry:
        doc.voids.append(entry)


# =========================
# 3. PDF Text Ingestion
# =========================

CONNECTOR_ID_RE = re.compile(r"\bC\d{3,4}\b")
CONNECTOR_ID_FLEX_RE = re.compile(r"\bC[\s-]?(\d{3,4})\b", re.IGNORECASE)
CAP_ID_RE = re.compile(r"\bCAP[\s-]?(\d+)\b", re.IGNORECASE)


@dataclass
class PDFChar:
    """Lowest-level glyph info captured from the text extraction layer.

    PDF text is placed via content stream operators (e.g., TJ/Tj) that draw
    glyphs from an embedded font at specific coordinates. Capturing chars lets
    us reason about soft hyphens, ligatures, and font changes that word-level
    APIs can obscure.
    """

    text: str
    bbox: Tuple[float, float, float, float]
    font: Optional[str] = None
    size: Optional[float] = None


@dataclass
class PDFTextBlock:
    page: int
    text: str
    bbox: Tuple[float, float, float, float]
    granularity: str = "page"
    chars: List[PDFChar] = field(default_factory=list)


@dataclass
class PDFWord:
    text: str
    bbox: Tuple[float, float, float, float]


@dataclass
class PDFLine:
    text: str
    bbox: Tuple[float, float, float, float]
    words: List[PDFWord]


@dataclass
class PDFPrimitive:
    """Vector/image primitive description for PDF introspection.

    PDF pages are content streams referencing resources (fonts, XObjects,
    images). When available, we snapshot the high-level primitives so callers
    can understand why geometry shows up where it does (lines, paths, images).
    """

    kind: str  # "line", "curve", "rect", "image", "text-span"
    bbox: Tuple[float, float, float, float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConnectorMention:
    connector_id: str
    page: int
    context: str
    bbox: Optional[Tuple[float, float, float, float]] = None
    source: str = "page"


def _words_to_line(word_dicts: List[Dict[str, Any]]) -> PDFLine:
    words = [
        PDFWord(
            text=w["text"],
            bbox=(
                float(w["x0"]),
                float(w.get("top", 0.0)),
                float(w["x1"]),
                float(w.get("bottom", 0.0)),
            ),
        )
        for w in word_dicts
    ]

    text = " ".join(w.text for w in words)
    x0 = min(w.bbox[0] for w in words)
    y0 = min(w.bbox[1] for w in words)
    x1 = max(w.bbox[2] for w in words)
    y1 = max(w.bbox[3] for w in words)
    return PDFLine(text=text, bbox=(x0, y0, x1, y1), words=words)


def _chars_to_line(char_dicts: List[Dict[str, Any]]) -> Tuple[str, Tuple[float, float, float, float], List[PDFChar]]:
    """Collapse adjacent chars into a text string and bounding box.

    Char-level grouping is intentionally loose so callers can reconstruct
    kerning/spacing decisions later if needed. We keep the individual glyphs
    alongside the aggregate.
    """

    chars = [
        PDFChar(
            text=c.get("text", ""),
            bbox=(
                float(c.get("x0", 0.0)),
                float(c.get("top", 0.0)),
                float(c.get("x1", 0.0)),
                float(c.get("bottom", 0.0)),
            ),
            font=c.get("fontname"),
            size=float(c.get("size", 0.0)) if c.get("size") is not None else None,
        )
        for c in char_dicts
    ]

    text = "".join(ch.text for ch in chars)
    x0 = min(ch.bbox[0] for ch in chars)
    y0 = min(ch.bbox[1] for ch in chars)
    x1 = max(ch.bbox[2] for ch in chars)
    y1 = max(ch.bbox[3] for ch in chars)
    return text, (x0, y0, x1, y1), chars


def _group_words_into_lines(words: List[Dict[str, Any]], *, y_tolerance: float = 2.0) -> List[PDFLine]:
    if not words:
        return []

    sorted_words = sorted(words, key=lambda w: (w.get("top", 0.0), w.get("x0", 0.0)))
    lines: List[PDFLine] = []
    current: List[Dict[str, Any]] = []
    current_top: Optional[float] = None

    for word in sorted_words:
        top = word.get("top", 0.0)
        if current_top is None or abs(top - current_top) <= y_tolerance:
            current.append(word)
            current_top = top if current_top is None else min(current_top, top)
            continue

        lines.append(_words_to_line(current))
        current = [word]
        current_top = top

    if current:
        lines.append(_words_to_line(current))

    return lines


def _group_chars_into_lines(chars: List[Dict[str, Any]], *, y_tolerance: float = 1.5) -> List[Tuple[str, Tuple[float, float, float, float], List[PDFChar]]]:
    """Cluster chars by baseline proximity to approximate original text lines."""

    if not chars:
        return []

    sorted_chars = sorted(chars, key=lambda c: (c.get("top", 0.0), c.get("x0", 0.0)))
    lines: List[List[Dict[str, Any]]] = []
    current: List[Dict[str, Any]] = []
    current_top: Optional[float] = None

    for char in sorted_chars:
        top = char.get("top", 0.0)
        if current_top is None or abs(top - current_top) <= y_tolerance:
            current.append(char)
            current_top = top if current_top is None else min(current_top, top)
            continue

        lines.append(current)
        current = [char]
        current_top = top

    if current:
        lines.append(current)

    return [_chars_to_line(line) for line in lines]


def extract_text_blocks_from_pdf(pdf_path: str) -> List[PDFTextBlock]:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(pdf_path)
    if pdfplumber is None:
        raise RuntimeError("pdfplumber is not installed")

    blocks: List[PDFTextBlock] = []

    with pdfplumber.open(str(path)) as pdf:
        for page_index, page in enumerate(pdf.pages):
            page_text = page.extract_text() or ""
            page_bbox = (0.0, 0.0, float(page.width), float(page.height))
            blocks.append(
                PDFTextBlock(
                    page=page_index + 1,
                    text=page_text,
                    bbox=page_bbox,
                    granularity="page",
                )
            )

            word_dicts = page.extract_words() or []
            for line in _group_words_into_lines(word_dicts):
                blocks.append(
                    PDFTextBlock(
                        page=page_index + 1,
                        text=line.text,
                        bbox=line.bbox,
                        granularity="line",
                    )
                )

            # Char-level capture so we can reason about hyphenation and fonts
            char_dicts = getattr(page, "chars", None) or []
            for text, bbox, chars in _group_chars_into_lines(char_dicts):
                blocks.append(
                    PDFTextBlock(
                        page=page_index + 1,
                        text=text,
                        bbox=bbox,
                        granularity="char-line",
                        chars=chars,
                    )
                )

    return blocks


# =========================
# 3b. PDF Structure Introspection
# =========================


def dissect_pdf_page(pdf_path: str, page_num: int) -> Tuple[List[PDFPrimitive], Dict[str, Any]]:
    """Inspect raw PDF primitives to expose how the page is constructed.

    PyMuPDF exposes the content streams (text spans, vector paths, images).
    This mirrors how a PDF viewer rasterizes a page and helps us debug
    connector glyph placement when the text layer is sparse or absent.
    """

    if fitz is None:
        raise RuntimeError("PyMuPDF not installed")

    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num - 1)

    primitives: List[PDFPrimitive] = []

    text_dict = page.get_text("dict")  # spans with font, size, color
    for block in text_dict.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                bbox = tuple(float(v) for v in span.get("bbox", (0, 0, 0, 0)))
                primitives.append(
                    PDFPrimitive(
                        kind="text-span",
                        bbox=bbox,  # type: ignore[arg-type]
                        metadata={
                            "text": span.get("text", ""),
                            "font": span.get("font"),
                            "size": span.get("size"),
                            "color": span.get("color"),
                        },
                    )
                )

    for drawing in page.get_drawings():
        bbox = drawing.get("rect")
        bbox_tuple = (float(bbox.x0), float(bbox.y0), float(bbox.x1), float(bbox.y1)) if bbox else (0.0, 0.0, 0.0, 0.0)
        primitives.append(
            PDFPrimitive(
                kind="path",
                bbox=bbox_tuple,
                metadata={
                    "stroke": drawing.get("stroke"),
                    "fill": drawing.get("fill"),
                    "items": len(drawing.get("items", [])),
                },
            )
        )

    for img in page.get_images(full=True):
        xref = img[0]
        bbox = page.get_image_bbox(xref)
        bbox_tuple = (float(bbox.x0), float(bbox.y0), float(bbox.x1), float(bbox.y1))
        primitives.append(
            PDFPrimitive(
                kind="image",
                bbox=bbox_tuple,
                metadata={
                    "xref": xref,
                    "width": img[2],
                    "height": img[3],
                    "cs": img[4],
                    "bpc": img[5],
                },
            )
        )

    info = {
        "page": page_num,
        "mediabox": (float(page.rect.x0), float(page.rect.y0), float(page.rect.x1), float(page.rect.y1)),
        "rotation": page.rotation,
        "primitives": len(primitives),
    }
    doc.close()
    return primitives, info


def summarize_pdf_primitives(primitives: List[PDFPrimitive], info: Dict[str, Any], *, limit: int = 5) -> str:
    """Human-readable summary of the page makeup.

    This is intentionally lightweight so it can be printed from the CLI
    without dumping full JSON for large manuals.
    """

    lines: List[str] = []
    lines.append(
        f"PDF page {info.get('page')} mediabox={info.get('mediabox')} rotation={info.get('rotation')} primitives={info.get('primitives')}"
    )
    counts = Counter(p.kind for p in primitives)
    if counts:
        counts_str = ", ".join(f"{k}:{v}" for k, v in counts.items())
        lines.append(f"Kinds: {counts_str}")

    for prim in primitives[:limit]:
        meta_preview = {k: v for k, v in prim.metadata.items() if k in {"text", "font", "size", "stroke", "fill", "xref"}}
        lines.append(f"  - {prim.kind} bbox={prim.bbox} meta={meta_preview}")

    if len(primitives) > limit:
        lines.append(f"  ... (+{len(primitives) - limit} more primitives)")

    return "\n".join(lines)


def build_connector_index(blocks: List[PDFTextBlock]) -> Dict[str, List[ConnectorMention]]:
    index: Dict[str, List[ConnectorMention]] = {}

    for block in blocks:
        text = block.text

        for m in CONNECTOR_ID_RE.finditer(text):
            cid = m.group(0)
            ctx_start = max(0, m.start() - 40)
            ctx_end = min(len(text), m.end() + 40)
            ctx = text[ctx_start:ctx_end]
            mention = ConnectorMention(
                connector_id=cid,
                page=block.page,
                context=ctx,
                bbox=block.bbox,
                source=block.granularity,
            )
            index.setdefault(cid, []).append(mention)

        for m in CONNECTOR_ID_FLEX_RE.finditer(text):
            cid = f"C{m.group(1)}"
            ctx_start = max(0, m.start() - 40)
            ctx_end = min(len(text), m.end() + 40)
            ctx = text[ctx_start:ctx_end]
            mention = ConnectorMention(
                connector_id=cid,
                page=block.page,
                context=ctx,
                bbox=block.bbox,
                source=block.granularity,
            )
            index.setdefault(cid, []).append(mention)

        for m in CAP_ID_RE.finditer(text):
            cid = f"CAP{m.group(1)}"
            ctx_start = max(0, m.start() - 40)
            ctx_end = min(len(text), m.end() + 40)
            ctx = text[ctx_start:ctx_end]
            mention = ConnectorMention(
                connector_id=cid,
                page=block.page,
                context=ctx,
                bbox=block.bbox,
                source=block.granularity,
            )
            index.setdefault(cid, []).append(mention)

    # Deduplicate identical page/context entries to avoid noisy repeats from
    # overlapping granularity (page + line + char-line).
    for cid, mentions in list(index.items()):
        seen = set()
        deduped: List[ConnectorMention] = []
        for m in mentions:
            key = (m.page, m.context, m.bbox, m.source)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(m)
        index[cid] = deduped

    return index


# =========================
# 4. Geometry & Fusion
# =========================


def extract_vector_geometry_for_connector(
    pdf_path: str,
    connector_id: str,
    mentions: List[ConnectorMention],
) -> Optional[ConnectorGeometry]:
    _ = (pdf_path, connector_id, mentions)
    return None


def render_pdf_page_to_image(pdf_path: str, page_num: int, dpi: int = 300):
    if fitz is None or np is None:
        raise RuntimeError("PyMuPDF/NumPy not installed")

    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num - 1)
    pix = page.get_pixmap(dpi=dpi)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    if pix.n == 4:
        img = img[:, :, :3]
    doc.close()
    return img


def detect_connector_body(img) -> Optional[Tuple[int, int, int, int]]:
    if cv2 is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for cnt in contours[:5]:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), closed=True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            if w > 100 and h > 50:
                return x, y, w, h
    return None


def detect_pin_cavities(crop_img) -> List[Tuple[int, int]]:
    pins: List[Tuple[int, int]] = []
    if cv2 is None:
        return pins

    gray = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20,
                               param1=50, param2=30, minRadius=5, maxRadius=20)
    if circles is not None:
        circles = circles[0, :].round().astype(int)
        pins.extend((int(x), int(y)) for x, y, _ in circles)

    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if 10 < w < 30 and 10 < h < 30:
            pins.append((x + w // 2, y + h // 2))

    return pins


def cluster_pins_to_grid(pins: List[Tuple[int, int]]) -> ConnectorGeometry:
    if not pins:
        return ConnectorGeometry(rows=0, cols=0)

    pins_sorted = sorted(pins, key=lambda p: (p[1], p[0]))
    rows_list: List[List[Tuple[int, int]]] = []
    current_row = [pins_sorted[0]]
    for p in pins_sorted[1:]:
        if abs(p[1] - current_row[-1][1]) < 20:
            current_row.append(p)
        else:
            rows_list.append(sorted(current_row, key=lambda pp: pp[0]))
            current_row = [p]
    if current_row:
        rows_list.append(sorted(current_row, key=lambda pp: pp[0]))

    num_rows = len(rows_list)
    num_cols = max(len(r) for r in rows_list) if rows_list else 0

    geom = ConnectorGeometry(rows=num_rows, cols=num_cols)
    for r_idx, row in enumerate(rows_list):
        for c_idx, _ in enumerate(row):
            label = f"{chr(65 + r_idx)}{c_idx + 1}"
            geom.cavities[(r_idx + 1, c_idx + 1)] = label

    return geom


def ocr_pin_info(crop_img, pins: List[Tuple[int, int]]) -> Dict[str, Dict[str, Any]]:
    info: Dict[str, Dict[str, Any]] = {}
    if cv2 is None or pytesseract is None:
        return info

    gray = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    for idx, (px, py) in enumerate(pins):
        roi = binary[max(0, py - 20):py + 20, max(0, px - 50):px + 50]
        if roi.size == 0:
            continue
        text = pytesseract.image_to_string(roi).strip().upper()
        if not text:
            continue

        parts = re.split(r"\s+", text)
        label = parts[0] if re.match(r"[A-Z]?\d+", parts[0]) else f"PIN{idx + 1}"
        color = parts[1] if len(parts) > 1 else None
        func = " ".join(parts[2:]) if len(parts) > 2 else None

        primary, secondary = (color.split("/") if color and "/" in color else (color, None))
        info[label] = {
            "color_primary": primary,
            "color_secondary": secondary,
            "function": func,
        }

    return info


def extract_pixel_geometry_for_connector(
    pdf_path: str,
    connector_id: str,
    mentions: List[ConnectorMention],
    doc: GLHDocument,
) -> Optional[ConnectorGeometry]:
    if fitz is None or cv2 is None or np is None:
        log.info("pixel geometry skipped for %s (missing deps)", connector_id)
        return None
    if not mentions:
        return None

    page = mentions[0].page
    img = render_pdf_page_to_image(pdf_path, page)

    if mentions[0].bbox:
        x0, y0, x1, y1 = mentions[0].bbox
        img = img[int(y0):int(y1), int(x0):int(x1)]

    body_bbox = detect_connector_body(img)
    if not body_bbox:
        log.warning("No connector body detected for %s on page %s", connector_id, page)
        return None

    x, y, w, h = body_bbox
    crop = img[y:y + h, x:x + w]

    pins_centers = detect_pin_cavities(crop)
    geom = cluster_pins_to_grid(pins_centers)

    conn = doc.connectors.get(connector_id)
    if conn:
        pin_info = ocr_pin_info(crop, pins_centers)
        for label, info in pin_info.items():
            pin = conn.pins.get(label)
            if pin is None:
                pin = Pin(label=label)
                conn.pins[label] = pin
            pin.color_primary = info.get("color_primary")
            pin.color_secondary = info.get("color_secondary")
            pin.function = info.get("function")
            r, c = _parse_pin_row_col(label)
            if r and c:
                geom.cavities[(r, c)] = label
                pin.row = r
                pin.col = c

    return geom


def fuse_connectors(
    doc: GLHDocument,
    pdf_index: Dict[str, List[ConnectorMention]],
    pdf_path: str,
) -> None:
    for cid, mentions in pdf_index.items():
        conn = doc.connectors.get(cid)
        if not conn:
            conn = Connector(connector_id=cid)
            doc.connectors[cid] = conn

        conn.sources.extend({"page": m.page, "context": m.context, "source": m.source} for m in mentions)

        if conn.geometry is None:
            geom = extract_vector_geometry_for_connector(pdf_path, cid, mentions)
            if geom is None:
                geom = extract_pixel_geometry_for_connector(pdf_path, cid, mentions, doc)
            if geom is not None:
                conn.geometry = geom


# =========================
# 5. Rule Engine
# =========================

@dataclass
class RuleViolation:
    rule_id: str
    severity: str
    message: str
    context: Dict[str, Any]


class RuleEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = {r.rule_id: r for r in rules}

    def run_all(self, doc: GLHDocument) -> List[RuleViolation]:
        violations: List[RuleViolation] = []
        violations.extend(self._check_awg_vs_current(doc))
        violations.extend(self._check_can_taps(doc))
        return violations

    def _check_awg_vs_current(self, doc: GLHDocument) -> List[RuleViolation]:
        violations: List[RuleViolation] = []
        awg_table = {20: 5.0, 18: 10.0, 16: 15.0, 14: 20.0}

        for harness in doc.harnesses.values():
            for net in harness.nets:
                if net.awg is None or net.to_connector != "LOAD":
                    continue
                load = harness.loads.get(net.to_pin)
                if not load:
                    continue
                max_a = awg_table.get(net.awg, 0.0)
                if load.continuous_current_a > max_a:
                    violations.append(
                        RuleViolation(
                            rule_id="AWG_CURRENT",
                            severity="error",
                            message=f"AWG {net.awg} too thin for {load.continuous_current_a}A on {net.net_id}",
                            context={"net": net.net_id, "load": load.load_id},
                        )
                    )
        return violations

    def _check_can_taps(self, doc: GLHDocument) -> List[RuleViolation]:
        violations: List[RuleViolation] = []
        for harness in doc.harnesses.values():
            for net in harness.nets:
                if net.category and net.category.lower() == "can":
                    from_pin = doc.connectors.get(net.from_connector, Connector("" )).pins.get(net.from_pin)
                    to_pin = doc.connectors.get(net.to_connector, Connector("" )).pins.get(net.to_pin)
                    if from_pin and from_pin.signal_type in (SignalType.POWER, SignalType.GROUND):
                        violations.append(
                            RuleViolation(
                                rule_id="CAN_POWER",
                                severity="error",
                                message=f"Power/GND on CAN net {net.net_id}",
                                context={"net": net.net_id},
                            )
                        )
                    if to_pin and to_pin.signal_type in (SignalType.POWER, SignalType.GROUND):
                        violations.append(
                            RuleViolation(
                                rule_id="CAN_POWER",
                                severity="error",
                                message=f"Power/GND on CAN net {net.net_id}",
                                context={"net": net.net_id},
                            )
                        )
        return violations


# =========================
# 6. ASCII Rendering
# =========================


def _parse_pin_row_col(label: str) -> Tuple[Optional[int], Optional[int]]:
    m = PIN_LABEL_RE.match(label.strip().upper())
    if not m:
        return None, None
    row_letters, col_str = m.groups()
    row_idx = ord(row_letters[0]) - ord("A") + 1
    col_idx = int(col_str)
    return row_idx, col_idx


def render_connector_ascii(conn: Connector, legend: Optional[Dict[str, str]] = None) -> str:
    legend = legend or {}

    if conn.geometry is None or conn.geometry.rows == 0 or conn.geometry.cols == 0:
        row_set = set()
        col_set = set()
        for label in conn.pins.keys():
            r, c = _parse_pin_row_col(label)
            if r is not None and c is not None:
                row_set.add(r)
                col_set.add(c)
        if row_set and col_set:
            geom = ConnectorGeometry(rows=max(row_set), cols=max(col_set))
            for label, pin in conn.pins.items():
                r, c = _parse_pin_row_col(label)
                if r is not None and c is not None:
                    geom.cavities[(r, c)] = label
                    pin.row = r
                    pin.col = c
            conn.geometry = geom

    if conn.geometry is None:
        return f"Connector {conn.connector_id} (no geometry/pins)\n"

    g = conn.geometry
    lines: List[str] = []
    lines.append(f"Connector {conn.connector_id} — Face View")

    border = "    +" + ("-----------" * g.cols) + "+"
    lines.append(border)

    for r in range(1, g.rows + 1):
        row_cells: List[str] = []
        for c in range(1, g.cols + 1):
            label = g.cavities.get((r, c))
            if label and label in conn.pins:
                pin = conn.pins[label]
                color_code = (pin.color_primary or "").upper()
                emo = legend.get(color_code, "⬜")
                cell = f"[{emo}{label:>3}]"
            elif label:
                cell = f"[⬜{label:>3}]"
            else:
                cell = "[       ]"
            row_cells.append(cell)
        lines.append(f" R{r:02d} | " + " ".join(row_cells) + " |")

    lines.append(border)
    lines.append("")
    lines.append("Pins:")
    for label, pin in sorted(conn.pins.items(), key=lambda kv: kv[0]):
        color = ""
        if pin.color_primary and pin.color_secondary:
            color = f"{pin.color_primary}/{pin.color_secondary}"
        elif pin.color_primary:
            color = pin.color_primary
        elif pin.color_secondary:
            color = pin.color_secondary
        lines.append(f"  {label:>4}: {color:<7} - {pin.function or ''}")

    return "\n".join(lines)


def render_harness_ascii(harness: Harness, legend: Optional[Dict[str, str]] = None) -> str:
    lines: List[str] = []
    lines.append(f"Harness {harness.harness_id}")
    lines.append("=" * 40)
    lines.append("Nets:")

    for net in sorted(harness.nets, key=lambda n: n.net_id):
        color = net.color_primary or "??"
        emo = legend.get(color.upper(), "⬜") if legend else ""
        lines.append(
            f"  {net.net_id}: {net.from_connector}.{net.from_pin} → {net.to_connector}.{net.to_pin} "
            f"[{emo}{color}, {net.awg}AWG, {net.category}]"
        )

    lines.append("\nLoads:")
    for load_id, load in sorted(harness.loads.items()):
        lines.append(
            f"  {load_id}: {load.description} ({load.continuous_current_a}A cont / "
            f"{load.peak_current_a}A peak) @ {load.location or '?'} pri={load.priority or '?'}"
        )

    return "\n".join(lines)


# =========================
# 7. UpfitSkillAgent
# =========================

class UpfitSkillAgent:
    def __init__(self, rules: Optional[List[Rule]] = None):
        self.rule_engine = RuleEngine(rules or [])

    def ingest_pdf(self, pdf_path: str) -> Tuple[GLHDocument, Dict[str, List[ConnectorMention]]]:
        blocks = extract_text_blocks_from_pdf(pdf_path)
        index = build_connector_index(blocks)
        doc = GLHDocument()
        fuse_connectors(doc, index, pdf_path)
        return doc, index

    def ingest_glh_text(self, glh_text: str) -> GLHDocument:
        return parse_glh_blocks(glh_text)

    def merge_pdf_and_glh(self, pdf_path: str, glh_text: str) -> GLHDocument:
        blocks = extract_text_blocks_from_pdf(pdf_path)
        index = build_connector_index(blocks)
        doc = parse_glh_blocks(glh_text)
        fuse_connectors(doc, index, pdf_path)
        return doc

    def lint(self, doc: GLHDocument) -> List[RuleViolation]:
        return self.rule_engine.run_all(doc)


# =========================
# 8. Simple example runner
# =========================

def _build_demo_doc() -> GLHDocument:
    glh_seed = """
```legend
RD: 🔴
BK: ⚫
GN: 🟢
YE: 🟡
WH: ⚪
```

```connector
id=C2001
description: Front bumper harness upfit connector
location: Front bumper LH
rows: 2
cols: 7

A1: RD/WH, Fog lamp feed
A2: BK, Ground
B1: GN, Micron grill flasher +
B2: BK/WH, Micron grill flasher -
```

```harness
id=FRONT_BUMPER

net N1: C2001.A1 -> LOAD.FOG_LEFT, 18AWG, upfit
net N2: C2001.A2 -> GND.CHASSIS, 16AWG, oem
net N3: C2001.B1 -> LOAD.GRILL_FLASHER_POS, 20AWG, upfit
net N4: C2001.B2 -> GND.CHASSIS, 20AWG, upfit

load FOG_LEFT: "Left fog lamp", 4A, 8A_peak, bumper LH, priority=2
load GRILL_FLASHER_POS: "Grill flasher positive", 2A, 5A_peak, grill center
```
"""
    return parse_glh_blocks(glh_seed)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="GLH demo pipeline")
    parser.add_argument("pdf", nargs="?", help="Optional PDF to ingest")
    parser.add_argument("--pdf-debug", action="store_true", help="Dissect PDF page primitives")
    parser.add_argument("--debug-page", type=int, default=1, help="Page number to debug when --pdf-debug is set")
    args = parser.parse_args(argv)

    doc = _build_demo_doc()

    print(render_connector_ascii(doc.connectors["C2001"], doc.legend))
    harness = doc.harnesses["FRONT_BUMPER"]
    print("\n" + render_harness_ascii(harness, doc.legend))

    rules = [
        Rule("AWG_CURRENT", "AWG must support load current", "error", "SAE"),
        Rule("CAN_POWER", "No power on CAN lines", "error", "OEM"),
    ]
    agent = UpfitSkillAgent(rules)
    violations = agent.lint(doc)
    if violations:
        print("\nViolations:")
        for v in violations:
            print(f"  [{v.severity}] {v.rule_id}: {v.message}")
    else:
        print("\nLint: No violations.")

    if args.pdf:
        try:
            pdf_doc, index = agent.ingest_pdf(args.pdf)
            print(f"\nIngested {len(pdf_doc.connectors)} connectors from PDF {args.pdf}")
            print(f"Index keys: {sorted(index.keys())[:5]}{'...' if len(index) > 5 else ''}")
            if args.pdf_debug:
                primitives, info = dissect_pdf_page(args.pdf, args.debug_page)
                print("\nPDF structure summary:")
                print(summarize_pdf_primitives(primitives, info))
        except Exception as exc:  # pragma: no cover - demo path
            print(f"PDF ingest skipped/failed: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
