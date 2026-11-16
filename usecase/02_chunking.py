"""# Use case 02 — Boundary-aware overlapping chunks

## Problem
A fact may straddle two adjacent chunks. A fixed-size split can leave neither
chunk with the complete phrase needed to answer a question.

## Reproduce
```bash
python3 usecase/02_chunking.py
```

## Expected
With size=5 and overlap=0, the phrase "refund within 30 days" is split.
With overlap=3, a chunk contains the entire phrase.

## Limits
This is word-based, not tokenizer-aware. Production chunkers must preserve
Unicode boundaries, structural headings, page/span provenance and token limits.
"""


def chunk_words(text: str, size: int, overlap: int) -> list[str]:
    """Return overlapping word windows with validated progress."""
    if size < 1 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")
    words = text.split()
    step = size - overlap
    return [" ".join(words[i : i + size]) for i in range(0, len(words), step)]


def main() -> None:
    text = "Our annual plan offers a refund within 30 days after purchase"
    phrase = "refund within 30 days"
    for overlap in (0, 3):
        chunks = chunk_words(text, size=5, overlap=overlap)
        print(f"overlap={overlap}: {chunks}")
        print(f"complete evidence present: {any(phrase in c for c in chunks)}")


if __name__ == "__main__":
    main()
