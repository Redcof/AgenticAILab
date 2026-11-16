"""# Use case 04 — Retrieval evaluation with explicit gold labels

## Problem
An answer can look plausible even when retrieval misses supporting documents.
Evaluate retrieval independently using a labeled relevant-document set.

## Sample
Retrieved top-4: d1, d2, d3, d4. Gold relevant: d1, d3, d5, d6, d7.
At k=4, precision=2/4=0.5, recall=2/5=0.4, F1≈0.444.

## Reproduce
```bash
python3 usecase/04_evaluation.py
```

## Limits
Labels are synthetic. Production evaluation requires representative queries,
independently reviewed judgments, confidence intervals and slice analysis.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Metrics:
    precision: float
    recall: float
    f1: float
    reciprocal_rank: float


def evaluate(retrieved: list[str], relevant: set[str], k: int) -> Metrics:
    """Compute simple binary relevance metrics for the top-k results."""
    if k < 1 or not relevant:
        raise ValueError("k must be positive and gold set nonempty")
    top = retrieved[:k]
    if len(top) != len(set(top)):
        raise ValueError("Retrieved document IDs must be unique")
    matches = sum(doc in relevant for doc in top)
    precision = matches / len(top) if top else 0.0
    recall = matches / len(relevant)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    rr = next((1 / i for i, doc in enumerate(top, 1) if doc in relevant), 0.0)
    return Metrics(precision, recall, f1, rr)


def main() -> None:
    metrics = evaluate(["d1", "d2", "d3", "d4"], {"d1", "d3", "d5", "d6", "d7"}, 4)
    print(metrics)


if __name__ == "__main__":
    main()
