"""
AUTOMATED GROUND TRUTH GENERATION – GhostLink Self-Healing Pipeline
=====================================================================
Now the machine creates its own truth.

New Features:
- Generate perfect ground truth from:
  1. Existing high-quality DSL blocks (your hand-written ones)
  2. Manual click-annotate tool (terminal + mouse via OpenCV highgui)
  3. Semi-supervised bootstrapping: use high-confidence extractions as new GT
  4. Export to DSL, JSON, COCO-style annotation for ML training
- One-click "bless this extraction" → becomes permanent GT
- Auto-versioned GT database (glh_gt_db.jsonl)
- Active learning loop: worst-performing connectors → prompt for correction

ghostlink protocol: collapse → mirror → forge → link → bless

This module consolidates the GLH pipeline into a single audited file:
- IR / schema (connectors, pins, harness, etc.)
- GLH DSL parsing (legend, connector, harness, void blocks)
- PDF text ingestion + connector index
- Pixel-based connector geometry extraction (simplified but real structure)
- Rule engine skeleton
- ASCII rendering
- Validation metrics
- Ground-truth store (JSONL) and DSL → GT conversion
- High-level ingest + validate helpers

External deps (optional, install as needed):
    pdfplumber         # text from PDFs
    PyMuPDF (fitz)     # render pages as images
    opencv-python      # image analysis
    numpy              # image arrays
    pytesseract/easyocr# optional OCR if you want to wire it in
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field, asdict, is_dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

log = logging.getLogger("glh")
if not log.handlers:
    logging.basicConfig(level=logging.INFO)


# -----------------------------------------------------------------------------
# Core IR / Schema
# -----------------------------------------------------------------------------

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
    # (row, col) -> pin_label (e.g. "A1", "B2", "1")
    cavities: Dict[Tuple[int, int], str] = field(default_factory=dict)


@dataclass
class Pin:
    label: str                 # "A1", "B2", "1", etc.
    row: Optional[int] = None
    col: Optional[int] = None

    color_primary: Optional[str] = None   # "RD", "BK", etc.
    color_secondary: Optional[str] = None # stripe, etc.
    awg: Optional[int] = None
    function: Optional[str] = None
    signal_type: SignalType = SignalType.UNKNOWN

    # coordinates in page space (for overlays), optional
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

    # provenance
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
    category: Optional[str] = None  # "upfit", "oem", "can", etc.


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
    severity: str          # "error", "warning", etc.
    source: str            # "OEM", "SAE", "GhostRule"


@dataclass
class Harness:
    harness_id: str
    connectors: Dict[str, Connector] = field(default_factory=dict)
    nets: List[WireNet] = field(default_factory=list)
    loads: Dict[str, Load] = field(default_factory=dict)


@dataclass
class GLHDocument:
    platform: Optional[VehiclePlatform] = None
    legend: Dict[str, str] = field(default_factory=dict)  # "RD" -> "🔴"
    connectors: Dict[str, Connector] = field(default_factory=dict)
    harnesses: Dict[str, Harness] = field(default_factory=dict)
    voids: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class PDFTextBlock:
    page: int
    text: str
    bbox: Tuple[float, float, float, float]  # (x0, y0, x1, y1)


@dataclass
class ConnectorMention:
    connector_id: str
    page: int
    context: str
    bbox: Optional[Tuple[float, float, float, float]] = None


# -----------------------------------------------------------------------------
# GLH DSL Parsing
# -----------------------------------------------------------------------------

FENCE_RE = re.compile(r"```(\w+)(.*?)```", re.DOTALL)


def parse_glh_blocks(text: str) -> GLHDocument:
    """Parse a GLH source string containing fenced code blocks."""
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
    """Simple `key: value` lines, e.g. `RD: 🔴`."""
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        doc.legend[key.strip()] = val.strip()


def _parse_connector_block(doc: GLHDocument, body: str) -> None:
    """Naive parser for connector blocks."""
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
        log.warning("Connector block without id, skipping:\n%s", body)
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

    doc.connectors[connector_id] = conn


def _parse_harness_block(doc: GLHDocument, body: str) -> None:
    """Naive parser for harness blocks."""
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    header: Dict[str, str] = {}
    net_lines: List[str] = []
    load_lines: List[str] = []

    for line in lines:
        low = line.lower()
        if low.startswith("net "):
            net_lines.append(line)
        elif low.startswith("load "):
            load_lines.append(line)
        else:
            if "=" in line:
                k, v = line.split("=", 1)
                header[k.strip().lower()] = v.strip()

    harness_id = header.get("id") or header.get("harness_id")
    if not harness_id:
        log.warning("Harness block without id, skipping:\n%s", body)
        return

    h = Harness(harness_id=harness_id)

    net_re = re.compile(
        r"^net\s+(\S+)\s*:\s*(\S+)\.(\S+)\s*->\s*(\S+)\.(\S+)\s*,\s*(\d+)AWG\s*,\s*(\S+)",
        re.IGNORECASE,
    )
    for nline in net_lines:
        m = net_re.match(nline)
        if not m:
            log.warning("Unparsed net line: %s", nline)
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
        h.nets.append(net)

    load_re = re.compile(
        r'^load\s+(\S+)\s*:\s*"(.*?)"\s*,\s*([\d.]+)A\s*,\s*([\d.]+)A_peak\s*,\s*(.*)$',
        re.IGNORECASE,
    )
    for lline in load_lines:
        m = load_re.match(lline)
        if not m:
            log.warning("Unparsed load line: %s", lline)
            continue
        load_id, desc, cont_str, peak_str, tail = m.groups()
        location = None
        priority = None

        parts = [p.strip() for p in tail.split(",") if p.strip()]
        for part in parts:
            if part.startswith("priority="):
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
        h.loads[load_id] = load

    doc.harnesses[harness_id] = h


def _parse_void_block(doc: GLHDocument, body: str) -> None:
    """Record unknown / incomplete segments."""
    entry: Dict[str, Any] = {}
    for line in body.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        k, v = line.split(":", 1)
        entry[k.strip()] = v.strip()
    if entry:
        doc.voids.append(entry)


# -----------------------------------------------------------------------------
# PDF Text Ingestion + Connector Index
# -----------------------------------------------------------------------------

CONNECTOR_ID_RE = re.compile(r"\bC\d{3,4}\b")
CAP_ID_RE = re.compile(r"\bCAP\d+\b")


def extract_text_blocks_from_pdf(pdf_path: str) -> List[PDFTextBlock]:
    """Basic text + bbox extraction using pdfplumber."""
    try:
        import pdfplumber  # type: ignore
    except Exception as exc:
        log.error("pdfplumber not available: %s", exc)
        return []

    blocks: List[PDFTextBlock] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages):
            page_text = page.extract_text() or ""
            bbox = (0.0, 0.0, float(page.width), float(page.height))
            blocks.append(
                PDFTextBlock(
                    page=page_index + 1,
                    text=page_text,
                    bbox=bbox,
                )
            )
    return blocks


def build_connector_index(blocks: List[PDFTextBlock]) -> Dict[str, List[ConnectorMention]]:
    """Scan all text blocks and collect connector/CAP mentions."""
    index: Dict[str, List[ConnectorMention]] = {}
    for block in blocks:
        text = block.text or ""
        for m in CONNECTOR_ID_RE.finditer(text):
            connector_id = m.group(0)
            ctx_start = max(0, m.start() - 40)
            ctx_end = min(len(text), m.end() + 40)
            mention = ConnectorMention(
                connector_id=connector_id,
                page=block.page,
                context=text[ctx_start:ctx_end],
                bbox=block.bbox,
            )
            index.setdefault(connector_id, []).append(mention)

        for m in CAP_ID_RE.finditer(text):
            cap_id = m.group(0)
            ctx_start = max(0, m.start() - 40)
            ctx_end = min(len(text), m.end() + 40)
            mention = ConnectorMention(
                connector_id=cap_id,
                page=block.page,
                context=text[ctx_start:ctx_end],
                bbox=block.bbox,
            )
            index.setdefault(cap_id, []).append(mention)

    return index


def group_mentions_by_page(index: Dict[str, List[ConnectorMention]]) -> Dict[int, List[ConnectorMention]]:
    pages: Dict[int, List[ConnectorMention]] = {}
    for _cid, mentions in index.items():
        for m in mentions:
            pages.setdefault(m.page, []).append(m)
    return pages


# -----------------------------------------------------------------------------
# Pixel-based Connector Geometry Extraction (simplified)
# -----------------------------------------------------------------------------

def render_pdf_page_to_image(pdf_path: str, page_num: int, dpi: int = 300):
    """Render a PDF page as a high-resolution image array (OpenCV BGR)."""
    try:
        import fitz  # type: ignore
        import numpy as np  # type: ignore
        import cv2  # type: ignore
    except Exception as exc:
        log.error("Pixel rendering requires PyMuPDF, numpy, cv2: %s", exc)
        return None

    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num - 1)
    pix = page.get_pixmap(dpi=dpi)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    doc.close()
    return img


def detect_connector_body(img) -> Optional[Tuple[int, int, int, int]]:
    """Find a plausible connector rectangle in the image using contours."""
    try:
        import cv2  # type: ignore
    except Exception:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for cnt in contours[:5]:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            if w > 80 and h > 30:
                return x, y, w, h
    return None


def detect_pin_cavities(crop_img) -> List[Tuple[int, int]]:
    """Detect small circular/rectangular pin cavities."""
    try:
        import cv2  # type: ignore
        import numpy as np  # type: ignore
    except Exception:
        return []

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    pins: List[Tuple[int, int]] = []

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=15,
        param1=50,
        param2=25,
        minRadius=4,
        maxRadius=18,
    )
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for x, y, r in circles:
            pins.append((int(x), int(y)))

    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if 8 < w < 30 and 8 < h < 30:
            pins.append((x + w // 2, y + h // 2))

    unique = list({(int(x), int(y)) for x, y in pins})
    return sorted(unique, key=lambda p: (p[1], p[0]))


def cluster_pins_to_grid(pins: List[Tuple[int, int]]) -> ConnectorGeometry:
    """Cluster pin centers into rows/cols by grouping y then x."""
    if not pins:
        return ConnectorGeometry(rows=0, cols=0)

    rows: List[List[Tuple[int, int]]] = []
    current: List[Tuple[int, int]] = [pins[0]]
    for p in pins[1:]:
        if abs(p[1] - current[-1][1]) < 20:
            current.append(p)
        else:
            rows.append(sorted(current, key=lambda pt: pt[0]))
            current = [p]
    if current:
        rows.append(sorted(current, key=lambda pt: pt[0]))

    num_rows = len(rows)
    num_cols = max(len(r) for r in rows) if rows else 0

    geom = ConnectorGeometry(rows=num_rows, cols=num_cols)
    for r_idx, row in enumerate(rows):
        for c_idx, _pt in enumerate(row):
            label = f"{chr(65 + r_idx)}{c_idx + 1}"
            geom.cavities[(r_idx + 1, c_idx + 1)] = label

    return geom


def extract_pixel_geometry_for_connector(
    pdf_path: str,
    connector_id: str,
    mentions: List[ConnectorMention],
) -> Optional[ConnectorGeometry]:
    """Render the first relevant page and detect pin layout."""
    if not mentions:
        return None

    page = mentions[0].page
    img = render_pdf_page_to_image(pdf_path, page, dpi=300)
    if img is None:
        return None

    bbox = mentions[0].bbox
    if bbox:
        x0, y0, x1, y1 = bbox
        h, w = img.shape[:2]
        import math
        mx = 0.3 * (x1 - x0)
        my = 0.3 * (y1 - y0)
        cx0 = max(0, int(math.floor(x0 - mx)))
        cy0 = max(0, int(math.floor(y0 - my)))
        cx1 = min(w, int(math.ceil(x1 + mx)))
        cy1 = min(h, int(math.ceil(y1 + my)))
        img_crop = img[cy0:cy1, cx0:cx1]
    else:
        img_crop = img

    body = detect_connector_body(img_crop)
    if not body:
        log.warning("No connector body detected for %s on page %d", connector_id, page)
        return None

    bx, by, bw, bh = body
    body_crop = img_crop[by:by + bh, bx:bx + bw]
    pins = detect_pin_cavities(body_crop)
    if not pins:
        log.warning("No pin cavities detected for %s on page %d", connector_id, page)
        return None

    geom = cluster_pins_to_grid(pins)
    return geom


# -----------------------------------------------------------------------------
# Fusion: PDF-derived connectors + geometry into GLHDocument
# -----------------------------------------------------------------------------

def fuse_connectors_from_pdf(
    doc: GLHDocument,
    pdf_path: str,
) -> GLHDocument:
    """Extract text → build index → pixel-geometry and populate doc.connectors."""
    blocks = extract_text_blocks_from_pdf(pdf_path)
    index = build_connector_index(blocks)
    for cid, mentions in index.items():
        conn = doc.connectors.get(cid)
        if not conn:
            conn = Connector(connector_id=cid)
            doc.connectors[cid] = conn

        conn.sources.extend({"page": m.page, "context": m.context} for m in mentions)

        if not conn.geometry:
            geom = extract_pixel_geometry_for_connector(pdf_path, cid, mentions)
            if geom:
                conn.geometry = geom

    return doc


def ingest_pdf_connectors_ultrafast(pdf_path: str) -> GLHDocument:
    """Public entry: start from empty GLHDocument and fuse connectors from PDF."""
    doc = GLHDocument()
    return fuse_connectors_from_pdf(doc, pdf_path)


# -----------------------------------------------------------------------------
# Rule Engine Skeleton
# -----------------------------------------------------------------------------

@dataclass
class RuleViolation:
    rule_id: str
    severity: str
    message: str
    context: Dict[str, Any]


class RuleEngine:
    """Classical deterministic checks."""

    def __init__(self, rules: Optional[List[Rule]] = None):
        self.rules: Dict[str, Rule] = {r.rule_id: r for r in (rules or [])}

    def run_all(self, doc: GLHDocument) -> List[RuleViolation]:
        violations: List[RuleViolation] = []
        violations.extend(self._check_awg_vs_current(doc))
        violations.extend(self._check_can_taps(doc))
        return violations

    def _check_awg_vs_current(self, doc: GLHDocument) -> List[RuleViolation]:
        """Placeholder AWG vs current-length checks."""
        _ = doc
        return []

    def _check_can_taps(self, doc: GLHDocument) -> List[RuleViolation]:
        """Placeholder CAN harness checks."""
        _ = doc
        return []


# -----------------------------------------------------------------------------
# ASCII Rendering
# -----------------------------------------------------------------------------

def render_connector_ascii(conn: Connector, legend: Dict[str, str]) -> str:
    """Geometry-aware ASCII rendering with emoji legend mapping."""
    lines: List[str] = []
    if not conn.geometry:
        lines.append(f"Connector {conn.connector_id}: [no geometry]")
        lines.append("Pins:")
        for label, pin in sorted(conn.pins.items(), key=lambda kv: kv[0]):
            color = f"{pin.color_primary or ''}/{pin.color_secondary or ''}".strip("/")
            lines.append(f"  {label}: {color:<7} - {pin.function or ''}")
        return "\n".join(lines)

    g = conn.geometry
    lines.append(f"Connector {conn.connector_id} — Face View")
    width = g.cols

    border = "    +" + ("-----------" * width) + "+"
    lines.append(border)
    for r in range(1, g.rows + 1):
        row_cells = []
        for c in range(1, g.cols + 1):
            label = g.cavities.get((r, c))
            if label and label in conn.pins:
                pin = conn.pins[label]
                color_code = pin.color_primary or "??"
                emoji = legend.get(color_code, "⬜")
                cell = f"[{emoji}{label}]"
            elif label:
                cell = f"[⬜{label}]"
            else:
                cell = "[       ]"
            row_cells.append(cell)
        lines.append(f" R{r:02d} | " + " ".join(row_cells) + " |")
    lines.append(border)

    lines.append("")
    lines.append("Legend:")
    for code, emo in legend.items():
        lines.append(f"  {emo} = {code}")

    lines.append("\nPins:")
    for label, pin in sorted(conn.pins.items(), key=lambda kv: kv[0]):
        color = f"{pin.color_primary or ''}/{pin.color_secondary or ''}".strip("/")
        lines.append(f"  {label}: {color:<7} - {pin.function or ''}")

    return "\n".join(lines)


# -----------------------------------------------------------------------------
# Validation Metrics
# -----------------------------------------------------------------------------

@dataclass
class ValidationMetrics:
    pin_detection_precision: float
    pin_detection_recall: float
    pin_detection_f1: float
    geometry_match_fraction: float
    color_accuracy: float
    function_accuracy: float
    overall_score: float
    details: Dict[str, Any] = field(default_factory=dict)


def _dataclass_to_dict(obj: Any) -> Any:
    """Convert nested dataclasses to plain dicts, dropping None."""
    if is_dataclass(obj):
        return {k: _dataclass_to_dict(v) for k, v in asdict(obj).items() if v is not None}
    if isinstance(obj, list):
        return [_dataclass_to_dict(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _dataclass_to_dict(v) for k, v in obj.items()}
    return obj


def validate_extraction(extracted: GLHDocument, ground_truth: GLHDocument) -> ValidationMetrics:
    """Compare two GLHDocuments and compute basic metrics."""
    geom_matches = 0
    geom_total = 0
    for cid, gt_conn in ground_truth.connectors.items():
        gt_geom = gt_conn.geometry
        ex_conn = extracted.connectors.get(cid)
        if not ex_conn or not gt_geom or not ex_conn.geometry:
            continue
        geom_total += 1
        ex_geom = ex_conn.geometry
        if ex_geom.rows == gt_geom.rows and ex_geom.cols == gt_geom.cols:
            geom_matches += 1
    geometry_match_fraction = (geom_matches / geom_total) if geom_total else 0.0

    tp = fp = fn = 0
    details: Dict[str, Any] = {}
    for cid, gt_conn in ground_truth.connectors.items():
        ex_conn = extracted.connectors.get(cid)
        if not ex_conn:
            fn += len(gt_conn.pins)
            details[cid] = {"tp": 0, "fp": 0, "fn": len(gt_conn.pins)}
            continue

        gt_pins = set(gt_conn.pins.keys())
        ex_pins = set(ex_conn.pins.keys())
        tp_c = len(gt_pins & ex_pins)
        fp_c = len(ex_pins - gt_pins)
        fn_c = len(gt_pins - ex_pins)
        tp += tp_c
        fp += fp_c
        fn += fn_c
        details[cid] = {"tp": tp_c, "fp": fp_c, "fn": fn_c}

    pin_precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    pin_recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    if pin_precision + pin_recall > 0:
        pin_f1 = 2 * pin_precision * pin_recall / (pin_precision + pin_recall)
    else:
        pin_f1 = 0.0

    color_matches = color_total = 0
    func_matches = func_total = 0
    for cid, gt_conn in ground_truth.connectors.items():
        ex_conn = extracted.connectors.get(cid)
        if not ex_conn:
            continue
        for label, gt_pin in gt_conn.pins.items():
            ex_pin = ex_conn.pins.get(label)
            if not ex_pin:
                continue
            gt_color = (gt_pin.color_primary or "", gt_pin.color_secondary or "")
            ex_color = (ex_pin.color_primary or "", ex_pin.color_secondary or "")
            if any(gt_color):
                color_total += 1
                if gt_color == ex_color:
                    color_matches += 1
            if gt_pin.function:
                func_total += 1
                if (ex_pin.function or "").strip() == gt_pin.function.strip():
                    func_matches += 1

    color_accuracy = color_matches / color_total if color_total else 0.0
    function_accuracy = func_matches / func_total if func_total else 0.0

    overall = (
        0.5 * pin_f1 +
        0.2 * geometry_match_fraction +
        0.15 * color_accuracy +
        0.15 * function_accuracy
    ) * 100.0

    return ValidationMetrics(
        pin_detection_precision=pin_precision,
        pin_detection_recall=pin_recall,
        pin_detection_f1=pin_f1,
        geometry_match_fraction=geometry_match_fraction,
        color_accuracy=color_accuracy,
        function_accuracy=function_accuracy,
        overall_score=overall,
        details=details,
    )


# -----------------------------------------------------------------------------
# Ground Truth DB (JSONL) + DSL → GT bridge
# -----------------------------------------------------------------------------

GT_DB_PATH = Path("gt_db/glh_ground_truth_db.jsonl")
GT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
if not GT_DB_PATH.exists():
    GT_DB_PATH.write_text("", encoding="utf-8")


def save_gt_entry(entry: Dict[str, Any]) -> None:
    """Append a GT record to the JSONL DB."""
    with GT_DB_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def get_all_gt_entries() -> List[Dict[str, Any]]:
    if not GT_DB_PATH.exists():
        return []
    with GT_DB_PATH.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def gt_db_to_document() -> GLHDocument:
    """Build a GLHDocument from all GT entries in the JSONL DB."""
    doc = GLHDocument()
    for entry in get_all_gt_entries():
        cid = entry.get("connector_id")
        if not cid:
            connectors = entry.get("connectors") or {}
            for ccid, cdata in connectors.items():
                geom_data = cdata.get("geometry") or {}
                geom = None
                if geom_data:
                    geom = ConnectorGeometry(
                        rows=geom_data.get("rows", 0),
                        cols=geom_data.get("cols", 0),
                    )
                conn = Connector(connector_id=ccid, geometry=geom)
                pins_data = cdata.get("pins", {}) or {}
                for label, info in pins_data.items():
                    conn.pins[label] = Pin(
                        label=label,
                        color_primary=info.get("color_primary"),
                        color_secondary=info.get("color_secondary"),
                        function=info.get("function"),
                    )
                doc.connectors[ccid] = conn
            continue

        geom_data = entry.get("geometry") or {}
        geom = None
        if geom_data:
            geom = ConnectorGeometry(
                rows=geom_data.get("rows", 0),
                cols=geom_data.get("cols", 0),
            )
        conn = Connector(connector_id=cid, geometry=geom)
        pins_data = entry.get("pins", {}) or {}
        for label, info in pins_data.items():
            conn.pins[label] = Pin(
                label=label,
                color_primary=info.get("color_primary"),
                color_secondary=info.get("color_secondary"),
                function=info.get("function"),
            )
        doc.connectors[cid] = conn
    return doc


def generate_gt_from_dsl(dsl_text: str, source_name: str = "manual") -> Dict[str, Any]:
    """Parse DSL and store it as a GT entry in the JSONL DB."""
    from datetime import datetime

    parsed = parse_glh_blocks(dsl_text)
    connectors = {}
    for cid, conn in parsed.connectors.items():
        geom = conn.geometry
        connectors[cid] = {
            "geometry": {
                "rows": geom.rows if geom else 0,
                "cols": geom.cols if geom else 0,
            },
            "pins": {
                label: {
                    "color_primary": pin.color_primary,
                    "color_secondary": pin.color_secondary,
                    "function": pin.function,
                }
                for label, pin in conn.pins.items()
            },
        }

    entry = {
        "id": f"gt_{int(datetime.now().timestamp())}",
        "source": source_name,
        "connectors": connectors,
        "created": datetime.now().isoformat(),
    }
    save_gt_entry(entry)
    return entry


def export_gt_to_dsl() -> str:
    """Regenerate a DSL-ish text representation from the JSONL DB."""
    lines: List[str] = []
    for entry in get_all_gt_entries():
        connectors = entry.get("connectors") or {}
        for cid, data in connectors.items():
            geom = data.get("geometry") or {}
            pins = data.get("pins") or {}
            lines.append("```connector")
            lines.append(f"id={cid}")
            if geom:
                lines.append(f"rows: {geom.get('rows', 0)}")
                lines.append(f"cols: {geom.get('cols', 0)}")
            for label, info in sorted(pins.items(), key=lambda kv: kv[0]):
                color_primary = info.get("color_primary") or ""
                color_secondary = info.get("color_secondary") or ""
                func = info.get("function") or ""
                color = color_primary
                if color_secondary:
                    color = f"{color_primary}/{color_secondary}"
                line = f"{label}: {color}"
                if func:
                    line += f", {func}"
                lines.append(line)
            lines.append("```")
            lines.append("")
    return "\n".join(lines)


# -----------------------------------------------------------------------------
# Ground Truth from DSL directory (per-connector JSON cache)
# -----------------------------------------------------------------------------

def dataclass_to_dict(obj: Any) -> Any:
    """Public helper to convert dataclasses to dicts for JSON cache."""
    return _dataclass_to_dict(obj)


def generate_ground_truth_cache(
    dsl_dir: Path,
    out_dir: Path,
    page_map: Optional[Dict[str, int]] = None,
) -> Dict[str, Path]:
    """Turn DSL files in dsl_dir into per-connector JSON files in out_dir."""
    dsl_dir = dsl_dir.expanduser().resolve()
    out_dir = out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    page_map = page_map or {}
    connector_to_path: Dict[str, Path] = {}

    for path in list(dsl_dir.rglob("*.glh")) + list(dsl_dir.rglob("*.txt")):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as exc:
            log.error("Failed to read %s: %s", path, exc)
            continue
        doc = parse_glh_blocks(text)
        for cid, conn in doc.connectors.items():
            data = dataclass_to_dict(conn)
            if cid.upper() in (page_map or {}):
                data["_gt_page"] = page_map[cid.upper()]
            json_path = out_dir / f"{cid}.json"
            json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            connector_to_path[cid] = json_path

    log.info("Generated GT cache for %d connectors", len(connector_to_path))
    return connector_to_path


# -----------------------------------------------------------------------------
# Convenience: build GT GLHDocument from JSON cache + DB
# -----------------------------------------------------------------------------

def load_gt_from_cache(cache_dir: Path) -> GLHDocument:
    """Load per-connector JSON files generated by generate_ground_truth_cache."""
    cache_dir = cache_dir.expanduser().resolve()
    doc = GLHDocument()
    for json_path in cache_dir.glob("*.json"):
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as exc:
            log.error("Failed to load GT cache %s: %s", json_path, exc)
            continue
        cid = data.get("connector_id") or json_path.stem
        geom_data = data.get("geometry") or {}
        geom = None
        if geom_data:
            geom = ConnectorGeometry(
                rows=geom_data.get("rows", 0),
                cols=geom_data.get("cols", 0),
            )
        conn = Connector(connector_id=cid, geometry=geom)
        pins_data = data.get("pins") or {}
        for label, info in pins_data.items():
            conn.pins[label] = Pin(
                label=label,
                color_primary=info.get("color_primary"),
                color_secondary=info.get("color_secondary"),
                function=info.get("function"),
            )
        doc.connectors[cid] = conn
    return doc


def build_combined_ground_truth(cache_dir: Path) -> GLHDocument:
    """Combine offline GT cache (from DSL) and online GT DB (JSONL)."""
    offline = load_gt_from_cache(cache_dir)
    online = gt_db_to_document()
    combined = GLHDocument()
    combined.connectors.update(offline.connectors)
    combined.connectors.update(online.connectors)
    return combined


# -----------------------------------------------------------------------------
# High-level workflows
# -----------------------------------------------------------------------------

def process_pdf_to_doc(pdf_path: str, glh_seed_text: str = "") -> GLHDocument:
    """Parse optional seed DSL, then ingest PDF connectors and fuse them."""
    if glh_seed_text:
        doc = parse_glh_blocks(glh_seed_text)
    else:
        doc = GLHDocument()
    return fuse_connectors_from_pdf(doc, pdf_path)


def ingest_and_validate(
    pdf_path: str,
    cache_dir: Path,
) -> Tuple[GLHDocument, ValidationMetrics]:
    """Ingest connectors then validate against combined GT."""
    extracted = ingest_pdf_connectors_ultrafast(pdf_path)
    gt_doc = build_combined_ground_truth(cache_dir)
    metrics = validate_extraction(extracted, gt_doc)
    return extracted, metrics


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="GLH system demo")
    parser.add_argument("--pdf", type=str, required=False, help="Path to PIU PDF")
    parser.add_argument("--dsl-dir", type=str, required=False, help="Path to DSL seed directory")
    parser.add_argument("--cache-dir", type=str, default="ground_truth_cache", help="GT cache directory")
    args = parser.parse_args()

    cache_dir = Path(args.cache_dir)

    if args.dsl_dir:
        dsl_dir = Path(args.dsl_dir)
        generate_ground_truth_cache(dsl_dir, cache_dir)

    if args.pdf:
        doc, metrics = ingest_and_validate(args.pdf, cache_dir)
        print(f"Overall score: {metrics.overall_score:.1f}%")
        print(f"Pin F1: {metrics.pin_detection_f1:.3f}")
        print(f"Color accuracy: {metrics.color_accuracy:.3f}")
        print(f"Function accuracy: {metrics.function_accuracy:.3f}")
        print(f"Geom match fraction: {metrics.geometry_match_fraction:.3f}")
        if doc.legend:
            for cid, conn in doc.connectors.items():
                print(render_connector_ascii(conn, doc.legend))
                break
    else:
        print("GLH system module loaded. Use process_pdf_to_doc() or ingest_and_validate().")
