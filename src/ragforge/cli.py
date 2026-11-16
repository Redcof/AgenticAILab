"""Command-line entrypoint for the runnable Stage 1 demo."""

import argparse

from ragforge.domain import Document
from ragforge.retrieval import LexicalRetriever


DEMO_DOCUMENTS = (
    Document("rag-001", "RAG combines retrieval with language generation.", "demo"),
    Document("rag-002", "Vector databases support semantic retrieval.", "demo"),
    Document("rag-003", "RAG retrieval is private to this tenant.", "other"),
)


def main() -> None:
    parser = argparse.ArgumentParser(description="RAGForge Stage 1 retrieval demo")
    parser.add_argument("query", nargs="?", default="RAG retrieval")
    parser.add_argument("--tenant", default="demo", help="Demo tenant ID")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    retriever = LexicalRetriever(DEMO_DOCUMENTS)
    try:
        hits = retriever.search(args.query, tenant_id=args.tenant, limit=args.limit)
    except ValueError as exc:
        parser.error(str(exc))
    if not hits:
        print("No matching documents.")
        return
    for hit in hits:
        print(f"{hit.score:.3f} | {hit.document.id} | {hit.document.text}")


if __name__ == "__main__":
    main()
