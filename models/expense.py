from dataclasses import dataclass
from typing import List


@dataclass
class Expense:
    id: str
    title: str
    amount_total: float
    payer_id: int
    participants_id: List[int]
