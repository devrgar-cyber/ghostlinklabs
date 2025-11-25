"""
GhostLink Harness (GLH) – Upfitter Brain Pipeline
=================================================

Pipeline:

1. PDF ingestion (text + vector + pixel stubs)
2. Connector index (Cxxxx, CAPxx, etc.)
3. DSL parsing for GLH blocks (connector, harness, legend, void)
4. Fusion into a unified IR
5. Netlist graph + rule engine + constraint solver hooks
6. ASCII + PDF overlay renderers
7. UpfitSkillAgent orchestration hooks

This is a skeleton: some parts are fully implemented,
others are stubs with explicit TODOs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
import argparse
import sys
import time
import importlib.util
import logging
import re

# Optional libs (install when you’re ready):
# pdfplumber, fitz (PyMuPDF), networkx, z3-solver, opencv-python, pytesseract


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("glh")


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
    # maps (row, col) -> pin_label (e.g., "A1", "1", "B7")
    cavities: Dict[Tuple[int, int], str] = field(default_factory=dict)


@dataclass
class Pin:
    label: str  # "A1", "1", "B7", etc.
    row: Optional[int] = None
    col: Optional[int] = None

    color_primary: Optional[str] = None  # "RD", "BK", etc.
    color_secondary: Optional[str] = None  # stripe, etc.
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

    # Source provenance (pages, pdf, etc.)
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
    severity: str  # "error", "warning", etc.
    source: str  # "OEM", "SAE", "GhostRule"
    # The condition is implemented in code (see RuleEngine).
    # You can reference rule_id in a registry.


@dataclass
class Harness:
    harness_id: str
    connectors: Dict[str, Connector] = field(default_factory=dict)
    nets: List[WireNet] = field(default_factory=list)
    loads: Dict[str, Load] = field(default_factory=dict)


@dataclass
class GLHDocument:
    platform: Optional[VehiclePlatform] = None
    legend: Dict[str, str] = field(default_factory=dict)  # e.g. "RD" -> "🔴"
    connectors: Dict[str, Connector] = field(default_factory=dict)
    harnesses: Dict[str, Harness] = field(default_factory=dict)
    voids: List[Dict[str, Any]] = field(default_factory=list)  # unknowns/holes


# -----------------------------------------------------------------------------
# DSL Parsing (```connector```, ```harness```, ```legend```, ```void```)
# -----------------------------------------------------------------------------

FENCE_RE = re.compile(r"```(\w+)(.*?)```", re.DOTALL)


def parse_glh_blocks(text: str) -> GLHDocument:
    """
    Parse a GLH source string containing fenced code blocks like:

    ```legend
    RD: 🔴
    BK: ⚫
    ```

    ```connector id=C2001
    description: Front bumper harness connector
    rows: 2
    cols: 7
    A1: RD/WH, FOG_LAMP_FEED
    A2: BK, GROUND
    ...
    ```

    ```harness id=FRONT_BUMPER
    net N1: C2001.A1 -> LOAD.FOG_LEFT, 18AWG, upfit
    ...
    ```

    This is intentionally simple; you can tighten it later
    (YAML inside blocks, etc.).
    """
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
    """
    Simple `key: value` lines.

    Example:
      RD: 🔴
      BK: ⚫
    """
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        doc.legend[key.strip()] = val.strip()


def _parse_connector_block(doc: GLHDocument, body: str) -> None:
    """
    Naive parser for connector blocks.

    Expected structure example:

        id=C2001
        description: Front bumper harness connector
        location: Front bumper, LH
        rows: 2
        cols: 7

        A1: RD/WH, Fog lamp feed
        A2: BK, Ground
        B1: GN, Micron grill flasher +
        ...

    You can later upgrade this to YAML or JSON inside the block.
    """
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    header: Dict[str, str] = {}
    pin_lines: List[str] = []

    # First read header lines until we hit something that looks like a pin
    pin_pattern = re.compile(r"^[A-Z]?\d+[: ]")
    for line in lines:
        if pin_pattern.match(line):
            pin_lines.append(line)
        else:
            if "=" in line:
                k, v = line.split("=", 1)
                header[k.strip()] = v.strip()
            elif ":" in line:
                k, v = line.split(":", 1)
                header[k.strip()] = v.strip()
            else:
                # ignore / TODO
                pass

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
        # Example formats:
        #   A1: RD/WH, Fog lamp feed
        #   1: GN, CAN-High
        #   B7: BK/WH, GND
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
    """
    Naive parser for harness blocks.

    Example:

        id=FRONT_BUMPER

        # nets
        net N1: C2001.A1 -> LOAD.FOG_LEFT, 18AWG, upfit
        net N2: C2001.A2 -> GROUND.CHASSIS_LH, 16AWG, oem

        # loads
        load FOG_LEFT: "Left fog lamp", 4A, 8A_peak, bumper LH, priority=2
    """
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
                header[k.strip()] = v.strip()

    harness_id = header.get("id") or header.get("harness_id")
    if not harness_id:
        log.warning("Harness block without id, skipping:\n%s", body)
        return

    h = Harness(harness_id=harness_id)

    # Nets
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

    # Loads – simple format:
    #   load FOG_LEFT: "Left fog lamp", 4A, 8A_peak, bumper LH, priority=2
    load_re = re.compile(
        r"^load\s+(\S+)\s*:\s*\"(.*?)\"\s*,\s*([\d\.]+)A\s*,\s*([\d\.]+)A_peak\s*,\s*(.*)$",
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
        # quick parse of trailing location / priority= fields
        parts = [p.strip() for p in tail.split(",") if p.strip()]
        for part in parts:
            if part.startswith("priority="):
                priority = int(part.split("=", 1)[1])
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
    """
    `void` block = explicitly unknown / incomplete segment.

    Example:

        reason: unknown length between splice S1 and load FOG_LEFT
        segment: net N1
    """
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
# PDF Ingestion + Connector Index
# -----------------------------------------------------------------------------

CONNECTOR_ID_RE = re.compile(r"\bC\d{3,4}\b")
CAP_ID_RE = re.compile(r"\bCAP\d+\b")


def _pdfplumber_available() -> bool:
    return importlib.util.find_spec("pdfplumber") is not None


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


def extract_text_blocks_from_pdf(pdf_path: str) -> List[PDFTextBlock]:
    """
    Basic text + bbox extraction using pdfplumber.

    Install:
        pip install pdfplumber
    """
    if not _pdfplumber_available():
        raise ImportError("pdfplumber is required for PDF ingestion. Install it to enable extract_text_blocks_from_pdf().")

    import pdfplumber  # type: ignore

    blocks: List[PDFTextBlock] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages):
            # using words as smallest building blocks
            words = page.extract_words()
            if not words:
                continue
            # For now, we join entire page text as one block
            page_text = page.extract_text() or ""
            blocks.append(
                PDFTextBlock(
                    page=page_index + 1,
                    text=page_text,
                    bbox=(0.0, 0.0, float(page.width), float(page.height)),
                )
            )

    return blocks


def build_connector_index(blocks: List[PDFTextBlock]) -> Dict[str, List[ConnectorMention]]:
    """
    Scan all text blocks and collect connector mentions from text.
    """
    index: Dict[str, List[ConnectorMention]] = {}
    for block in blocks:
        # For each connector ID found in the text
        for m in CONNECTOR_ID_RE.finditer(block.text):
            connector_id = m.group(0)
            ctx_start = max(0, m.start() - 40)
            ctx_end = min(len(block.text), m.end() + 40)
            context = block.text[ctx_start:ctx_end]
            mention = ConnectorMention(
                connector_id=connector_id,
                page=block.page,
                context=context,
                bbox=block.bbox,
            )
            index.setdefault(connector_id, []).append(mention)

        for m in CAP_ID_RE.finditer(block.text):
            cap_id = m.group(0)
            ctx_start = max(0, m.start() - 40)
            ctx_end = min(len(block.text), m.end() + 40)
            context = block.text[ctx_start:ctx_end]
            mention = ConnectorMention(
                connector_id=cap_id,
                page=block.page,
                context=context,
                bbox=block.bbox,
            )
            index.setdefault(cap_id, []).append(mention)

    return index


# -----------------------------------------------------------------------------
# Vector / Pixel Connector Geometry Extraction (Stubs)
# -----------------------------------------------------------------------------


def extract_vector_geometry_for_connector(
    pdf_path: str,
    connector_id: str,
    mentions: List[ConnectorMention],
) -> Optional[ConnectorGeometry]:
    """
    Stub: use PyMuPDF or similar to inspect vector graphics on relevant pages.

    Steps you'd implement:

    1. Open PDF, go to `mentions[0].page`.
    2. Inspect the drawing layer for rectangles containing
       regular grids of small circles/rects (cavities).
    3. Cluster their centers into rows/cols.
    4. Optionally associate text labels near each cavity.

    Returns a ConnectorGeometry if found, else None.
    """
    # TODO: implement vector geometry detection with PyMuPDF / PDF operators.
    log.info(
        "extract_vector_geometry_for_connector: not yet implemented for %s",
        connector_id,
    )
    return None


def extract_pixel_geometry_for_connector(
    pdf_path: str,
    connector_id: str,
    mentions: List[ConnectorMention],
) -> Optional[ConnectorGeometry]:
    """
    Stub: pixel-level extraction using OpenCV + OCR.

    Idea:

    1. Render page as image (e.g., with PyMuPDF or pdf2image).
    2. Crop region around connector diagram using mention.bbox
       and/or heuristic from headings.
    3. Use OpenCV to:
       - find outer connector body rectangle
       - detect repeated cavities (circular/rectangular blobs)
       - cluster into rows/cols
    4. Use OCR (pytesseract) on small ROIs near each cavity
       to assign labels.
    """
    # TODO: implement pixel pipeline.
    log.info(
        "extract_pixel_geometry_for_connector: not yet implemented for %s",
        connector_id,
    )
    return None


# -----------------------------------------------------------------------------
# Fusion: PDF-derived connectors + DSL-derived connectors
# -----------------------------------------------------------------------------


def fuse_connectors(
    doc: GLHDocument,
    pdf_index: Dict[str, List[ConnectorMention]],
    pdf_path: str,
) -> None:
    """
    For each connector ID seen in text / index, make sure there is a
    Connector in GLHDocument, enriched with geometry where possible.

    1. If connector exists from DSL, attach sources + geometry if missing.
    2. If connector does not exist, create a minimal one with geometry only.
    """
    for cid, mentions in pdf_index.items():
        conn = doc.connectors.get(cid)
        if not conn:
            conn = Connector(connector_id=cid)
            doc.connectors[cid] = conn

        conn.sources.extend({"page": m.page, "context": m.context} for m in mentions)

        # Geometry:
        if not conn.geometry:
            geom = extract_vector_geometry_for_connector(pdf_path, cid, mentions)
            if not geom:
                geom = extract_pixel_geometry_for_connector(pdf_path, cid, mentions)
            if geom:
                conn.geometry = geom


# -----------------------------------------------------------------------------
# Harness Graph + Rule Engine Skeleton
# -----------------------------------------------------------------------------


@dataclass
class RuleViolation:
    rule_id: str
    severity: str
    message: str
    context: Dict[str, Any]


class RuleEngine:
    """
    Classical checks, no AI magic.

    Add methods that implement your taboos & constraints.
    """

    def __init__(self, rules: List[Rule]):
        self.rules = {r.rule_id: r for r in rules}

    def run_all(self, doc: GLHDocument) -> List[RuleViolation]:
        violations: List[RuleViolation] = []
        # hooks for individual rule categories
        violations.extend(self._check_awg_vs_current(doc))
        violations.extend(self._check_can_taps(doc))
        return violations

    def _check_awg_vs_current(self, doc: GLHDocument) -> List[RuleViolation]:
        """
        Example: AWG must be >= 14 for 20A over 15ft, etc.
        Stubbed here; you'd need length/current info from harness loads/nets.
        """
        out: List[RuleViolation] = []
        # TODO: implement real AWG vs current / length check
        return out

    def _check_can_taps(self, doc: GLHDocument) -> List[RuleViolation]:
        """
        Example rule: "no power on CAN lines" or "no arbitrary taps on CAN harness".
        Also stubbed.
        """
        out: List[RuleViolation] = []
        # TODO: implement CAN-specific wiring checks
        return out


# -----------------------------------------------------------------------------
# ASCII & PDF Overlay (Skeleton)
# -----------------------------------------------------------------------------


def _infer_cavities_from_pin_labels(conn: Connector) -> None:
    """Populate geometry cavities + pin row/col using labels like ``A1`` or ``B7``.

    This is a lightweight helper so we can render without an upstream geometry
    detector. If the geometry already has cavities, the function is a no-op.
    """

    if not conn.geometry or conn.geometry.cavities:
        return

    letter_digit = re.compile(r"^([A-Z])(\d+)$")
    for label, pin in conn.pins.items():
        match = letter_digit.match(label)
        if not match:
            continue
        row_letter, col_str = match.groups()
        row = ord(row_letter) - ord("A") + 1
        col = int(col_str)
        conn.geometry.cavities[(row, col)] = label
        pin.row = pin.row or row
        pin.col = pin.col or col


def render_connector_ascii(
    conn: Connector,
    legend: Dict[str, str],
    *,
    use_ansi_colors: bool = False,
) -> str:
    """
    Geometry-aware ASCII rendering with either emoji legend mapping or ANSI
    foreground/background blocks.

    ``use_ansi_colors`` is handy when a terminal supports colors but you do not
    want emoji in the grid. The function falls back to plain text when geometry
    is missing.
    """

    if not conn.geometry:
        return f"Connector {conn.connector_id}: [no geometry]\n"

    # Populate simple grids if upstream geometry detectors have not done so.
    _infer_cavities_from_pin_labels(conn)

    g = conn.geometry
    lines: List[str] = []
    lines.append(f"Connector {conn.connector_id} — Face View")

    if use_ansi_colors:
        bg_map = {
            "RD": "\033[101m",
            "BK": "\033[100m",
            "GN": "\033[102m",
            "YE": "\033[103m",
            "WH": "\033[107m",
            None: "",
        }
        text_color_map = {
            "RD": "\033[30m",
            "BK": "\033[97m",
            "GN": "\033[30m",
            "YE": "\033[30m",
            "WH": "\033[30m",
            None: "\033[0m",
        }

    border = "    +" + ("-----------" * g.cols) + "+"
    lines.append(border)
    for r in range(1, g.rows + 1):
        row_cells = []
        for c in range(1, g.cols + 1):
            label = g.cavities.get((r, c))
            if label and label in conn.pins:
                pin = conn.pins[label]
                color_code = pin.color_primary or "??"

                if use_ansi_colors:
                    bg = bg_map.get(color_code, "")
                    text_color = text_color_map.get(color_code, "\033[0m")
                    reset = "\033[0m"
                    padded_label = label.center(7)
                    cell = f"{bg}{text_color}[{padded_label}]{reset}"
                else:
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

    # Legend
    lines.append("Legend:")
    if use_ansi_colors:
        for code in legend:
            bg = bg_map.get(code, "")
            text_color = text_color_map.get(code, "\033[0m")
            reset = "\033[0m"
            padded_code = code.center(7)
            lines.append(f"  {bg}{text_color}[{padded_code}]{reset} = {code}")
    else:
        for code, emo in legend.items():
            lines.append(f"  {emo} = {code}")

    # Optional pin list
    lines.append("\nPins:")
    for plabel, pin in sorted(conn.pins.items(), key=lambda x: x[0]):
        color = f"{pin.color_primary or ''}/{pin.color_secondary or ''}".strip("/")
        lines.append(f"  {plabel}: {color:<7} - {pin.function or ''}")

    return "\n".join(lines)


def render_connector_isometric(
    conn: Connector,
    legend: Dict[str, str],
    *,
    use_ansi_colors: bool = True,
) -> str:
    """
    Simple 3D-ish rendering of a connector face using ASCII/ANSI blocks.

    This favors clarity over perspective correctness: it offsets the second
    (and subsequent) rows to imply depth while keeping the same cell shapes
    as the regular face view. The function honors ``use_ansi_colors`` to make
    the block fills match the legend colors in capable terminals.
    """

    if not conn.geometry:
        return f"Connector {conn.connector_id}: [no geometry]\n"

    _infer_cavities_from_pin_labels(conn)

    g = conn.geometry

    bg_map = {
        "RD": "\033[101m",
        "BK": "\033[100m",
        "GN": "\033[102m",
        "YE": "\033[103m",
        "WH": "\033[107m",
        None: "",
    }
    text_color_map = {
        "RD": "\033[30m",
        "BK": "\033[97m",
        "GN": "\033[30m",
        "YE": "\033[30m",
        "WH": "\033[30m",
        None: "\033[0m",
    }

    def _cell_for_label(label: Optional[str]) -> str:
        if not label:
            return "       "

        pin = conn.pins.get(label)
        if not pin or not use_ansi_colors:
            return label.center(7)

        bg = bg_map.get(pin.color_primary, "")
        text_color = text_color_map.get(pin.color_primary, "\033[0m")
        reset = "\033[0m"
        return f"{bg}{text_color}{label.center(7)}{reset}"

    def _grid_border(prefix: str = "") -> str:
        return f"{prefix}+" + "+".join(["-------"] * g.cols) + "+"

    def _grid_row(row_idx: int, prefix: str = "") -> str:
        cells: List[str] = []
        for c in range(1, g.cols + 1):
            label = g.cavities.get((row_idx, c))
            cells.append(_cell_for_label(label))
        return f"{prefix}| " + " | ".join(cells) + " |"

    lines: List[str] = [f"Connector {conn.connector_id} — 3D Isometric View"]

    # Top slanted edges to suggest perspective.
    slant = "/" + "/".join(["-------"] * g.cols) + "/"
    lines.append(f"    {slant}")
    lines.append(f"    {slant}")

    # First row (closest face)
    lines.append(_grid_border())
    lines.append(_grid_row(1))
    lines.append(_grid_border())

    # Subsequent rows are offset to the right to imply depth.
    for row_idx in range(2, g.rows + 1):
        prefix = "    " * (row_idx - 1)
        lines.append(f"{prefix}{_grid_border()}")
        lines.append(f"{prefix}{_grid_row(row_idx)}")
        lines.append(f"{prefix}{_grid_border()}")

    # Closing slants
    back_slant = "\\" + "\\".join(["       "] * g.cols) + "\\"
    lines.append(back_slant)
    lines.append(back_slant)

    # Legend and pins (colorized if desired)
    lines.append("")
    lines.append("Legend:")
    for code in legend:
        if use_ansi_colors:
            bg = bg_map.get(code, "")
            text_color = text_color_map.get(code, "\033[0m")
            reset = "\033[0m"
            lines.append(f"  {bg}{text_color}[  {code:<3} ]{reset} = {code}")
        else:
            lines.append(f"  {legend[code]} = {code}")

    lines.append("")
    lines.append("Pins:")
    for plabel, pin in sorted(conn.pins.items(), key=lambda x: x[0]):
        primary = pin.color_primary or "?"
        secondary = pin.color_secondary
        if use_ansi_colors:
            fg_primary = text_color_map.get(primary, "\033[0m")
            fg_secondary = text_color_map.get(secondary, "\033[0m")
            reset = "\033[0m"
            color_str = f"{bg_map.get(primary, '')}{fg_primary}{primary}{reset}"
            if secondary:
                color_str += f"/{bg_map.get(secondary, '')}{fg_secondary}{secondary}{reset}"
        else:
            color_str = f"{primary}/{secondary}".strip("/")
        lines.append(f"  {plabel}: {color_str:<10} - {pin.function or ''}")

    return "\n".join(lines)


def render_connector_3d_dynamic(
    conn: Connector,
    legend: Dict[str, str],
    duration: int = 10,
) -> None:
    """
    Animate a rotating 3D projection of the connector in the terminal.

    This favors ANSI block colors for pins and asterisks for the connector
    housing. It runs for ``duration`` seconds at ~15 FPS and clears the
    viewport afterward. Geometry and pins must be present or the function
    will exit early with a short notice.
    """

    if not conn.geometry or not conn.pins:
        print("No geometry or pins available for 3D rendering.")
        return

    color_map: Dict[str, Tuple[str, str]] = {
        "RD": ("101", "30"),  # red bg, black text
        "BK": ("100", "97"),  # black bg, white text
        "GN": ("102", "30"),  # green bg, black text
        "YE": ("103", "30"),  # yellow bg, black text
        "WH": ("107", "30"),  # white bg, black text
    }

    # Ensure legend colors at least map to a neutral background if not predefined.
    for code in legend:
        color_map.setdefault(code, ("47", "30"))

    def get_ansi(color_code: Optional[str]) -> str:
        bg, fg = color_map.get(color_code, color_map["BK"])
        return f"\033[{bg}m\033[{fg}m"

    def get_row_col(label: str) -> Tuple[int, int]:
        if label[0].isalpha():
            row = ord(label[0].upper()) - ord("A")
            col = int(label[1:]) - 1
        else:
            row = 0
            col = int(label) - 1
        return row, col

    rows = max(get_row_col(l)[0] for l in conn.pins) + 1
    cols = max(get_row_col(l)[1] for l in conn.pins) + 1
    spacing = 1.0

    pins_3d: List[Tuple[float, float, float, str]] = []
    x_vals: List[float] = []
    y_vals: List[float] = []
    for label, pin in conn.pins.items():
        row, col = get_row_col(label)
        x = col * spacing - (cols - 1) * spacing / 2
        y = -row * spacing
        z = 0.0
        ansi = get_ansi(pin.color_primary)
        char = ansi + "█" + "\033[0m"
        pins_3d.append((x, y, z, char))
        x_vals.append(x)
        y_vals.append(y)

    margin = 0.5
    x_min = min(x_vals) - margin
    x_max = max(x_vals) + margin
    y_min = min(y_vals) - margin
    y_max = max(y_vals) + margin
    z_front = 0.5
    z_back = -0.5
    housing_vertices: List[Tuple[float, float, float]] = [
        (x_min, y_min, z_front),
        (x_max, y_min, z_front),
        (x_max, y_max, z_front),
        (x_min, y_max, z_front),
        (x_min, y_min, z_back),
        (x_max, y_min, z_back),
        (x_max, y_max, z_back),
        (x_min, y_max, z_back),
    ]
    housing_edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    ]
    housing_char = "\033[90m*\033[0m"

    w, h = 80, 24
    out = sys.stdout
    s = 0.1
    c = (1 - s ** 2) ** 0.5
    ym = h / 3.0
    xm = 2 * ym
    z_offset = 3.0

    start_time = time.time()
    while time.time() - start_time < duration:
        housing_rot = [(c * x + s * z, y, -s * x + c * z) for x, y, z in housing_vertices]
        pins_rot = [(c * x + s * z, y, -s * x + c * z, ch) for x, y, z, ch in pins_3d]

        proj_h = [
            (
                round(w / 2 + xm * x / (z + z_offset)),
                round(h / 2 + ym * y / (z + z_offset)),
            )
            for x, y, z in housing_rot
        ]
        proj_p = [
            (
                round(w / 2 + xm * x / (z + z_offset)),
                round(h / 2 + ym * y / (z + z_offset)),
                ch,
            )
            for x, y, z, ch in pins_rot
        ]

        from collections import defaultdict

        screen: "defaultdict[Tuple[int, int], str]" = defaultdict(lambda: " ")

        for edge in housing_edges:
            start = proj_h[edge[0]]
            end = proj_h[edge[1]]
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            steps = max(abs(dx), abs(dy), 1)
            for i in range(steps + 1):
                px = start[0] + round(i * dx / steps)
                py = start[1] + round(i * dy / steps)
                if 0 <= px < w and 0 <= py < h:
                    screen[(px, py)] = housing_char

        for px, py, ch in proj_p:
            if 0 <= px < w and 0 <= py < h:
                screen[(px, py)] = ch

        lines: List[str] = []
        for y in range(h):
            line = "".join(screen[(x, y)] for x in range(w))
            lines.append(line)

        out.write("\033[H" + "\n".join(lines))
        out.flush()
        time.sleep(1 / 15.0)

    out.write("\033[H" + (" " * w + "\n") * h)
    out.flush()


def create_pdf_overlays(pdf_path: str, doc: GLHDocument, out_path: str) -> None:
    """
    Skeleton for PDF overlay generation.

    You'd typically use PyMuPDF (fitz) or ReportLab + PyMuPDF:

    - Open original PDF
    - For each connector with page + coordinates:
      * Draw a small schematic / label near the OEM drawing
    - Save to out_path.
    """
    # TODO: implement PDF overlay logic.
    log.info("create_pdf_overlays: not yet implemented, out=%s", out_path)


# -----------------------------------------------------------------------------
# UpfitSkillAgent Skeleton (LLM + Tools)
# -----------------------------------------------------------------------------


class UpfitSkillAgent:
    """
    Orchestrates:

    - PDF ingestion & index
    - GLH DSL parsing
    - Connector fusion
    - Rule engine checks
    - (Later) LLM calls for DESIGN / DIAGNOSE that emit GLH blocks.
    """

    def __init__(self, rules: List[Rule]):
        self.rule_engine = RuleEngine(rules)

    # --- Core pipelines ---

    def ingest_pdf(self, pdf_path: str) -> Tuple[GLHDocument, Dict[str, List[ConnectorMention]]]:
        blocks = extract_text_blocks_from_pdf(pdf_path)
        index = build_connector_index(blocks)
        # start with empty GLH doc; later you can mix in DSL
        doc = GLHDocument()
        fuse_connectors(doc, index, pdf_path)
        return doc, index

    def ingest_glh_text(self, glh_text: str) -> GLHDocument:
        return parse_glh_blocks(glh_text)

    def merge_pdf_and_glh(
        self,
        pdf_path: str,
        glh_text: str,
    ) -> GLHDocument:
        blocks = extract_text_blocks_from_pdf(pdf_path)
        index = build_connector_index(blocks)
        doc = parse_glh_blocks(glh_text)
        fuse_connectors(doc, index, pdf_path)
        return doc

    def lint(self, doc: GLHDocument) -> List[RuleViolation]:
        return self.rule_engine.run_all(doc)

    # --- Hooks for future LLM integration ---

    def design_harness(self, platform: VehiclePlatform, loads: List[Load]) -> GLHDocument:
        """
        Stub: call LLM with platform + loads + rules to generate GLH DSL,
        then parse and return GLHDocument.
        """
        # TODO: plug your favorite LLM / RAG layer here.
        raise NotImplementedError

    def diagnose(self, doc: GLHDocument, symptoms: Dict[str, Any]) -> str:
        """
        Stub: given existing harness model + symptoms, let LLM propose
        likely faults + test steps. You can constrain its access to doc only.
        """
        raise NotImplementedError


# -----------------------------------------------------------------------------
# Orchestrator Example
# -----------------------------------------------------------------------------


def process_pdf_to_harness(pdf_path: str, glh_seed_text: str = "") -> GLHDocument:
    """
    High-level pipeline:

    1. Parse any seed GLH DSL (if provided).
    2. Ingest PDF text and build connector index.
    3. Fuse geometry and connector IDs.
    4. Return GLHDocument ready for linting / visualization.
    """
    blocks = extract_text_blocks_from_pdf(pdf_path)
    index = build_connector_index(blocks)

    if glh_seed_text:
        doc = parse_glh_blocks(glh_seed_text)
    else:
        doc = GLHDocument()

    fuse_connectors(doc, index, pdf_path)
    return doc


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GLH demo runner")
    parser.add_argument(
        "--pdf",
        type=Path,
        default=Path("2026-Explorer-PIU-Police-Modifier-Guide_20250702_Final (1).pdf"),
        help="Optional PIU PDF to ingest (defaults to local sample name)",
    )
    parser.add_argument(
        "--animate",
        type=int,
        default=0,
        metavar="SECONDS",
        help="Duration to show the rotating 3D view (0 disables animation)",
    )
    parser.add_argument(
        "--no-iso",
        action="store_true",
        help="Skip the static isometric render",
    )
    args = parser.parse_args()

    # Minimal GLH seed example:
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
cols: 4

A1: RD/WH, Fog lamp feed
A2: BK, Ground
A3: GN, Micron grill flasher +
A4: BK/WH, Micron grill flasher -
B1: YE, Spare feed 1
B2: WH, Spare feed 2
B3: RD, Spare feed 3
B4: BK, Spare ground
```

"""

    pdf_ready = args.pdf.exists() and _pdfplumber_available()

    if pdf_ready:
        doc = process_pdf_to_harness(str(args.pdf), glh_seed)
    else:
        reason_bits = []
        if not args.pdf.exists():
            reason_bits.append(f"missing file: {args.pdf}")
        if not _pdfplumber_available():
            reason_bits.append("pdfplumber not installed")

        log.info(
            "Skipping PDF ingestion (%s); rendering seed GLH only.",
            "; ".join(reason_bits) or "PDF unavailable",
        )
        doc = parse_glh_blocks(glh_seed)

    if "C2001" in doc.connectors:
        ascii_art = render_connector_ascii(doc.connectors["C2001"], doc.legend)
        print(ascii_art)

        if not args.no_iso:
            iso_art = render_connector_isometric(
                doc.connectors["C2001"], doc.legend, use_ansi_colors=True
            )
            print(iso_art)

        if args.animate > 0 and sys.stdout.isatty():
            render_connector_3d_dynamic(
                doc.connectors["C2001"], doc.legend, duration=args.animate
            )
        elif args.animate > 0:
            log.info("Animation requested but stdout is not a TTY; skipping animation.")
    else:
        print("Connector C2001 not found yet.")
