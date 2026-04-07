import requests
from models.expense import Expense


class APIClient:

    def __init__(self, base_url):
        # Bazowy URL
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.user_role = None  # Admin czy user?

    def login(self, username, password):
        url = f"{self.base_url}/auth/login"
        headers = {
            "X-API-Version": "1.0.0",
            "Content-Type": "application/json"
        }
        payload = {
            "email": username,
            "password": password
        }

        try:
            # Wysłanie danych jako JSON
            response = self.session.post(url, json=payload, headers=headers, timeout=5)

            if response.status_code == 200:
                data = response.json()
                self.token = data.get("accessToken")
                self.user_role = data.get("role")

                if self.token:
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.token}"
                    })
                    return True
            # Jeśli błąd:
            print(f"Logowanie nieudane. Kod statusu: {response.status_code}")
            print(f"Odpowiedź serwera: {response.text}")
            return False

        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenie: {e}")
            return False

    def get_expenses(self):
        if self.token:
            url = f"{self.base_url}/expenses"

        try:
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            print("RESPONSE DATA:", data)
            expenses_list = data.get("content", [])

            expenses = []

            for item in expenses_list:
                expense = Expense(
                    id=item["id"],
                    title=item["title"],
                    amount_total=item["amountTotal"],
                    my_balance=item["myBalance"],
                    expense_date=item["expenseDate"]
                )
                print(expense)

                expenses.append(expense)

            return expenses
        except requests.exceptions.RequestException as e:
            print(f"Błąd pobierania wydatków: {e}")
            return []
