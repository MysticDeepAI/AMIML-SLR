# `amiml` — Analysis Toolkit

Modular Python package powering the AMIML systematic review.

## Modules

| Module | Description |
|---|---|
| `loader.py` | Data loading (`CSV`/`Excel`), cleaning, multi-label expansion |
| `taxonomy.py` | Rule-based mapping of free-text labels to canonical families (scope, data modality, task, output artifact, metric, publisher) |
| `metrics.py` | Normalisation pipelines for quantitative and qualitative metric names |
| `themes.py` | Keyword dictionaries and thematic coding engine for ethical/regulatory and limitations fields |
| `analysis.py` | Section-level synthesis functions (§4.2–§4.8) and `run_all()` pipeline |
| `plots.py` | Publication-quality matplotlib figures for every research question |
| `export.py` | DataFrame → BibTeX export |
| `arxiv.py` | arXiv API search automation and RIS export |

## Installation

```bash
# From the repository root:
pip install -e ".[dev]"
```

## Quick Start

```python
from amiml.analysis import run_all
from amiml import plots

results = run_all("data/DB.xlsx")
plots.plot_year_counts(results["4.2"]["year_counts"])
```
