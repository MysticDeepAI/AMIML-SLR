"""
Rule-based mapping of free-text labels to canonical families.

Each public function receives a raw label string and returns the
canonical family name used throughout the paper and the analysis.
"""

import re

from amiml.loader import clean_token


# ── Scope ────────────────────────────────────────────────────────────

def scope_category(x: object) -> str:
    """Map a ``Type (Local/Global)`` cell to {Local, Global, Local & Global}."""
    from amiml.loader import split_labels

    labels = set(split_labels(x))
    has_local = "local" in labels
    has_global = "global" in labels

    if has_local and has_global:
        return "Local & Global"
    if has_local:
        return "Local"
    if has_global:
        return "Global"
    return "Not specified"


# ── Data modality ────────────────────────────────────────────────────

def data_family(label: str) -> str:
    """Map a raw data-type label to a canonical modality family."""
    t = clean_token(label)
    if "time series" in t or "timeseries" in t:
        return "Time series"
    if "text" in t or "nlp" in t:
        return "Text"
    if "image" in t or "vision" in t:
        return "Image"
    if "graph" in t:
        return "Graph"
    if "audio" in t:
        return "Audio"
    if "tabular" in t or "structured" in t or "relational" in t:
        return "Tabular"
    return "Other"


# ── Task type ────────────────────────────────────────────────────────

def task_family(label: str) -> str:
    """Map a raw task-type label to a canonical task family."""
    t = clean_token(label)
    if "regression" in t:
        return "Regression"
    if "clustering" in t:
        return "Clustering"
    if "segmentation" in t or "detection" in t:
        return "Detection/Segmentation"
    if "classification" in t:
        if "binary" in t:
            return "Classification (binary)"
        if "multi" in t or "multiclass" in t:
            return "Classification (multi)"
        return "Classification"
    return "Other"


# ── Output artifact ──────────────────────────────────────────────────

def _classify_output_token(t: str) -> str:
    """Classify a *single* output-type token."""
    tt = clean_token(t)

    # 1 — Counterfactual
    if any(k in tt for k in [
        "counterfactual", "recourse", "what if", "what-if",
        "minimal perturbation", "actionable", "feature adjustment",
        "change the prediction", "flip prediction",
    ]):
        return "Counterfactual"

    # 2 — Rule-based
    if any(k in tt for k in [
        "rule", "rules", "if then", "if-then", "decision rule",
        "fuzzy", "tree", "trepan", "surrogate", "itemset", "itemsets",
    ]):
        return "Rule-based"

    # 3 — Effect summary
    if any(k in tt for k in [
        "partial dependence", "pdp", "ale",
        "accumulated local effects", "ice",
        "individual conditional expectation",
        "dependence plot", "effect plot", "response curve",
        "sensitivity curve", "marginal plot", "perturbation plot",
        "stacked-area",
    ]):
        return "Effect summary"

    # 4 — Attribution vector
    if any(k in tt for k in [
        "feature", "attribution", "importance", "saliency", "heatmap",
        "shap", "lime", "force plot", "token-level", "signed score",
        "contribution", "mask", "occlusion",
    ]):
        return "Attribution vector"

    return "Other"


def output_family(label: str) -> str:
    """Map a raw ``Output Type`` cell to a canonical artifact family.

    When the cell contains multiple outputs separated by ``,``, ``;``,
    ``/``, ``&``, or ``and``, the *first* matching family is returned
    (preserving the original order).
    """
    raw = label or ""
    parts = [p.strip() for p in re.split(r"(?:,|;|\n|/| & | and )", raw) if p and p.strip()]
    if not parts:
        parts = [raw]

    for p in parts:
        c = _classify_output_token(p)
        if c != "Other":
            return c
    return _classify_output_token(clean_token(raw))


# ── Metric family (coarse) ───────────────────────────────────────────

def metric_family(metric_label: str) -> str:
    """Map a raw metric name to a coarse evaluation family."""
    t = clean_token(metric_label)
    if any(k in t for k in [
        "accuracy", "f1", "auc", "precision", "recall",
        "rmse", "mae", "mse", "r2", "cross-entropy", "logloss",
    ]):
        return "Predictive performance"
    if any(k in t for k in [
        "fidelity", "faithfulness", "infidelity", "agreement", "consistency",
    ]):
        return "Explanation fidelity/faithfulness"
    if any(k in t for k in [
        "proximity", "sparsity", "plausibility", "feasibility",
        "actionability", "diversity", "validity",
    ]):
        return "Counterfactual quality"
    if any(k in t for k in [
        "robustness", "stability", "sensitive", "sensitivity",
        "jaccard", "kendall",
    ]):
        return "Robustness/stability"
    if any(k in t for k in [
        "complexity", "size", "number of rules", "rule length",
        "premise", "length",
    ]):
        return "Complexity/compactness"
    if any(k in t for k in [
        "time", "runtime", "efficiency", "computational", "memory",
    ]):
        return "Computational cost"
    return "Other"


# ── Publisher proxy ──────────────────────────────────────────────────

def publisher_from_url(url: str) -> str:
    """Infer publisher family from a paper's landing-page URL domain."""
    from urllib.parse import urlparse

    host = urlparse(str(url)).netloc.lower().replace("www.", "")
    if "arxiv.org" in host:
        return "arXiv"
    if "ieee" in host:
        return "IEEE"
    if "springer" in host:
        return "Springer"
    if "sciencedirect" in host or "elsevier" in host:
        return "Elsevier"
    if "acm" in host:
        return "ACM"
    if "mdpi" in host:
        return "MDPI"
    if "wiley" in host:
        return "Wiley"
    if "tandfonline" in host:
        return "Taylor & Francis"
    return "Other"
