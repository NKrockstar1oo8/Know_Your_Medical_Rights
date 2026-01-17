from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class AuditTrail:
    query_id: str
    facts_used: List[str]
    rules_evaluated: List[str]
    verdict_status: str
    proof_ids: List[str]
    refusal: Refusal | None
