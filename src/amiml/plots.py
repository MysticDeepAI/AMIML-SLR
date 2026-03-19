"""
Publication-quality matplotlib figures for each RQ.

Every function returns a ``matplotlib.figure.Figure`` and optionally
saves to *outpath* at 600 dpi (suitable for journal submission).
"""

from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


# ── Shared defaults ──────────────────────────────────────────────────

_BAR_KW = dict(width=0.85, edgecolor="black", linewidth=0.4)
_GRID_KW = dict(axis="y", linewidth=0.3, alpha=0.5)
_SAVE_KW = dict(dpi=600, bbox_inches="tight")


def _maybe_save(fig, outpath):
    if outpath:
        fig.savefig(outpath, **_SAVE_KW)


# ── §4.2  Year counts ───────────────────────────────────────────────

def plot_year_counts(year_df: pd.DataFrame, *, outpath: str | None = None):
    """Bar chart of included papers per year."""
    df = year_df.copy()
    df["year"] = df["year"].astype(int)
    df = df.sort_values("year")

    fig, ax = plt.subplots(figsize=(3.5, 2.4))
    ax.bar(df["year"], df["n_papers"], **_BAR_KW)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of papers")
    ax.grid(**_GRID_KW)
    ax.set_axisbelow(True)

    label_map = {2025: "  2025-2"}
    ax.set_xticks(df["year"].tolist())
    ax.set_xticklabels([label_map.get(y, str(y)) for y in df["year"]])

    fig.tight_layout()
    _maybe_save(fig, outpath)
    return fig


# ── §4.2  Publisher proxy ────────────────────────────────────────────

def plot_publisher_proxy(pub_df: pd.DataFrame, *, outpath: str | None = None):
    """Bar chart of papers by publisher/outlet family."""
    df = pub_df.sort_values("n_papers", ascending=False)
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ax.bar(df["publisher"], df["n_papers"], **_BAR_KW)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("Publisher")
    ax.set_ylabel("Number of papers")
    ax.grid(**_GRID_KW)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelrotation=35)
    fig.tight_layout()
    _maybe_save(fig, outpath)
    return fig


# ── §4.3  Scope (Local/Global) ──────────────────────────────────────

def plot_scope(scope_df: pd.DataFrame, *, outpath: str | None = None):
    df = scope_df.sort_values("n_papers", ascending=False)
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ax.bar(df["scope"], df["n_papers"], **_BAR_KW)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("Scope")
    ax.set_ylabel("Number of papers")
    ax.grid(**_GRID_KW)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelrotation=20)
    fig.tight_layout()
    _maybe_save(fig, outpath)
    return fig


# ── §4.3  Output families ───────────────────────────────────────────

def plot_output_families(out_df: pd.DataFrame, *, outpath: str | None = None):
    df = out_df.sort_values("n_mentions", ascending=False)
    short = {
        "Attribution vector": "Attribution",
        "Effect summary": "Effect summary",
        "Rule-based": "Rule-based",
        "Counterfactual": "Counterfactual",
        "Other": "Other",
    }
    df["label"] = df["output_family"].map(short).fillna(df["output_family"])
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ax.bar(df["label"], df["n_mentions"], **_BAR_KW)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("Output family")
    ax.set_ylabel("Number of mentions")
    ax.grid(**_GRID_KW)
    ax.set_axisbelow(True)
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df["label"], rotation=20, ha="right")
    fig.tight_layout()
    _maybe_save(fig, outpath)
    return fig


# ── §4.4  Data modalities ───────────────────────────────────────────

def plot_data_types(data_df: pd.DataFrame, *, outpath: str | None = None):
    df = data_df.sort_values("n_mentions", ascending=False)
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ax.bar(df["data_family"], df["n_mentions"], **_BAR_KW)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("Data type")
    ax.set_ylabel("Number of mentions")
    ax.grid(**_GRID_KW)
    ax.set_axisbelow(True)
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df["data_family"], rotation=35, ha="right", rotation_mode="anchor")
    fig.tight_layout(pad=0.4)
    _maybe_save(fig, outpath)
    return fig


# ── §4.4  Task types ────────────────────────────────────────────────

def plot_task_types(task_df: pd.DataFrame, *, outpath: str | None = None):
    df = task_df.sort_values("n_mentions", ascending=False)
    short = {
        "Classification (binary)": "Classif. (bin)",
        "Classification (multi)": "Classif. (multi)",
        "Detection/Segmentation": "Det./Seg.",
    }
    df["label"] = df["task_family"].map(short).fillna(df["task_family"])
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ax.bar(df["label"], df["n_mentions"], **_BAR_KW)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("Task type")
    ax.set_ylabel("Number of mentions")
    ax.grid(**_GRID_KW)
    ax.set_axisbelow(True)
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df["label"], rotation=20, ha="right", rotation_mode="anchor")
    fig.tight_layout(pad=0.4)
    _maybe_save(fig, outpath)
    return fig


# ── §4.4  Data × Task heatmap ───────────────────────────────────────

def plot_data_task_heatmap(cross_df: pd.DataFrame, *, outpath: str | None = None):
    short = {
        "Classification (binary)": "Classif. (bin)",
        "Classification (multi)": "Classif. (multi)",
        "Detection/Segmentation": "Det./Seg.",
    }
    mat = cross_df.set_index("data_family")
    xlabels = [short.get(c, c) for c in mat.columns]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    im = ax.imshow(mat.values, aspect="auto")
    ax.set_yticks(range(len(mat.index)))
    ax.set_yticklabels(mat.index)
    ax.set_xticks(range(len(mat.columns)))
    ax.set_xticklabels(xlabels, rotation=25, ha="right")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("# papers")
    ax.set_xlabel("Task type")
    ax.set_ylabel("Data type")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, str(int(mat.values[i, j])), ha="center", va="center", fontsize=8)
    fig.tight_layout()
    _maybe_save(fig, outpath)
    return fig


# ── §4.5  Top-15 quantitative metrics ───────────────────────────────

def plot_quant_top15(quant_df: pd.DataFrame, *, outpath: str | None = None):
    df = quant_df.head(15).sort_values("n_mentions", ascending=True)
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.barh(df["metric_raw"], df["n_mentions"])
    ax.set_xlabel("Mentions (#)")
    ax.set_ylabel("Quantitative metric")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.6)
    for i, v in enumerate(df["n_mentions"].values):
        ax.text(v + 0.1, i, str(int(v)), va="center", fontsize=8)
    fig.tight_layout()
    _maybe_save(fig, outpath)
    return fig


# ── §4.5  Top-10 qualitative metrics ────────────────────────────────

def plot_qual_top10(qual_df: pd.DataFrame, *, outpath: str | None = None):
    df = qual_df.head(10).sort_values("n_mentions", ascending=True)
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    ax.barh(df["qual_raw"], df["n_mentions"])
    ax.set_xlabel("Mentions (#)")
    ax.set_ylabel("Qualitative metric")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.6)
    for i, v in enumerate(df["n_mentions"].values):
        ax.text(v + 0.1, i, str(int(v)), va="center", fontsize=8)
    fig.tight_layout()
    _maybe_save(fig, outpath)
    return fig


# ── §4.6  Human feedback ────────────────────────────────────────────

def plot_human_feedback(fb_df: pd.DataFrame, *, outpath: str | None = None):
    df = fb_df.copy()
    df["human_feedback"] = df["human_feedback"].astype(str).str.lower().str.strip()
    df["human_feedback"] = pd.Categorical(df["human_feedback"], categories=["yes", "no"], ordered=True)
    df = df.sort_values("human_feedback")
    fig, ax = plt.subplots(figsize=(4.8, 3.2))
    ax.bar(df["human_feedback"].astype(str), df["n_papers"])
    ax.set_ylabel("# papers")
    ax.set_xlabel("Human feedback")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.6)
    for x, v in zip(df["human_feedback"].astype(str), df["n_papers"]):
        ax.text(x, v + 0.3, str(int(v)), ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    _maybe_save(fig, outpath)
    return fig


# ── §4.7  Ethical themes ────────────────────────────────────────────

def plot_ethical_themes(themes_df: pd.DataFrame, *, outpath: str | None = None):
    df = themes_df.sort_values("n_papers", ascending=False)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.barh(df["theme"], df["n_papers"])
    ax.set_xlabel("# papers")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis="x", linestyle="--", linewidth=0.6, alpha=0.6)
    for i, v in enumerate(df["n_papers"].values):
        ax.text(v + 0.1, i, str(int(v)), va="center", fontsize=8)
    ax.invert_yaxis()
    fig.tight_layout()
    _maybe_save(fig, outpath)
    return fig
