# ghostlink_reflection_experiment.py
# Can also be used in a Jupyter Notebook (.ipynb) for interactive visualization.
# This script simulates and analyzes self-model dynamics for GhostLink.

import itertools, random, pandas as pd, matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------
# Utility functions from the reflection harness.
# These help tokenize text, compute similarities, and measure reflection metrics.
# -----------------------------------------------------------------------------

def tokens(s: str):
    # Extract lowercase alphanumeric tokens from the input string.
    import re
    return re.findall(r"[A-Za-z0-9_]+", s.lower())

def jaccard(a, b):
    # Compute Jaccard similarity between two token sets.
    # Jaccard = |Intersection| / |Union|, measures overlap of unique items.
    A, B = set(a), set(b)
    if not A and not B:
        return 1.0  # Both empty → perfect similarity.
    return len(A & B) / max(1, len(A | B))

def shingles(s: str, k: int = 3):
    # Create k-character shingles (sliding substrings) from a text.
    # Used to approximate semantic difference by overlapping character n-grams.
    import re
    s = re.sub(r"\s+", " ", s.strip())
    return { s[i:i+k] for i in range(max(0, len(s)-k+1)) }

def metrics(prev_summary: str, cur_summary: str):
    # Compute three metrics between consecutive summaries:
    # coherence (similarity), novelty (1 - coherence), lift (shingle divergence).
    coh = jaccard(tokens(prev_summary), tokens(cur_summary)) if prev_summary else 0.0
    nov = 1.0 - coh
    prev_sh, cur_sh = shingles(prev_summary), shingles(cur_summary)
    if not prev_sh and not cur_sh:
        lift = 0.0
    else:
        inter = len(prev_sh & cur_sh)
        union = max(1, len(prev_sh | cur_sh))
        lift = 1.0 - (inter / union)
    return (round(coh,4), round(nov,4), round(lift,4))

def summarize_operation(op: str, state: str):
    # Generate a deterministic summary string representing an operation.
    # The summary includes an operation label, transformation type, and a short
    # SHA-256 digest of the input state for traceability.
    import hashlib
    return f"STATE:: op={op} | transform=reflective_map | input_digest={hashlib.sha256(state.encode()).hexdigest()[:8]}"

# -----------------------------------------------------------------------------
# Experimental function.
# This runs multiple combinations of parameters (depth, boundary, noise) and
# collects metrics for each reflection cycle.
# -----------------------------------------------------------------------------

def run_experiment(depth_levels=(1,3,5), boundary_flags=(True,False), noise_levels=(0,0.05,0.10), cycles=4, seed=42):
    rng = random.Random(seed)
    results = []

    # Iterate over all parameter combinations.
    for D, B, N in itertools.product(depth_levels, boundary_flags, noise_levels):
        prev_summary = ""  # Initialize previous state summary.
        state = "SEED::MAP on MAP"  # Base starting state string.
        for t in range(cycles):
            # Introduce random noise into the state to simulate entropy effects.
            noisy = list(state)
            for i in range(int(len(noisy)*N)):
                idx = rng.randrange(len(noisy))
                noisy[idx] = random.choice("abcdefghijklmnopqrstuvwxyz")
            state = "".join(noisy)

            # Summarize current operation and compute metrics vs previous.
            cur_summary = summarize_operation("MAP on MAP", state)
            coh, nov, lift = metrics(prev_summary, cur_summary)

            # Store experimental results for this step.
            results.append(dict(depth=D, boundary=B, noise=N, t=t, coherence=coh, novelty=nov, lift=lift))
            prev_summary = cur_summary

    # Compile results into a DataFrame and save for later analysis.
    df = pd.DataFrame(results)
    df.to_csv("aggregate_metrics.csv", index=False)
    return df

# -----------------------------------------------------------------------------
# Analysis and visualization.
# Uses seaborn/matplotlib for visual plots and statsmodels for basic regression.
# -----------------------------------------------------------------------------

def analyze_results(df):
    import seaborn as sns
    plt.figure(figsize=(8,5))
    # Plot coherence trajectories by depth and boundary condition.
    sns.lineplot(data=df, x="t", y="coherence", hue="depth", style="boundary")
    plt.title("Coherence vs Depth & Boundary")
    plt.savefig("coherence_vs_depth_boundary.png")
    plt.close()

    plt.figure(figsize=(8,5))
    # Plot predictive lift variation across noise levels.
    sns.lineplot(data=df, x="noise", y="lift", hue="boundary", style="depth")
    plt.title("Predictive Lift vs Noise")
    plt.savefig("lift_vs_noise.png")
    plt.close()

    # Simple regression model: lift ~ noise + noise^2 to test inverted-U hypothesis.
    import statsmodels.formula.api as smf
    model = smf.ols('lift ~ noise + I(noise**2)', data=df).fit()

    # Save statistical summary to a text file.
    with open('anova_results.txt', 'w') as f:
        f.write(model.summary().as_text())
    return model

# -----------------------------------------------------------------------------
# Entry point for standalone execution.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    df = run_experiment()  # Run experiment with default parameters.
    model = analyze_results(df)  # Analyze and plot the results.
    print("Experiment complete. Files saved: aggregate_metrics.csv, coherence_vs_depth_boundary.png, lift_vs_noise.png, anova_results.txt")
