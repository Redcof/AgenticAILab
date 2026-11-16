import pytest

from ragforge.domain import Document
from ragforge.retrieval import LexicalRetriever, tokenize


@pytest.fixture
def retriever() -> LexicalRetriever:
    return LexicalRetriever(
        [
            Document("1", "RAG retrieval", "tenant-a"),
            Document("2", "RAG retrieval", "tenant-b"),
            Document("3", "Python engineering", "tenant-a"),
        ]
    )


def test_tenant_isolation(retriever: LexicalRetriever) -> None:
    hits = retriever.search("RAG", tenant_id="tenant-a")
    assert [hit.document.id for hit in hits] == ["1"]


def test_empty_query(retriever: LexicalRetriever) -> None:
    assert retriever.search(" ", tenant_id="tenant-a") == []


def test_invalid_limit(retriever: LexicalRetriever) -> None:
    with pytest.raises(ValueError, match="Limit must be positive"):
        retriever.search("RAG", tenant_id="tenant-a", limit=0)


def test_invalid_tenant(retriever: LexicalRetriever) -> None:
    with pytest.raises(ValueError, match="Tenant ID is required"):
        retriever.search("RAG", tenant_id="")


def test_deterministic_results(retriever: LexicalRetriever) -> None:
    assert retriever.search("RAG", tenant_id="tenant-a") == retriever.search(
        "RAG", tenant_id="tenant-a"
    )


def test_duplicate_document_ids_within_tenant() -> None:
    docs = [Document("1", "a", "t"), Document("1", "b", "t")]
    with pytest.raises(ValueError, match="Duplicate"):
        LexicalRetriever(docs)


def test_duplicate_ids_across_tenants_are_valid() -> None:
    docs = [Document("1", "RAG", "a"), Document("1", "RAG", "b")]
    assert len(LexicalRetriever(docs).search("RAG", tenant_id="a")) == 1


def test_empty_document_rejected() -> None:
    with pytest.raises(ValueError, match="text cannot be empty"):
        Document("1", " ", "a")


def test_unicode_tokenizer() -> None:
    assert tokenize("RAG, VECTOR-search!") == ["rag", "vector", "search"]


def test_ranked_retrieval() -> None:
    retriever = LexicalRetriever(
        [Document("a", "rag rag", "demo"), Document("b", "rag vector", "demo")]
    )
    hits = retriever.search("rag", tenant_id="demo", limit=1)
    assert [hit.document.id for hit in hits] == ["a"]
