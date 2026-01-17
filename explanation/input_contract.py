from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class ExplanationInput:
    verdict_status: str                 # PROVABLE only
    conclusion_symbol: str
    proof_steps: List[str]              # Serialized proof steps
