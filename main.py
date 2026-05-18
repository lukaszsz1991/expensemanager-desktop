import sys
from PyQt6.QtWidgets import QApplication, QDialog

from api.client import APIClient
from config import API_BASE_URL
from ui.main_window import MainWindow
from ui.login_window import LoginWindow
from ui.inactivity_manager import InactivityManager
from ui.inactivity_warning_dialog import InactivityWarningDialog
from ui.users_window import UsersWindow


class ExpenseSplitterApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        # Inicjalizacja API
        self.api_client = APIClient(base_url=API_BASE_URL)

        # Tworzenie okien
        self.login_window = LoginWindow(self.api_client)
        self.main_window = None

        # Menedżer nieaktywności
        self.inactivity_manager = InactivityManager(self.app)
        self.inactivity_manager.show_warning.connect(self._on_inactivity_warning)
        self.inactivity_manager.logout_requested.connect(self._on_auto_logout)

    def run(self):
        if self.login_window.exec() == QDialog.DialogCode.Accepted:
            self._open_main_window()
            return self.app.exec()
        else:
            return 0

    def _open_main_window(self):
        if self.api_client.user_role and "ADMIN" in self.api_client.user_role.upper():
            self.main_window = UsersWindow(self.api_client)
        else:
            self.main_window = MainWindow(self.api_client)
        self.main_window.logout_requested.connect(self._on_auto_logout)
        self.main_window.show()
        if hasattr(self.main_window, 'load_data'):
            self.main_window.load_data()
        self.inactivity_manager.start()

    def _on_inactivity_warning(self):
        dialog = InactivityWarningDialog(self.main_window)
        dialog.start_countdown()
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # Użytkownik kliknął "Zostań zalogowany"
            self.inactivity_manager.reset()
        else:
            # Odliczanie dobiegło końca lub zamknięto okno
            self._on_auto_logout()

    def _on_auto_logout(self):
        self.inactivity_manager.stop()
        self.api_client.logout()

        if self.main_window:
            self.main_window.close()
            self.main_window = None

        self.login_window = LoginWindow(self.api_client)
        if self.login_window.exec() == QDialog.DialogCode.Accepted:
            self._open_main_window()
        else:
            self.app.quit()



if __name__ == "__main__":
    expense_splitter = ExpenseSplitterApp()
    sys.exit(expense_splitter.run())
