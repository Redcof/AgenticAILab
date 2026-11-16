"""Framework-independent domain contracts."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Document:
    """A document in one tenant's search corpus."""

    id: str
    text: str
    tenant_id: str

    def __post_init__(self) -> None:
        if not self.id or not self.id.strip():
            raise ValueError("Document ID is required")
        if not self.tenant_id or not self.tenant_id.strip():
            raise ValueError("Tenant ID is required")
        if not self.text or not self.text.strip():
            raise ValueError("Document text cannot be empty")


@dataclass(frozen=True, slots=True)
class SearchHit:
    """Retrieved document with a cosine similarity score."""

    document: Document
    score: float
