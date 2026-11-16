"""# Use case 05 — Authorization and idempotency for an agent tool

## Problem
A tool-using agent proposes a refund. A model's proposed action is not proof
that the caller is authorized to issue that refund.

## Sample
Order O1 belongs to customer C1 and is refundable up to 5,000 units.
Customer C2 must be denied; C1 may refund 1,000 once, not twice.

## Reproduce
```bash
python3 usecase/05_agent_authorization.py
```

## Limits
TrustedContext is a stand-in for server-verified identity; do not construct it
from an untrusted LLM message. Real systems need atomic durable idempotency,
audit logs, role checks, transaction boundaries and approval for high risk.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TrustedContext:
    customer_id: str


@dataclass
class RefundService:
    owner: str = "C1"
    refundable_amount: int = 5000
    processed: set[str] = field(default_factory=set)

    def refund(self, ctx: TrustedContext, amount: int, key: str) -> str:
        """Authorize before issuing a refund; reject replay of a key."""
        if ctx.customer_id != self.owner:
            return "DENIED: order does not belong to caller"
        if not key or amount <= 0 or amount > self.refundable_amount:
            return "DENIED: invalid amount or idempotency key"
        if key in self.processed:
            return "DUPLICATE: refund already processed"
        self.processed.add(key)
        self.refundable_amount -= amount
        return f"APPROVED: refund={amount}, remaining={self.refundable_amount}"


def main() -> None:
    service = RefundService()
    print(service.refund(TrustedContext("C2"), 1000, "req-1"))
    print(service.refund(TrustedContext("C1"), 1000, "req-1"))
    print(service.refund(TrustedContext("C1"), 1000, "req-1"))


if __name__ == "__main__":
    main()
