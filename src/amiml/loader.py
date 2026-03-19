"""
Data loading, cleaning, and multi-label expansion utilities.
"""

import re
from pathlib import Path

import pandas as pd


def load_db(path: str, sheet_name: str = "DATA_EXTRACTION") -> pd.DataFrame:
    """Load the extraction database from CSV or Excel.

    Parameters
    ----------
    path : str
        Path to ``.csv`` or ``.xlsx`` file.
    sheet_name : str, optional
        Sheet name when *path* is an Excel file (default ``DATA_EXTRACTION``).

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with spurious ``Unnamed`` columns removed.
    """
    p = Path(path)
    if p.suffix in (".xlsx", ".xls"):
        df = pd.read_excel(p, sheet_name=sheet_name)
    else:
        df = pd.read_csv(p)
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    return df


def clean_token(x: object) -> str:
    """Lower-case, trim, and normalise whitespace / hyphens."""
    x = str(x).strip().lower()
    x = re.sub(r"\s+", " ", x)
    x = x.replace("\u2013", "-").replace("\u2014", "-")  # en-dash, em-dash
    return x


def split_labels(x: object, sep: str = ",") -> list[str]:
    """Split a multi-label cell into a list of cleaned tokens."""
    if pd.isna(x):
        return []
    return [clean_token(t) for t in str(x).split(sep) if clean_token(t)]


def explode_col(df: pd.DataFrame, col: str, sep: str = ",") -> pd.DataFrame:
    """Expand a multi-label column into one row per label.

    Parameters
    ----------
    df : pd.DataFrame
    col : str
        Column to explode.
    sep : str
        Separator used inside the column (default ``","``).

    Returns
    -------
    pd.DataFrame
        Long-format DataFrame with one label per row in *col*.
    """
    out = df.copy()
    out[col] = out[col].apply(lambda x: split_labels(x, sep))
    return out.explode(col).dropna(subset=[col])
