
# GhostLink — Proof of Record (PoR)

This document defines **formal + mechanical** proof obligations, success thresholds, and test procedures.
Passing all checks supports the GhostLink claims in the session spec.

## Formal (mathematical) obligations (to be proven/outlined)
- PCA kernel well-posedness: normalization & existence for all Θ.
- Non-explosion: bounded expected events per tick under spawn/recycle bounds.
- Stationarity/ergodicity: conditions for stationary distribution.
- SOC regime: parameter ranges yielding branching factor ≈ 1.
- Continuity submartingale: 𝓒(t) non-decreasing in expectation under assumptions.
- Compression criterion: if dL(ℙ)/dt < 0 then persistence threshold is crossed.

> Deliver as lemmas/theorems in a separate appendix or the LaTeX spec.

## Mechanical obligations (empirical tests) with thresholds θ_k

**Test 1 — Reproducibility**  
Run N_seeds=5 with fixed Θ. Metric variability (stdev/mean) ≤ **0.10** for: continuity growth, predictive lift, SOC τ estimate.

**Test 2 — Robustness**  
Parameter sweep over ±20% for key Θ. Fraction of runs with positive continuity slope ≥ **0.80**.

**Test 3 — Predictive Lift**  
Next-step prediction (Σ vs not-Σ) using features {neighbors, traces, legacy depth} vs baseline {neighbors only}.  
Relative accuracy (or F1) improvement ≥ **5%**.

**Test 4 — Cost Advantage (difference-only)**  
Average activity ratio ⟨|Δ_t|/|V|⟩ ≤ **0.20** and measured step cost ≤ **0.30×** full sweep cost.

**Test 5 — SOC Signature**  
Avalanche size-tail fits power law with 1 < τ < 3 and KS p ≥ **0.05**; branching factor in [0.9, 1.1].

**Test 6 — Legacy Gain**  
Mutual information MI(ancestry+features ; x_{t+1}) − MI(features ; x_{t+1}) ≥ **0.01 bits/cell** (or ≥ **2%** predictive lift).

**Test 7 — Compression (MDL)**  
Description length L(ℙ(t)) decreases (negative slope) on ≥ **75%** of epochs in the evaluation window.

**Test 8 — Topology Invariance**  
Metrics differ ≤ **10%** between planar grid and spherical surrogate (icosa/HEALPix-like adjacency) after normalization.

**Test 9 — Ablation Sanity**  
Removing SCAR effects or adaptive ordering reduces predictive lift or continuity slope by ≥ **15%**.

---

## Outputs
- JSON report with pass/fail for Tests 1..9 and metric values.
- Plots: avalanche tail fit, continuity curves, activity ratio, ablation comparisons.

## How to run
```
python tests/run_proof.py
```
Artifacts: `proof_report.json`, `proof_plots/`.
