"""
Validation helpers to compare extracted GLHDocuments against
reference ground truth documents.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from glh.glh_pipeline import GLHDocument, Connector, Pin


def _pin_key(pin: Pin) -> Tuple[str, str, str]:
    return (
        (pin.color_primary or "").upper(),
        (pin.color_secondary or "").upper(),
        (pin.function or "").strip().lower(),
    )


@dataclass
class ValidationMetrics:
    overall_score: float
    pin_detection_f1: float
    color_accuracy: float
    function_accuracy: float
    ocr_cer_avg: float = 0.0
    details: Dict[str, Dict[str, int]] = field(default_factory=dict)


def validate_extraction(extracted: GLHDocument, ground_truth: GLHDocument) -> ValidationMetrics:
    """Compute simple per-connector pin metrics.

    F1 is computed on pin labels. Color/function accuracy are averaged across
    overlapping pins. CER is left as zero (placeholder) to keep signature stable.
    """
    total_tp = total_fp = total_fn = 0
    color_hits = color_total = 0
    func_hits = func_total = 0
    details: Dict[str, Dict[str, int]] = {}

    for cid, gt_conn in ground_truth.connectors.items():
        det_conn = extracted.connectors.get(cid)
        gt_pins = set(gt_conn.pins.keys())
        det_pins = set(det_conn.pins.keys()) if det_conn else set()

        tp = len(gt_pins & det_pins)
        fp = len(det_pins - gt_pins)
        fn = len(gt_pins - det_pins)

        total_tp += tp
        total_fp += fp
        total_fn += fn

        if det_conn:
            for pin_label in gt_pins & det_pins:
                g_pin = gt_conn.pins[pin_label]
                d_pin = det_conn.pins[pin_label]
                color_total += 1
                func_total += 1
                if _pin_key(g_pin)[:2] == _pin_key(d_pin)[:2]:
                    color_hits += 1
                if _pin_key(g_pin)[2] == _pin_key(d_pin)[2]:
                    func_hits += 1

        details[cid] = {"tp": tp, "fp": fp, "fn": fn}

    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) else 0.0
    recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

    color_acc = color_hits / color_total if color_total else 0.0
    func_acc = func_hits / func_total if func_total else 0.0

    overall = (f1 + color_acc + func_acc) / 3 * 100.0 if (color_total or func_total or total_tp) else 0.0

    return ValidationMetrics(
        overall_score=overall,
        pin_detection_f1=f1,
        color_accuracy=color_acc,
        function_accuracy=func_acc,
        ocr_cer_avg=0.0,
        details=details,
    )


__all__ = [
    "ValidationMetrics",
    "validate_extraction",
]
