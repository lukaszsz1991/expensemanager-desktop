import sys
from PyQt6.QtWidgets import QApplication

from api.client import APIClient
from ui.main_window import MainWindow
from ui.login_window import LoginWindow


def main():
    app = QApplication(sys.argv)

    # Obiekt API
    client = APIClient(base_url="http://localhost:8000")

    # Instancje: okno logowania i główne
    login_win = LoginWindow("api_client")
    main_win = MainWindow()

    # Przełączenie okna
    def login_successful():
        login_win.hide()
        main_win.show()

    login_win.login_successful.connect(login_successful)

    # Startujemy od okna logowania + uruchomienie pętli zdarzeń
    login_win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()