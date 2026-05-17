# ExpenseSplitter Desktop

Desktopowa aplikacja do zarządzania wydatkami i użytkownikami, komunikująca się z backendem [wydatkomat.tech](https://www.wydatkomat.tech).

## Uruchomienie

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

pip install PyQt6 requests
python main.py
```

## Konfiguracja

Plik `config.py`:

| Zmienna | Opis | Domyślnie |
|---|---|---|
| `TEST` | Tryb testowy — auto-wypełnienie loginu i hasła | `False` |
| `TEST_ROLE` | Rola w trybie testowym: `"USER"` lub `"ADMIN"` | `"ADMIN"` |
| `MINUTES_TO_LOGOUT` | Czas nieaktywności przed wylogowaniem (minuty) | `15` |
| `SECONDS_TO_WARNING` | Czas odliczania w oknie ostrzeżenia (sekundy) | `30` |
| `API_BASE_URL` | Adres backendu | `https://www.wydatkomat.tech/api` |
