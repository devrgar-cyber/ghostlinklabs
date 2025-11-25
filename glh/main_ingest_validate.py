"""
Top-level runner to build ground truth from DSL seeds, ingest a PDF,
and compute validation metrics. Designed to be the one-button entry
point for evaluating the fast vision pipeline against curated GT.
"""
from __future__ import annotations

from pathlib import Path
import argparse
import json
import logging
import sys

if __package__ is None:  # allow execution via `python glh/main_ingest_validate.py`
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from glh.glh_pipeline import GLHDocument
from glh.glh_ground_truth import generate_ground_truth, load_ground_truth_cache
from glh.glh_gt_db import gt_db_to_document
from glh.glh_validation import validate_extraction, ValidationMetrics
from glh.glh_vision_fast import ingest_pdf_connectors_ultrafast
from glh.pdf_inspector import pretty_print_report, summarize_pdf_structure

log = logging.getLogger("glh.main")
logging.basicConfig(level=logging.INFO)


def build_ground_truth_corpus(dsl_dir: Path, gt_cache_dir: Path, page_map: Path | None = None) -> GLHDocument:
    generate_ground_truth(dsl_dir, gt_cache_dir, page_map)
    offline_doc = load_ground_truth_cache(gt_cache_dir)

    online_doc = gt_db_to_document()

    combined = GLHDocument()
    combined.connectors.update(offline_doc.connectors)
    combined.connectors.update(online_doc.connectors)
    return combined


def run_full_validation(pdf_path: Path, dsl_dir: Path, gt_cache_dir: Path, page_map: Path | None = None) -> ValidationMetrics:
    log.info("Ingesting connectors from %s", pdf_path)
    extracted = ingest_pdf_connectors_ultrafast(str(pdf_path))

    log.info("Building ground truth corpus from %s", dsl_dir)
    gt_doc = build_ground_truth_corpus(dsl_dir, gt_cache_dir, page_map)

    metrics = validate_extraction(extracted, gt_doc)
    log.info(
        "Accuracy %.1f | F1 %.3f | Color %.3f | Function %.3f",
        metrics.overall_score,
        metrics.pin_detection_f1,
        metrics.color_accuracy,
        metrics.function_accuracy,
    )
    return metrics


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Run fast ingest + validation against DSL/DB ground truth.")
    parser.add_argument("--pdf", type=Path, help="Path to PIU PDF", required=False)
    parser.add_argument("--dsl-dir", type=Path, default=Path("dsl_seed"))
    parser.add_argument("--gt-cache", type=Path, default=Path("ground_truth_cache"))
    parser.add_argument("--page-map", type=Path, default=None)
    parser.add_argument("--skip-validation", action="store_true", help="Skip PDF ingest and only build GT cache")
    parser.add_argument(
        "--inspect-pdf",
        action="store_true",
        help="Print a structural PDF summary (xref, spans, fonts) instead of running validation.",
    )
    parser.add_argument(
        "--inspect-json",
        type=Path,
        default=None,
        help="Optional path to write the PDF structure report as JSON.",
    )
    args = parser.parse_args()

    if args.skip_validation and not args.inspect_pdf:
        log.info("Skipping validation; generating ground truth only.")
        build_ground_truth_corpus(args.dsl_dir, args.gt_cache, args.page_map)
        return

    if args.inspect_pdf:
        if not args.pdf:
            parser.error("--inspect-pdf requires --pdf")
        if not args.pdf.exists():
            parser.error(f"PDF {args.pdf} does not exist")

        report = summarize_pdf_structure(args.pdf)
        print(pretty_print_report(report))
        if args.inspect_json:
            args.inspect_json.write_text(json.dumps(report.to_dict(), indent=2))
            log.info("Wrote PDF structure report to %s", args.inspect_json)
        return

    if not args.pdf:
        parser.error("--pdf is required unless skipping validation")
    if not args.pdf.exists():
        parser.error(f"PDF {args.pdf} does not exist")

    metrics = run_full_validation(args.pdf, args.dsl_dir, args.gt_cache, args.page_map)
    print(json.dumps(metrics.__dict__, indent=2))


if __name__ == "__main__":
    _cli()
