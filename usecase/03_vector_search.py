"""# Use case 03 — Exact cosine retrieval with tenant isolation

## Problem
A vector search must rank by similarity while excluding unauthorized tenants
*before* ranking, rather than filtering a globally ranked top-k afterward.

## Reproduce
```bash
python3 usecase/03_vector_search.py
```

## Expected
Tenant A sees only A1 and A2; tenant B's highly similar B1 is never returned.

## Limits
Hand-authored 2D vectors are not embeddings. This is exact linear search,
not an approximate nearest-neighbor (ANN) index or authentication layer.
"""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    id: str
    tenant: str
    vector: tuple[float, ...]


ITEMS = (
    Item("A1", "A", (0.8, 0.6)),
    Item("A2", "A", (0.0, 1.0)),
    Item("B1", "B", (1.0, 0.0)),
)


def cosine(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    if len(a) != len(b) or not a:
        raise ValueError("Vectors must have the same nonzero dimension")
    denom = math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))
    if denom == 0:
        raise ValueError("Zero-norm vectors cannot be compared")
    return sum(x * y for x, y in zip(a, b)) / denom


def search(query: tuple[float, ...], tenant: str, k: int = 2) -> list[tuple[str, float]]:
    if not tenant or k < 1:
        raise ValueError("Tenant required and k must be positive")
    ranked = [(item.id, cosine(query, item.vector)) for item in ITEMS if item.tenant == tenant]
    return sorted(ranked, key=lambda hit: (-hit[1], hit[0]))[:k]


def main() -> None:
    print("Tenant A:", search((1.0, 0.0), "A"))
    print("Tenant B:", search((1.0, 0.0), "B"))


if __name__ == "__main__":
    main()
