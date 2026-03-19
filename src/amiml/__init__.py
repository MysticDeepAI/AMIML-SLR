"""
AMIML — Analysis toolkit for the systematic review of
Post-Hoc Model-Agnostic Interpretability Methods.

Modules
-------
loader      Data loading, cleaning, and multi-label expansion.
taxonomy    Rule-based mapping of free-text labels to canonical families.
metrics     Normalisation of quantitative and qualitative metric names.
themes      Keyword-based thematic coding for free-text extraction fields.
analysis    Section-level synthesis functions (§4.2–§4.8) and ``run_all``.
plots       Publication-quality matplotlib figures for every RQ.
export      BibTeX / RIS export helpers.
arxiv       arXiv API search and RIS export utilities.
"""

from amiml.analysis import run_all  # noqa: F401

__version__ = "1.0.0"
