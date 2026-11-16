"""# Use case 01 — Current-policy retrieval and abstention

## Problem
An LLM may know an outdated refund policy. The retrieval layer must select
evidence that is currently effective, and abstain if none supports the query.

## Sample data
- Policy v1: refund window 14 days, effective 2025-01-01.
- Policy v2: refund window 30 days, effective 2026-01-01.

## Reproduce
```bash
python3 usecase/01_foundations.py
```

## Expected
The current policy returns 30 days. A missing warranty policy returns no
answer rather than a fabricated value.

## Limits
Keyword filtering and dates are illustrative; production retrieval requires
document ACLs, provenance, robust search and explicit policy authority.
"""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Policy:
    topic: str
    effective: date
    value: str
    source: str


POLICIES = (
    Policy("refund", date(2025, 1, 1), "14 days", "policy-v1"),
    Policy("refund", date(2026, 1, 1), "30 days", "policy-v2"),
)


def retrieve_policy(topic: str, as_of: date) -> Policy | None:
    eligible = [p for p in POLICIES if p.topic == topic and p.effective <= as_of]
    return max(eligible, key=lambda p: p.effective) if eligible else None


def answer(topic: str, as_of: date) -> str:
    policy = retrieve_policy(topic, as_of)
    return (
        f"{topic}: {policy.value} [source={policy.source}]"
        if policy
        else f"{topic}: cannot verify from available evidence"
    )


def main() -> None:
    print(answer("refund", date(2026, 11, 16)))
    print(answer("warranty", date(2026, 11, 16)))


if __name__ == "__main__":
    main()
