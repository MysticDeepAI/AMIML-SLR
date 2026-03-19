# RIS — Bibliographic Records

PRISMA 2020 bibliographic records exported from [Rayyan](https://www.rayyan.ai/) in RIS format. Each subdirectory corresponds to a stage in the systematic review workflow.

## PRISMA Flow

```
  Identification     619 records    ──→  Duplicates removed: 296
        │
        ▼
    Screening         323 records    ──→  Excluded (scope): 223
        │
        ▼
   Eligibility        100 records    ──→  Excluded (criteria): 30
        │
        ▼
    Included           70 records
```

## Files

| Directory | File | Records | Description |
|---|---|---:|---|
| `identification/` | `619.ris` | 619 | All records retrieved from arXiv, ACM DL, IEEE Xplore, and Scopus |
| `duplicates/` | `296_1.ris` | 141 | Duplicate batch 1 (Rayyan deduplication) |
| `duplicates/` | `296_2.ris` | 155 | Duplicate batch 2 (manual near-duplicate inspection) |
| `screening/` | `364.ris` | 364 | Records excluded by Rayyan (includes screening exclusions + duplicate overlap) |
| `eligibility/` | `30.ris` | 30 | Full-text articles excluded for not meeting inclusion criteria |
| `included/` | `70.ris` | 70 | **Final corpus** — studies included in the review |

## Information Sources

| Source | Records | Search fields |
|---|---:|---|
| arXiv | 40 | Title, abstract |
| ACM Guide to Computing Literature | 94 | Title, abstract, keywords |
| IEEE Xplore | 146 | Title, abstract, keywords |
| Scopus | 339 | Title, abstract, keywords |

## Notes

- Records were screened using [Rayyan](https://www.rayyan.ai/) with built-in duplicate detection.
- Rayyan IDs differ across export sessions (`rayyan-171536xxx` for the merged 619 export vs. `rayyan-164453xxx` for the per-stage exports).
- The `screening/364.ris` file contains all Rayyan-excluded records, which partially overlaps with `duplicates/` due to Rayyan's internal categorization.
