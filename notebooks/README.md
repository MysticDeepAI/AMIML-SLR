# Notebooks

Analysis notebooks that import from the `amiml` package (`../src/amiml/`).

## Setup

```bash
# From the repository root:
pip install -e ".[dev]"
```

## `Data_analysis.ipynb`

Main synthesis notebook. Calls `amiml.analysis.run_all()` and generates all
figures via `amiml.plots`. Organised by paper section:

| Section | Output |
|---|---|
| §4.2 — Descriptive landscape | Papers per year, outlet distribution, citation statistics |
| §4.3 — Method characterisation | Scope distribution, output families, theoretical foundations |
| §4.4 — Data/tasks/domains | Modality counts, task types, modality × task cross-tabulation, top domains/datasets |
| §4.5 — Evaluation practice | Top-15 quantitative metrics, top-10 qualitative criteria, qualitative coverage |
| §4.6 — Human feedback | Feedback prevalence, cross-tabulation by output family |
| §4.7 — Normative themes | Keyword-based thematic coding of ethical/regulatory fields |
| §4.8 — Limitations | Keyword-based thematic coding of limitations/challenges |

## `ARXIV_WEB_SCRAPING.ipynb`

Automated search script for arXiv records. Uses `amiml.arxiv.search_arxiv()`
to retrieve records matching the review's Boolean search strategy and exports
results via `amiml.arxiv.df_to_ris()` for Rayyan import.
