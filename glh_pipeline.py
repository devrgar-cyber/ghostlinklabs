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
from typing import List, Dict, Optional, Tuple, Any
import re
import logging

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


def render_connector_ascii(conn: Connector, legend: Dict[str, str]) -> str:
    """
    Geometry-aware ASCII rendering with emoji legend mapping.

    This assumes `conn.geometry` is filled with rows/cols and cavity->label mapping.
    """
    if not conn.geometry:
        return f"Connector {conn.connector_id}: [no geometry]\n"

    g = conn.geometry
    lines: List[str] = []
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

    # Legend
    lines.append("Legend:")
    for code, emo in legend.items():
        lines.append(f"  {emo} = {code}")

    # Optional pin list
    lines.append("\nPins:")
    for plabel, pin in sorted(conn.pins.items(), key=lambda x: x[0]):
        color = f"{pin.color_primary or ''}/{pin.color_secondary or ''}".strip("/")
        lines.append(f"  {plabel}: {color:<7} - {pin.function or ''}")

    return "\n".join(lines)


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
    # Example usage (replace with your actual PIU PDF path):
    pdf_path = "2026-Explorer-PIU-Police-Modifier-Guide_20250702_Final (1).pdf"

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
cols: 7

A1: RD/WH, Fog lamp feed
A2: BK, Ground
B1: GN, Micron grill flasher +
B2: BK/WH, Micron grill flasher -
```

"""

    # Build doc from both PDF + DSL
    doc = process_pdf_to_harness(pdf_path, glh_seed)

    # Example: render one connector ASCII
    if "C2001" in doc.connectors:
        ascii_art = render_connector_ascii(doc.connectors["C2001"], doc.legend)
        print(ascii_art)
    else:
        print("Connector C2001 not found yet.")
