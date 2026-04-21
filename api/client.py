import requests
from models.expense import Expense
from models.user import User


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
        if not self.token:
            return []

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

    def get_users(self, query: str = "", page: int = 0, size: int = 20):
        if not self.token:
            return [], 0
        url = f"{self.base_url}/users"
        params = {
            "query": query,
            "page": page,
            "size": size,
        }

        try:
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            users_list = data.get("content", [])
            total_pages = data.get("page", {}).get("totalPages", 1)
            users = [
                User(
                    id=item["id"],
                    email=item["email"],
                    first_name=item.get("firstName", ""),
                    last_name=item.get("lastName", "")
                )
                for item in users_list
            ]
            return users, total_pages
        except requests.exceptions.RequestException as e:
            print(f"Błąd pobierania użytkownikiów: {e}")
            return [], 0