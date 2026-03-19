"""
Conservative keyword-based thematic coding for free-text extraction fields.

A theme is marked as present for a paper only if at least one associated
keyword matches the extracted text (case-insensitive substring matching).
"""

import re

import pandas as pd

# ── Ethical / Regulatory themes (§4.7) ───────────────────────────────

ETHICAL_THEMES: dict[str, list[str]] = {
    "privacy / data protection": [
        "gdpr", "privacy", "data protection", "personal data",
        "consent", "anonym", "data minimization",
    ],
    "fairness / bias": [
        "fairness", "bias", "discrimination", "equity",
        "disparate impact", "demographic parity", "equalized odds",
    ],
    "accountability / transparency": [
        "accountability", "accountable", "transparency",
        "audit", "auditing", "traceability", "explainability",
    ],
    "regulation / compliance": [
        "regulation", "regulatory", "compliance", "law", "legal", "policy",
        "right to explanation", "right to an explanation",
        "ai act", "artificial intelligence act",
        "algorithmic accountability act",
    ],
    "responsible / trustworthy ai": [
        "ethics", "ethical", "responsible ai", "trustworthy",
        "trust", "human rights", "stakeholders",
    ],
    "security / misuse": [
        "security", "adversarial", "attack", "misuse", "abuse",
    ],
}

# ── Limitation / Challenge themes (§4.8) ─────────────────────────────

LIMITATION_THEMES: dict[str, list[str]] = {
    "computational cost / scalability": [
        "computational", "runtime", "running time", "time", "expensive",
        "efficiency", "scalable", "scalability", "overhead",
        "np-hard", "exponential", "quadratic",
    ],
    "hyperparameter sensitivity / tuning": [
        "hyperparameter", "tuning", "parameter selection", "manual",
        "sensitive to", "depends on", "budget", "threshold",
        "epsilon", "lambda", "beam width", "window size",
    ],
    "fidelity / surrogate mismatch": [
        "fidelity", "faithful", "approximation", "surrogate",
        "local linear", "misestimate",
    ],
    "robustness / stability / randomness": [
        "robust", "robustness", "stability", "sensitive", "variance",
        "variability", "non-determinism", "random seeds", "inconsistent",
    ],
    "data limitations / distribution issues": [
        "dataset", "shift", "drift", "out-of-distribution", "ood",
        "imbalance", "noise", "missing", "mcar", "mar", "mnar",
    ],
    "limited evaluation scope / generalization": [
        "single", "only", "restricted", "limited", "toy", "curated",
        "preliminary", "validated", "not tested", "remains untested",
        "extension to", "generalizability",
    ],
    "human evaluation gap / usability": [
        "human-in-the-loop", "human centered", "user study",
        "participants", "usability", "domain expert", "expert",
        "clinician", "user-centric", "end-user",
    ],
    "actionability / plausibility trade-offs": [
        "actionable", "actionability", "plausible", "plausibility",
        "feasible", "realistic", "trade-off", "pareto",
        "choose among", "conflicting objectives",
    ],
}


# ── Generic coding function ──────────────────────────────────────────

def theme_counts(
    text_series: pd.Series,
    themes: dict[str, list[str]],
) -> pd.DataFrame:
    """Count how many papers explicitly mention each theme.

    Parameters
    ----------
    text_series : pd.Series
        Free-text column from the extraction table.
    themes : dict
        ``{theme_name: [keyword, …]}`` dictionary.

    Returns
    -------
    pd.DataFrame
        Columns ``theme`` and ``n_papers``, sorted descending.
    """
    text = text_series.fillna("").astype(str).str.lower()
    rows = []
    for theme, keys in themes.items():
        pat = "|".join(re.escape(k.lower()) for k in keys)
        n = int(text.str.contains(pat).sum())
        rows.append((theme, n))
    return (
        pd.DataFrame(rows, columns=["theme", "n_papers"])
        .sort_values("n_papers", ascending=False)
        .reset_index(drop=True)
    )
