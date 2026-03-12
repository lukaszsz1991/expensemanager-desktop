import requests
from models.expense import Expense

class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

    def login(self, username, password):
        pass

    def get_expenses(self):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        response = requests.get(f"{self.base_url}/expenses", headers=headers)
        data = response.json()

        expenses = []

        for item in data:
            expense = Expense(
                id=item["id"],
                title=item["title"],
                amount=item["amount"],
                payer_id=item["payer_id"],
                participants_id=item["participants_id"]
            )

            expenses.append(expense)

        return expenses

