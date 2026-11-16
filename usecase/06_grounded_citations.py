"""# Use case 06 — Verify a numerical claim against a citation

## Problem
A generated answer can cite a document but state a number not supported by it.
Check that the cited source actually contains the claimed refund window.

## Sample
Document p2 says 30 days. A claim of 60 days with citation p2 is rejected.

## Reproduce
```bash
python3 usecase/06_grounded_citations.py
```

## Limits
This is a deliberately narrow numeric extractor, not an NLI/entailment model.
Production claim verification must handle paraphrases, qualifiers, contradictions,
document versions, permissions, and evidence spans.
"""

import re

SOURCES = {
    "p1": "Refund window is 14 days for purchases before January 2026.",
    "p2": "Current refund window is 30 days for eligible purchases.",
}


def verify_days(claimed_days: int, citation_id: str) -> bool:
    """Verify a toy 'N days' claim against one cited source."""
    source = SOURCES.get(citation_id)
    if source is None:
        return False
    mentioned_days = [int(x) for x in re.findall(r"\b(\d+)\s+days\b", source)]
    return claimed_days in mentioned_days


def main() -> None:
    for days, source in ((30, "p2"), (60, "p2"), (30, "missing")):
        print(f"claim={days} days citation={source}: supported={verify_days(days, source)}")


if __name__ == "__main__":
    main()
