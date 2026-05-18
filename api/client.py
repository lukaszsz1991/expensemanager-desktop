import requests, base64, json
from models.expense import Expense
from models.user import User


class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.user_role = None

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
            response = self.session.post(url, json=payload, headers=headers, timeout=5)

            if response.status_code == 200:
                data = response.json()
                print(f"Login response: {data}")  # ← dodaj tę linię
                self.token = data.get("accessToken")
                self.user_role = self._decode_role_from_token(self.token)

                if self.token:
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.token}"
                    })
                    print(f"Ustawiam user_role: {self.user_role}")
                    return True

            print(f"Logowanie nieudane. Kod statusu: {response.status_code}")
            print(f"Odpowiedź serwera: {response.text}")
            return False

        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenia: {e}")
            return False

    def get_expenses(self):
        if not self.token:
            return []

        url = f"{self.base_url}/expenses"

        try:
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            # w get_expenses, po data = response.json()
            print("EXPENSES RESPONSE:", data)
            expenses_list = data.get("content", [])

            expenses = []
            for item in expenses_list:
                expense = Expense(
                    id=item["id"],
                    title=item["title"],
                    amount_total=item.get("amountTotal", 0.0),
                    expense_date=item["expenseDate"],
                    role=item.get("role", ""),
                    my_balance=item.get("myBalance", 0.0)

                )
                expenses.append(expense)

            return expenses
        except requests.exceptions.RequestException as e:
            print(f"Błąd pobierania wydatków: {e}")
            return []

    def get_users(self, query: str = "", page: int = 0, size: int = 20):
        if not self.token:
            return [], 0

        url = f"{self.base_url}/admin/users"
        params = {
            "query": query,
            "page": page,
            "size": size,
        }
        headers = {"X-API-Version": "1.0.0"}

        try:
            response = self.session.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            users_list = data.get("content", [])
            total_pages = data.get("page", {}).get("totalPages", 1)
            users = [
                User(
                    id=item["id"],
                    email=item["email"],
                    role=item.get("role", ""),
                    created_at=item.get("createdAt", "")
                )
                for item in users_list
            ]
            return users, total_pages
        except requests.exceptions.RequestException as e:
            print(f"Błąd pobierania użytkowników: {e}")
            return [], 0

    def get_user_details(self, user_id: str) -> tuple[dict, str]:
        if not self.token:
            return {}, "Brak autoryzacji."

        url = f"{self.base_url}/admin/users/{user_id}"
        headers = {"X-API-Version": "1.0.0"}

        try:
            response = self.session.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            return response.json(), ""
        except requests.exceptions.RequestException as e:
            print(f"Błąd pobierania szczegółów użytkownika {user_id}: {e}")
            return {}, str(e)

    def create_user(
            self,
            email: str,
            role: str,
            new_password: str,
            repeat_new_password: str,
            first_name: str = "",
            last_name: str = "",
    ) -> tuple[bool, str]:
        if not self.token:
            return False, "Brak autoryzacji."

        url = f"{self.base_url}/admin/users"
        headers = {"X-API-Version": "1.0.0"}
        payload = {
            "email": email,
            "role": role,
            "newPassword": new_password,
            "repeatNewPassword": repeat_new_password,
        }

        if first_name:
            payload["firstName"] = first_name
        if last_name:
            payload["lastName"] = last_name

        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=5)
            if response.status_code == 201:
                return True, ""
            try:
                error_data = response.json()
                msg = error_data.get("message") or error_data.get("detail") or str(response.status_code)
            except Exception:
                msg = f"Kod HTTP: {response.status_code}"
            print(f"Błąd tworzenia użytkownika: {response.status_code} - {response.text}")
            return False, msg
        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenia przy tworzeniu użytkownika: {e}")
            return False, str(e)

    def reset_user_password(self, user_id: str) -> tuple[bool, str]:
        """
        Wysyła żądanie resetu hasła dla użytkownika.
        Użytkownik otrzyma e-mail z instrukcjami.
        """
        if not self.token:
            return False, "Brak autoryzacji."

        url = f"{self.base_url}/admin/users/{user_id}/reset-password"
        headers = {"X-API-Version": "1.0.0"}

        try:
            response = self.session.post(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return True, ""
            try:
                error_data = response.json()
                msg = error_data.get("message") or error_data.get("detail") or str(response.status_code)
            except Exception:
                msg = f"Kod HTTP: {response.status_code}"
            print(f"Błąd resetu hasła: {response.status_code} - {response.text}")
            return False, msg
        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenia przy resecie hasła: {e}")
            return False, str(e)

    def change_user_password(self, user_id: str, new_password: str, repeat_new_password: str) -> tuple[bool, str]:
        if not self.token:
            return False, "Brak autoryzacji."

        url = f"{self.base_url}/admin/users/{user_id}/password"
        headers = {"X-API-Version": "1.0.0"}
        payload = {
            "newPassword": new_password,
            "repeatNewPassword": repeat_new_password,
        }

        try:
            response = self.session.patch(url, json=payload, headers=headers, timeout=5)
            if response.status_code == 200:
                return True, ""
            try:
                error_data = response.json()
                msg = error_data.get("message") or error_data.get("detail") or str(response.status_code)
            except Exception:
                msg = f"Kod HTTP: {response.status_code}"
            print(f"Błąd zmiany hasła: {response.status_code} - {response.text}")
            return False, msg
        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenia przy zmianie hasła: {e}")
            return False, str(e)

    def update_user(self, user_id: str, email: str, role: str, first_name: str = "", last_name: str = "") -> tuple[
        bool, str]:
        if not self.token:
            return False, "Brak autoryzacji."

        url = f"{self.base_url}/admin/users/{user_id}"
        headers = {"X-API-Version": "1.0.0"}
        payload = {
            "email": email,
            "role": role,
        }
        if first_name:
            payload["firstName"] = first_name
        if last_name:
            payload["lastName"] = last_name

        try:
            response = self.session.patch(url, json=payload, headers=headers, timeout=5)
            if response.status_code == 200:
                return True, ""
            try:
                error_data = response.json()
                msg = error_data.get("message") or error_data.get("detail") or str(response.status_code)
            except Exception:
                msg = f"Kod HTTP: {response.status_code}"
            print(f"Błąd aktualizacji użytkownika: {response.status_code} - {response.text}")
            return False, msg
        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenia przy aktualizacji użytkownika: {e}")
            return False, str(e)

    def delete_user(self, user_id: str) -> tuple[bool, str]:
        if not self.token:
            return False, "Brak autoryzacji."

        url = f"{self.base_url}/admin/users/{user_id}"
        headers = {"X-API-Version": "1.0.0"}

        try:
            response = self.session.delete(url, headers=headers, timeout=5)
            if response.status_code == 204:
                return True, ""
            try:
                error_data = response.json()
                msg = error_data.get("message") or error_data.get("detail") or str(response.status_code)
            except Exception:
                msg = f"Kod HTTP: {response.status_code}"
            print(f"Błąd usuwania użytkownika: {response.status_code} - {response.text}")
            return False, msg
        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenia przy usuwaniu użytkownika: {e}")
            return False, str(e)

    def _decode_role_from_token(self, token: str) -> str | None:
        try:
            payload = token.split(".")[1]
            # base64 wymaga dopełnienia do wielokrotności 4
            payload += "=" * (4 - len(payload) % 4)
            data = json.loads(base64.b64decode(payload))
            roles = data.get("roles", [])
            return roles[0] if roles else None
        except Exception as e:
            print(f"Błąd dekodowania tokenu: {e}")
            return None

    def logout(self):
        self.token = None
        self.user_role = None
        self.session.headers.pop("Authorization", None)

    def request_password_reset(self, email: str) -> tuple[bool, str]:
        url = f"{self.base_url}/auth/reset-password"
        headers = {"X-API-Version": "1.0.0"}
        payload = {"email": email}

        try:
            response = self.session.post(url, json=payload, headers=headers, timeout=5)
            if response.status_code == 204:
                return True, ""
            try:
                error_data = response.json()
                msg = error_data.get("message") or error_data.get("detail") or str(response.status_code)
            except Exception:
                msg = f"Kod HTTP: {response.status_code}"
            print(f"Błąd resetu hasła: {response.status_code} - {response.text}")
            return False, msg
        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenia przy resecie hasła: {e}")
            return False, str(e)


