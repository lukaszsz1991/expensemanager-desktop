from dataclasses import dataclass
from typing import List


@dataclass
class Expense:
    id: str
    title: str
    amount_total: float
    my_balance: float
    expense_date: str