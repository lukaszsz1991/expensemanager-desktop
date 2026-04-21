import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtCore import Qt

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
        self.main_window = MainWindow(self.api_client)

    def run(self):
        if self.login_window.exec() == QDialog.DialogCode.Accepted:
            self.main_window.show()
            self.main_window.load_data()
            return self.app.exec()
        else:
            return 0

if __name__ == "__main__":
    # Tworzymy instancję zarządcy i odpalamy
    expense_splitter = ExpenseSplitterApp()
    sys.exit(expense_splitter.run())
