from dataclasses import dataclass
from typing import List


@dataclass
class Expense:
    id: str
    title: str
    amount_total: float
    expense_date: str
    my_balance: float = 0.0
    role: str = ""