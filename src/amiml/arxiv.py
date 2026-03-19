"""
arXiv API search automation and RIS export.

Provides functions to query the arXiv API, extract structured metadata
(title, authors, abstract, DOI, keywords), and export results as RIS
for import into Rayyan or other reference managers.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
import xml.etree.ElementTree as ET


# ── Keyword extraction (lightweight, no spaCy required) ──────────────

def extract_keywords_simple(text: str, max_words: int = 6) -> list[str]:
    """Extract candidate keywords via simple noun-phrase heuristics.

    For production use, replace with spaCy:
    ``nlp = spacy.load("en_core_web_sm")``
    """
    # Fallback: longest capitalised tokens (crude but dependency-free)
    tokens = text.split()
    seen: set[str] = set()
    kw: list[str] = []
    for t in tokens:
        w = t.strip(".,;:()[]\"'")
        if len(w) > 3 and w[0].isupper() and w.lower() not in seen:
            seen.add(w.lower())
            kw.append(w)
        if len(kw) >= max_words:
            break
    return kw


# ── arXiv API query ──────────────────────────────────────────────────

ARXIV_API = "http://export.arxiv.org/api/query?"
NS = {"atom": "http://www.w3.org/2005/Atom"}


def search_arxiv(
    query: str,
    *,
    max_results: int = 200,
    start: int = 0,
    sort_by: str = "submittedDate",
    sort_order: str = "descending",
) -> pd.DataFrame:
    """Query the arXiv API and return structured results.

    Parameters
    ----------
    query : str
        arXiv search query (e.g. ``all:"model-agnostic" AND all:"post-hoc"``).
    max_results : int
        Maximum number of results to retrieve.

    Returns
    -------
    pd.DataFrame
        Columns: ``id, title, summary, authors, published, doi, link``.
    """
    params = {
        "search_query": query,
        "start": start,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    resp = requests.get(ARXIV_API, params=params, timeout=60)
    resp.raise_for_status()

    root = ET.fromstring(resp.content)
    records: list[dict] = []

    for entry in root.findall("atom:entry", NS):
        title = entry.findtext("atom:title", "", NS).replace("\n", " ").strip()
        summary = entry.findtext("atom:summary", "", NS).replace("\n", " ").strip()
        published = entry.findtext("atom:published", "", NS)[:19].replace("T", " ")
        authors = "; ".join(
            a.findtext("atom:name", "", NS)
            for a in entry.findall("atom:author", NS)
        )
        doi_el = entry.find("atom:doi", NS)
        doi = doi_el.text.strip() if doi_el is not None else ""
        link = entry.findtext("atom:id", "", NS).strip()

        records.append(dict(
            id=link,
            title=title,
            summary=summary,
            authors=authors,
            published=published,
            doi=doi,
            link=link,
        ))

    return pd.DataFrame(records)


# ── RIS export ───────────────────────────────────────────────────────

def df_to_ris(
    df: pd.DataFrame,
    output_path: str,
    *,
    date_min: datetime = datetime(2020, 1, 1),
    date_max: datetime = datetime(2025, 2, 28),
    keyword_fn=extract_keywords_simple,
) -> int:
    """Export a DataFrame of arXiv results to RIS format.

    Parameters
    ----------
    df : pd.DataFrame
        As returned by :func:`search_arxiv`.
    output_path : str
        Destination ``.ris`` file.
    date_min, date_max : datetime
        Only include records published within this range.
    keyword_fn : callable
        Function ``(text) -> list[str]`` for keyword extraction.

    Returns
    -------
    int
        Number of records written.
    """
    written = 0
    with open(output_path, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            try:
                pub = datetime.strptime(str(row["published"]), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
            if not (date_min <= pub <= date_max):
                continue

            title = row["title"].replace("\n", " ").replace("\r", " ")
            abstract = row["summary"].replace("\n", " ").replace("\r", " ")
            keywords = keyword_fn(f"{title}. {abstract}")

            f.write("TY  - \n")
            f.write(f"TI  - {title}\n")
            for author in row["authors"].split(";"):
                f.write(f"AU  - {author.strip()}\n")
            f.write(f"PY  - {pub.strftime('%Y')}\n")
            for kw in keywords:
                f.write(f"KW  - {kw}\n")
            if row.get("doi"):
                f.write(f"DO  - {row['doi']}\n")
            f.write(f"Y1  - {row['published']}\n")
            f.write(f"AB  - {abstract}\n")
            f.write("ER  - \n\n")
            written += 1

    return written
