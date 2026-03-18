from http.client import responses
from os import access

import requests
from models.expense import Expense

class APIClient:

    def __init__(self, base_url):
        # Bazowy URL
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.user_role = None # Admin czy user?

    def login(self, username, password):
        url = f"{self.base_url}/auth/login"
        payload = {
            "username": username,
            "password": password
        }

        try:
            # Wysłanie danych jako JSON
            response = self.session.post(url, json=payload, timeout=5)

            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token") or data.get("access_token")
                self.user_role = data.get("role")

                if self.token:
                    return True
            # Jeśli błąd:
            print(f"Logowanie nieudane. Kod statusu: {response.status_code}")
            return False

        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenie: {e}")
            return False

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

