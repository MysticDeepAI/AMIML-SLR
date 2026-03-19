"""
Section-level synthesis functions aligned with the paper's RQs (§4.2–§4.8).

Each ``synth_*`` function receives the cleaned DataFrame and returns a
dict of named result tables (``pd.DataFrame``).  The convenience wrapper
:func:`run_all` executes the full pipeline.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from amiml.loader import load_db, clean_token, explode_col
from amiml.taxonomy import (
    scope_category, data_family, task_family,
    output_family, metric_family, publisher_from_url,
)
from amiml.metrics import build_quant_top, build_qual_top, explode_quant_metrics
from amiml.themes import theme_counts, ETHICAL_THEMES, LIMITATION_THEMES


# ═══════════════════════════════════════════════════════════════════════
# §4.2  Descriptive landscape
# ═══════════════════════════════════════════════════════════════════════

def synth_42_descriptive(df: pd.DataFrame) -> dict:
    """Publication volume, citation profile, and outlet distribution."""
    years = df["Publication year"].dropna().astype(int)
    citations = pd.to_numeric(
        df["Number of citation google scholar"], errors="coerce"
    ).fillna(0).astype(int)

    q1, q3 = np.percentile(citations, [25, 75])
    stats = pd.DataFrame([{
        "n_papers": len(df),
        "cit_median": int(np.median(citations)),
        "cit_IQR": float(q3 - q1),
        "cit_mean": round(float(np.mean(citations)), 2),
        "cit_max": int(np.max(citations)),
    }])

    year_counts = (
        years.value_counts().sort_index()
        .rename_axis("year").reset_index(name="n_papers")
    )

    top_cited = (
        df.assign(citations=citations)
        .sort_values("citations", ascending=False)
        [["Title", "Publication year", "citations", "Link"]]
        .head(10)
    )

    publisher_proxy = (
        df["Link"].apply(publisher_from_url)
        .value_counts()
        .rename_axis("publisher").reset_index(name="n_papers")
    )

    return dict(
        stats=stats,
        year_counts=year_counts,
        top_cited=top_cited,
        publisher_proxy=publisher_proxy,
    )


# ═══════════════════════════════════════════════════════════════════════
# §4.3  Method characterisation (scope, outputs, foundations)
# ═══════════════════════════════════════════════════════════════════════

def synth_43_methods(df: pd.DataFrame) -> dict:
    """Scope distribution, output families, and theoretical foundations."""
    scope = df["Type (Local/Global)"].apply(scope_category)
    scope_counts = (
        scope.value_counts()
        .rename_axis("scope").reset_index(name="n_papers")
    )

    out_long = explode_col(df, "Output Type")
    out_long["output_family"] = out_long["Output Type"].apply(output_family)
    output_family_counts = (
        out_long["output_family"].value_counts()
        .rename_axis("output_family").reset_index(name="n_mentions")
    )

    foundations_long = explode_col(df, "Theoretical Foundation")
    foundation_top = (
        foundations_long["Theoretical Foundation"].value_counts()
        .rename_axis("foundation_raw").reset_index(name="n_mentions")
    )

    return dict(
        scope_counts=scope_counts,
        output_family_counts=output_family_counts,
        foundation_top=foundation_top,
    )


# ═══════════════════════════════════════════════════════════════════════
# §4.4  Data / tasks / domains / datasets
# ═══════════════════════════════════════════════════════════════════════

def synth_44_data_tasks(df: pd.DataFrame) -> dict:
    """Data modalities, task types, domains, datasets, and cross-tabulation."""
    data_long = explode_col(df, "Data Type")
    data_long["data_family"] = data_long["Data Type"].apply(data_family)
    data_counts = (
        data_long["data_family"].value_counts()
        .rename_axis("data_family").reset_index(name="n_mentions")
    )

    task_long = explode_col(df, "Task type")
    task_long["task_family"] = task_long["Task type"].apply(task_family)
    task_counts = (
        task_long["task_family"].value_counts()
        .rename_axis("task_family").reset_index(name="n_mentions")
    )

    domain_long = explode_col(df, "Domain Application")
    domain_long["Domain Application"] = (
        domain_long["Domain Application"].replace({"no": "not specified"})
    )
    domain_top = (
        domain_long["Domain Application"].value_counts().head(20)
        .rename_axis("domain").reset_index(name="n_mentions")
    )

    datasets_long = explode_col(df, "Datasets")
    datasets_top = (
        datasets_long["Datasets"].value_counts().head(20)
        .rename_axis("dataset").reset_index(name="n_mentions")
    )

    dt = data_long[["Index", "data_family"]].merge(
        task_long[["Index", "task_family"]], on="Index", how="inner",
    )
    crosstab_data_task = pd.crosstab(
        dt["data_family"], dt["task_family"],
    ).reset_index()

    return dict(
        data_counts=data_counts,
        task_counts=task_counts,
        domain_top=domain_top,
        datasets_top=datasets_top,
        crosstab_data_task=crosstab_data_task,
    )


# ═══════════════════════════════════════════════════════════════════════
# §4.5  Evaluation practice
# ═══════════════════════════════════════════════════════════════════════

def synth_45_evaluation(df: pd.DataFrame) -> dict:
    """Top quantitative/qualitative metrics and qualitative coverage."""
    quant_top = build_quant_top(df, top_k=25)
    qual_top_10 = build_qual_top(df, top_k=10)

    qual = df["Qualitative metrics"].fillna("No").apply(clean_token)
    qual_presence = pd.DataFrame([{
        "n_papers": len(df),
        "with_qual_metrics": int((qual != "no").sum()),
        "share_with_qual_metrics": round(float((qual != "no").mean()), 3),
    }])

    return dict(
        quant_top=quant_top,
        qual_top_10=qual_top_10,
        qual_presence=qual_presence,
    )


# ═══════════════════════════════════════════════════════════════════════
# §4.6  Human feedback
# ═══════════════════════════════════════════════════════════════════════

def synth_46_human_feedback(df: pd.DataFrame) -> dict:
    """Feedback prevalence and cross-tabulation by output family."""
    fb = df["Human feeback"].fillna("No").apply(clean_token)
    feedback_counts = (
        fb.value_counts()
        .rename_axis("human_feedback").reset_index(name="n_papers")
    )

    out_long = explode_col(df, "Output Type")
    out_long["output_family"] = out_long["Output Type"].apply(output_family)
    out_long["human_feedback"] = (
        df.set_index("Index")["Human feeback"]
        .fillna("No").apply(clean_token)
        .reindex(out_long["Index"]).values
    )
    cross = pd.crosstab(
        out_long["output_family"], out_long["human_feedback"],
    ).reset_index()

    return dict(feedback_counts=feedback_counts, cross_output_feedback=cross)


# ═══════════════════════════════════════════════════════════════════════
# §4.7  Normative / ethical / regulatory themes
# ═══════════════════════════════════════════════════════════════════════

def synth_47_ethical(df: pd.DataFrame) -> pd.DataFrame:
    return theme_counts(df["Ethical/Regulatory Aspects"], ETHICAL_THEMES)


# ═══════════════════════════════════════════════════════════════════════
# §4.8  Limitations and challenges
# ═══════════════════════════════════════════════════════════════════════

def synth_48_limitations(df: pd.DataFrame) -> pd.DataFrame:
    return theme_counts(df["Limitations/Challenges"], LIMITATION_THEMES)


# ═══════════════════════════════════════════════════════════════════════
# Full pipeline
# ═══════════════════════════════════════════════════════════════════════

def run_all(path: str, sheet_name: str = "DATA_EXTRACTION") -> dict:
    """Execute the complete synthesis pipeline.

    Parameters
    ----------
    path : str
        Path to the extraction database (``.csv`` or ``.xlsx``).
    sheet_name : str
        Excel sheet name (ignored for CSV).

    Returns
    -------
    dict
        Keyed by paper section: ``"4.2"`` … ``"4.8"``.
    """
    df = load_db(path, sheet_name=sheet_name)
    return {
        "4.2": synth_42_descriptive(df),
        "4.3": synth_43_methods(df),
        "4.4": synth_44_data_tasks(df),
        "4.5": synth_45_evaluation(df),
        "4.6": synth_46_human_feedback(df),
        "4.7": synth_47_ethical(df),
        "4.8": synth_48_limitations(df),
    }
