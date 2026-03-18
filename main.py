import sys
from PyQt6.QtWidgets import QApplication

from api.client import APIClient
from ui.main_window import MainWindow
from ui.login_window import LoginWindow

class ExpenseSplitterApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Inicjalizacja API
        self.api_client = APIClient(base_url="http://localhost:8080/api")

        # Tworzenie okien
        self.login_window = LoginWindow(self.api_client)
        self.main = None # Tworzone dopiero po zalogowaniu

        # Przełączenie okiem po zalogowaniu
        self.login_window.login_successful.connect(self.start_main_app)

    def run(self):
        self.login_window.show()
        return self.app.exec()

    def start_main_app(self):
        self.main_window = MainWindow(self.api_client)
        self.main_window.show()
        self.login_window.close()

if __name__ == "__main__":
    # Tworzymy instancję zarządcy i odpalamy
    expense_splitter = ExpenseSplitterApp()
    sys.exit(expense_splitter.run())