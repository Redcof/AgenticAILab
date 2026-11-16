"""A deterministic lexical retrieval baseline, not a semantic RAG retriever.

Complexity: index O(total tokens), search O(corpus token counts).
In-memory only; do not use as a production authorization boundary.
"""

import math
import re
from collections import Counter
from collections.abc import Sequence

from ragforge.domain import Document, SearchHit


def tokenize(text: str) -> list[str]:
    """Basic Unicode word tokenization for the learning baseline."""
    return re.findall(r"\w+", text.casefold())


class LexicalRetriever:
    """Cosine similarity of raw word-count vectors.

    The tenant_id must come from an authenticated/trusted context. Production
    also requires storage authorization, cache isolation and citation checks.
    """

    def __init__(self, documents: Sequence[Document]) -> None:
        ids = [(doc.tenant_id, doc.id) for doc in documents]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate document IDs within a tenant")
        self._documents = tuple(documents)
        self._vectors = [Counter(tokenize(doc.text)) for doc in self._documents]
        self._norms = [
            math.sqrt(sum(count * count for count in vector.values()))
            for vector in self._vectors
        ]

    def search(
        self, query: str, *, tenant_id: str, limit: int = 5
    ) -> list[SearchHit]:
        if not tenant_id or not tenant_id.strip():
            raise ValueError("Tenant ID is required")
        if limit < 1:
            raise ValueError("Limit must be positive")

        query_vector = Counter(tokenize(query))
        if not query_vector:
            return []
        query_norm = math.sqrt(sum(count * count for count in query_vector.values()))
        hits: list[SearchHit] = []

        for document, vector, document_norm in zip(
            self._documents, self._vectors, self._norms
        ):
            # Exclude other tenants BEFORE similarity scoring.
            if document.tenant_id != tenant_id:
                continue
            dot = sum(
                count * vector.get(term, 0)
                for term, count in query_vector.items()
            )
            if dot == 0 or document_norm == 0:
                continue
            score = dot / (query_norm * document_norm)
            hits.append(SearchHit(document=document, score=score))

        return sorted(
            hits, key=lambda hit: (-hit.score, hit.document.id)
        )[:limit]
