"""
Skrypt do wypełnienia bazy danych testowymi użytkownikami.
Uruchomienie: python scripts/seed.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from api.client import APIClient
from config import API_BASE_URL, ADMIN_LOGIN, ADMIN_PASSWORD

FIRST_NAMES = [
    "Jan", "Anna", "Piotr", "Maria", "Tomasz", "Katarzyna", "Michał", "Agnieszka",
    "Krzysztof", "Barbara", "Andrzej", "Ewa", "Stanisław", "Małgorzata", "Marek",
    "Monika", "Paweł", "Joanna", "Grzegorz", "Zofia", "Łukasz", "Teresa", "Adam",
    "Halina", "Wojciech", "Irena", "Jacek", "Danuta", "Robert", "Elżbieta",
]

LAST_NAMES = [
    "Kowalski", "Nowak", "Wiśniewski", "Wójcik", "Kamiński", "Kowalczyk",
    "Lewandowski", "Zieliński", "Szymański", "Woźniak", "Dąbrowski", "Kozłowski",
    "Jankowski", "Mazur", "Wojciechowski", "Kwiatkowski", "Krawczyk", "Kaczmarek",
    "Piotrowska", "Grabowska", "Nowicka", "Pawlak", "Michalska", "Adamczyk",
    "Dudek", "Zając", "Wieczorek", "Jabłońska", "Król", "Majewski",
]


def generate_users(count: int) -> list[dict]:
    users = []
    for i in range(count):
        first = FIRST_NAMES[i % len(FIRST_NAMES)]
        last = LAST_NAMES[i % len(LAST_NAMES)]
        email = f"{first.lower()}.{last.lower()}{i + 1}@example.com"
        # Usuń polskie znaki z emaila
        email = (email
                 .replace("ą", "a").replace("ć", "c").replace("ę", "e")
                 .replace("ł", "l").replace("ń", "n").replace("ó", "o")
                 .replace("ś", "s").replace("ź", "z").replace("ż", "z"))
        users.append({
            "email": email,
            "role": "USER",
            "new_password": "Test1234!",
            "repeat_new_password": "Test1234!",
            "first_name": first,
            "last_name": last,
        })
    return users


def main():
    api = APIClient(base_url=API_BASE_URL)

    print(f"Logowanie jako {ADMIN_LOGIN}...")
    if not api.login(ADMIN_LOGIN, ADMIN_PASSWORD):
        print("Logowanie nieudane. Sprawdź dane w config.py.")
        sys.exit(1)

    users = generate_users(50)
    print(f"Zalogowano. Tworzenie {len(users)} użytkowników...\n")

    ok = 0
    fail = 0
    for user in users:
        success, msg = api.create_user(**user)
        status = "✓" if success else "✗"
        info = "" if success else f" — {msg}"
        print(f"  {status} {user['email']}{info}")
        if success:
            ok += 1
        else:
            fail += 1

    print(f"\nGotowe: {ok} utworzonych, {fail} błędów.")


if __name__ == "__main__":
    main()
