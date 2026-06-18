# Methodology

Method, algorithm, and references behind the two charts. Statistics are generated separately by
`scripts/compute_stats.py` into [`STATS.md`](STATS.md); this file documents *how* they are produced.
Sources verified June 2026.

- **Part A — Perception vs. Reality:** conceptual model (no external data; values encode an argument).
- **Part B — Practitioner sentiment:** content analysis of 12 public sources.

---

## Part A — Perception vs. Reality (conceptual)

**Represents.** For six contributors to a Genie deployment, two markers on a 0–100 scale:
*Credit* (importance teams assign) vs. *Impact* (actual effect on production accuracy and trust).

**Data.** [`data/perception_vs_reality.csv`](../data/perception_vs_reality.csv) — `factor, credit, impact`.

**Calculation.** `Gap = Impact − Credit` (positive = under-credited; negative = over-credited).
`scripts/perception_vs_reality.py` renders the chart; `compute_stats.py` reports means, gaps, and the
credit-vs-impact correlation.

**Nature.** Illustrative opinion device from hands-on experience. Values are chosen to make one
argument legible — teams over-credit the model and under-credit the foundation. They are not
measurements, and the inverse pattern (r ≈ −0.90) is a property of the chosen values, not a finding.

---

## Part B — Practitioner sentiment (content analysis)

### Research question
When people who have used Databricks Genie write about it publicly, which aspects do they raise as
**strengths** and which as **concerns**?

### Corpus
[`data/sources.csv`](../data/sources.csv) — 12 sentiment-bearing sources (S1–S12): review aggregates,
independent reviews, practitioner field reports, and vendor material reporting outcomes. A source is
"sentiment-bearing" if it expresses evaluation, not just product facts. Vendor-published: S10, S11, S12.

### Algorithm
Inputs: corpus of 12 sources; theme set Θ of 8 themes.

1. Include a source only if it states an evaluation (praise or criticism).
2. For each source `s` and theme `θ`, read its treatment of `θ`.
3. If `s` praises `θ` → `strength[θ] += 1`. If `s` criticizes `θ` → `concern[θ] += 1`.
4. A source may increment **both** sides of one theme when its assessment is mixed
   (at most one per side per source per theme).
5. Compute per-theme `total`, `net = strength − concern`, `share = strength / total`.
6. Order themes by `net` descending; render diverging bar (concern left, strength right).

```
strength[θ] = concern[θ] = 0  for all θ in Θ
for s in corpus (12):
    for θ in Θ (8):
        if praises(s, θ):    strength[θ] += 1
        if criticizes(s, θ): concern[θ]  += 1
```

This is encoded literally as rows in [`data/sentiment_coding.csv`](../data/sentiment_coding.csv)
(`theme, source, polarity`); `scripts/practitioner_sentiment.py` and `compute_stats.py` simply
aggregate those rows.

### Themes (inclusion criteria)

| Theme | Counts when a source mentions… |
|---|---|
| Speed / time-to-insight | faster answers, reduced turnaround, self-service speed |
| Native Databricks integration | working inside the platform/Unity Catalog (− side: only useful if already on Databricks) |
| Governance & per-user permissions | row/column security, per-user access, read-only queries |
| Answer accuracy | correctness of SQL/answers; benchmark figures; correctness on real schemas |
| Learning curve for business users | whether non-technical users can use it without training |
| Cost / compute (DBU) spend | pricing, compute consumption, enterprise cost |
| Trust & silent wrong answers | confidence in results; undetected errors; auditability |
| Heavy data prep required | need for curation/metadata/modeling before it works |

### Per-theme source attribution (the calculation)

| Theme | Strength sources (n) | Concern sources (n) |
|---|---|---|
| Speed / time-to-insight | S10, S6, S1, S3, S9, S11 (6) | S2 (1) |
| Native Databricks integration | S1, S3, S10, S11, S12 (5) | S3 (1) |
| Governance & per-user permissions | S12, S3, S1, S11 (4) | — (0) |
| Answer accuracy | S11, S3, S1, S5 (4) | S6, S7, S2, S4, S5 (5) |
| Learning curve for business users | S11, S10 (2) | S1, S2, S9 (3) |
| Cost / compute (DBU) spend | S11 (1) | S3, S1, S5 (3) |
| Trust & silent wrong answers | S7 (1) | S6, S5, S7, S2 (4) |
| Heavy data prep required | — (0) | S3, S5, S6, S7, S9, S12 (6) |

Mixed sources (both sides of a theme): S3 (integration), S5 (accuracy), S7 (trust).

### External hard figures (chart callout; not part of the coding)
[`data/external_figures.csv`](../data/external_figures.csv): Gartner Peer Insights 4.8/5, 94% recommend,
n=167 (S1); ToolChase 4.4/5 (S3); vendor 84.5% first-try benchmark and Genie Code 77.1% vs 32.1% (S11).

### Constraints
- Single coder; no second-rater agreement check. Counts are directional.
- Non-random corpus (n=12), surfaced via web search; Reddit and LinkedIn not included.
- 3 of 12 sources are vendor-published and skew positive on Speed, Integration, Governance.
- Theme boundaries (esp. Accuracy vs. Trust) involve coding judgment.
- Point-in-time (June 2026); feature- and price-bound themes may change.

### References
See [`data/sources.csv`](../data/sources.csv) for the full S1–S12 list with URLs.
