"""
Normalisation pipelines for quantitative and qualitative metric names.
"""

import re

import pandas as pd


# ── Quantitative metrics ─────────────────────────────────────────────

def _split_metrics_cell(cell: str) -> list[str]:
    s = str(cell).replace("\n", ",")
    parts = [p.strip() for p in s.split(",") if p.strip()]
    parts = [re.sub(r"^(and\s+)", "", p, flags=re.IGNORECASE).strip() for p in parts]
    return parts


def normalize_metric_name(m: str) -> str:
    """Normalise a raw quantitative metric string to a canonical form."""
    t = str(m).strip().lower()
    t = t.replace("\u2019", "'").replace("\u2013", "-").replace("\u2014", "-")
    t = t.replace("\u221e", "inf")
    t = t.replace("r\u00b2", "r2").replace("r^2", "r2")
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\bf1[-\s]?score\b", "f1", t)
    t = re.sub(r"\bauc[-\s]?roc\b", "auc", t)
    t = re.sub(r"\b(i|d|sn)auc\b", "auc", t)
    t = re.sub(r"\bauc metrics\b", "auc", t)
    t = re.sub(r"\bmean absolute error\b", "mae", t)
    t = re.sub(r"\bmean squared error\b", "mse", t)
    t = re.sub(r"\broot mean squared error\b", "rmse", t)
    return t.strip(" .;:")


def explode_quant_metrics(df: pd.DataFrame, col: str = "Quantitative metrics") -> pd.DataFrame:
    """Expand multi-valued quantitative metric cells into long format."""
    out = df.copy()
    out[col] = out[col].fillna("").astype(str).apply(_split_metrics_cell)
    out = out.explode(col)
    return out[out[col].notna() & (out[col].astype(str).str.strip() != "")]


def build_quant_top(df: pd.DataFrame, col: str = "Quantitative metrics", top_k: int = 25) -> pd.DataFrame:
    """Return a top-*k* frequency table of normalised quantitative metrics."""
    q = explode_quant_metrics(df, col)
    q["metric_norm"] = q[col].apply(normalize_metric_name)
    return (
        q["metric_norm"]
        .value_counts()
        .head(top_k)
        .rename_axis("metric_raw")
        .reset_index(name="n_mentions")
    )


# ── Qualitative metrics ──────────────────────────────────────────────

def _split_qual_cell(cell: str) -> list[str]:
    s = str(cell).replace("\n", ",")
    return [p.strip() for p in s.split(",") if p.strip()]


def normalize_qual_name(x: str) -> str:
    """Normalise a raw qualitative metric string to a canonical form."""
    t = str(x).strip().lower()
    t = t.replace("\u2019", "'").replace("\u2013", "-")
    t = re.sub(r"\s+", " ", t)
    t = t.replace("pleasibility", "plausibility")
    t = re.sub(r"^and\s+", "", t)

    if t in {"no", "n/a", "na", "none"}:
        return ""

    if any(k in t for k in [
        "visual inspection", "visual assessment", "visual analysis",
        "visual evaluation", "visual comparisons", "visual comparison",
        "illustrative visualizations", "graphical visualizations",
    ]):
        return "visual inspection/assessment"
    if any(k in t for k in ["heatmap", "heatmaps", "saliency maps", "relevance maps"]):
        return "saliency/heatmap inspection"
    if "force plots" in t:
        return "force plots"
    if "tsne" in t:
        return "tsne plots"
    if any(k in t for k in [
        "user study", "participants", "user feedback", "user preference",
        "perceived trust", "subjective feedback",
    ]):
        return "user feedback"
    if any(k in t for k in ["domain expert feedback", "expert interpretation"]):
        return "expert feedback"
    if any(k in t for k in ["interpretability", "comprehensibility", "conceptual clarity"]):
        return "interpretability"
    for concept in ["readability", "actionability", "plausibility", "trust", "consistency", "stability"]:
        if concept in t:
            return concept
    return t


def explode_qual_metrics(df: pd.DataFrame, col: str = "Qualitative metrics") -> pd.DataFrame:
    """Expand multi-valued qualitative metric cells into long format."""
    out = df.copy()
    out[col] = out[col].fillna("").astype(str).apply(_split_qual_cell)
    out = out.explode(col)
    return out[out[col].astype(str).str.strip() != ""]


def build_qual_top(df: pd.DataFrame, col: str = "Qualitative metrics", top_k: int = 10) -> pd.DataFrame:
    """Return a top-*k* frequency table of normalised qualitative metrics."""
    q = explode_qual_metrics(df, col)
    q["qual_norm"] = q[col].apply(normalize_qual_name)
    q = q[q["qual_norm"].astype(str).str.strip() != ""]
    return (
        q["qual_norm"]
        .value_counts()
        .head(top_k)
        .rename_axis("qual_raw")
        .reset_index(name="n_mentions")
    )
