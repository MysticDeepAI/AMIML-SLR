"""
Bibliographic export utilities (DataFrame → BibTeX / RIS).
"""

from datetime import datetime

import pandas as pd


def dataframe_to_bibtex(df: pd.DataFrame, output_path: str) -> None:
    """Convert a DataFrame with bibliographic metadata into a BibTeX file.

    Expected columns: ``title``, ``authors`` (semicolon-separated),
    ``published`` (``%Y-%m-%d %H:%M:%S``), ``summary``, ``doi``.
    """
    entries: list[str] = []

    for _, row in df.iterrows():
        try:
            pub_date = datetime.strptime(str(row["published"]), "%Y-%m-%d %H:%M:%S")
            year = pub_date.strftime("%Y")
        except Exception:
            year = "Unknown"

        authors_str = row.get("authors", "")
        first_author = authors_str.split(";")[0].strip() if authors_str else ""
        surname = first_author.split()[-1] if first_author else "Unknown"
        key = f"{surname}{year}"

        lines = [
            f"@article{{{key},",
            f"  title = {{{row.get('title', '').strip()}}},",
            f"  author = {{{authors_str.strip()}}},",
            f"  year = {{{year}}},",
        ]
        if "doi" in df.columns and pd.notnull(row.get("doi")):
            lines.append(f"  doi = {{{row['doi'].strip()}}},")
        if "summary" in df.columns and pd.notnull(row.get("summary")):
            abstract = row["summary"].replace("\n", " ").strip()
            lines.append(f"  abstract = {{{abstract}}},")
        lines.append("}")
        entries.append("\n".join(lines))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(entries))
