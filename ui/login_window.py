import sys
import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QMessageBox, QDialog
from PyQt6.QtCore import pyqtSignal as Signal, Qt
from config import TEST, USER_LOGIN, USER_PASSWORD, ADMIN_LOGIN, ADMIN_PASSWORD, resource_path, \
    TEST_ROLE_IS_ADMIN


class LoginWindow(QDialog):
    login_successful = Signal()

    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.setWindowTitle("Logowanie")

        layout = QVBoxLayout()

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        self.logo_label = QLabel()
        pixmap = QPixmap(resource_path("ui/logo.png"))
        self.logo_label.setPixmap(pixmap.scaled(150, 150))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)

        self.email_input = QLineEdit()
        if TEST:
            if TEST_ROLE_IS_ADMIN:
                self.email_input.setText(ADMIN_LOGIN)
            else:
                self.email_input.setText(USER_LOGIN)
        else:
            self.email_input.setPlaceholderText("E-mail (np. john.doe@example.com)")
        layout.addWidget(self.email_input)
        self.password_input = QLineEdit()
        self.password_input.returnPressed.connect(self.handle_login)
        if TEST:
            if TEST_ROLE_IS_ADMIN:
                self.password_input.setText(ADMIN_PASSWORD)
            else:
                self.password_input.setText(USER_PASSWORD)
        else:
            self.password_input.setPlaceholderText("Hasło:")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Obsługa przycisku "Zaloguj"
        buttons_layout = QHBoxLayout()
        button_password_forgotten = QPushButton("Zapomniałem hasła")
        button_password_forgotten.clicked.connect(self._handle_password_forgotten)
        buttons_layout.addWidget(button_password_forgotten)
        self.button_submit = QPushButton("Zaloguj")
        self.button_submit.clicked.connect(self.handle_login)
        buttons_layout.addWidget(self.button_submit)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)
        self.resize(350, 500)

    # Metoda obsługująca przycisk "Zaloguj"
    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        # Wywołanie API
        if self.api.login(email, password):
            self.accept()
        else:
            QMessageBox.warning(self, "Błąd", "Nieprawidłowy login lub/i hasło!")
            self.password_input.clear()

    def _handle_password_forgotten(self):
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning((self, "Błąd", "Wpisz najpier swój e-mail."))
            self.email_input.setFocus()
            return

        success, error_msg = self.api.request_password_reset(email)
        if success:
            QMessageBox.information(
                self,
                "Reset hasła",
                f"Na adres {email} został wysłany e-mail z instrukcjami resetu hasła."
            )
        else:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wysłać resetu hasła.\n{error_msg}")