from dataclasses import dataclass
from typing import List

@dataclass
class Expense:
    id: int
    title: str
    amount: float
    payer_id: int
    participants_id: List[int]