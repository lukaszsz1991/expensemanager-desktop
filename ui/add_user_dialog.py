# ui/add_user_dialog.py
import re

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QPushButton, QLabel, QMessageBox
)

from api.client import APIClient

PASSWORD_REGEX = re.compile(
    r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^a-zA-Z0-9])(?=\S+$).{8,}$'
)
PASSWORD_HINT = (
    "Hasło musi zawierać:\n"
    "  • minimum 8 znaków\n"
    "  • wielką literę (A–Z)\n"
    "  • małą literę (a–z)\n"
    "  • cyfrę (0–9)\n"
    "  • znak specjalny (np. !@#$%^&*)"
)


class AddUserDialog(QDialog):
    def __init__(self, api_client: APIClient, parent=None):
        super().__init__(parent)
        self.api = api_client

        self.setWindowTitle("Dodaj nowego użytkownika")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setFixedSize(430, 420)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(14)

        title = QLabel("Nowy użytkownik")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("john.doe@example.com")
        form.addRow("E-mail *", self.email_input)

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Jane")
        form.addRow("Imię", self.first_name_input)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Doe")
        form.addRow("Nazwisko", self.last_name_input)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["USER", "ADMIN"])
        form.addRow("Rola *", self.role_combo)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Min. 8 znaków, A-z, cyfra, znak spec.")
        self.password_input.setToolTip(PASSWORD_HINT)
        self.password_input.textChanged.connect(self._validate_password_live)
        form.addRow("Hasło *", self.password_input)

        self.password_repeat_input = QLineEdit()
        self.password_repeat_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_repeat_input.setPlaceholderText("Powtórz hasło")
        self.password_repeat_input.returnPressed.connect(self._handle_submit)
        form.addRow("Powtórz hasło *", self.password_repeat_input)

        # Etykieta błędu hasła — widoczna tylko gdy coś jest nie tak
        self.password_error_label = QLabel()
        self.password_error_label.setStyleSheet("color: #c0392b; font-size: 11px;")
        self.password_error_label.setWordWrap(True)
        self.password_error_label.hide()
        form.addRow("", self.password_error_label)

        main_layout.addLayout(form)
        main_layout.addStretch()

        buttons_layout = QHBoxLayout()
        cancel_btn = QPushButton("Anuluj")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        self.submit_btn = QPushButton("Utwórz użytkownika")
        self.submit_btn.setStyleSheet("font-weight: bold;")
        self.submit_btn.clicked.connect(self._handle_submit)
        buttons_layout.addWidget(self.submit_btn)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    def _validate_password_live(self, text: str):
        """Pokazuje podpowiedź na żywo gdy hasło nie spełnia wymagań."""
        if not text:
            self.password_error_label.hide()
            self.password_input.setStyleSheet("")
            return

        if PASSWORD_REGEX.match(text):
            self.password_error_label.hide()
            self.password_input.setStyleSheet("border: 1px solid green;")
        else:
            self.password_error_label.setText(PASSWORD_HINT)
            self.password_error_label.show()
            self.password_input.setStyleSheet("border: 1px solid #c0392b;")

    def _handle_submit(self):
        email = self.email_input.text().strip()
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        role = self.role_combo.currentText()
        password = self.password_input.text()
        repeat_password = self.password_repeat_input.text()

        if not email:
            QMessageBox.warning(self, "Błąd walidacji", "E-mail jest wymagany.")
            self.email_input.setFocus()
            return

        if not password:
            QMessageBox.warning(self, "Błąd walidacji", "Hasło jest wymagane.")
            self.password_input.setFocus()
            return

        if not PASSWORD_REGEX.match(password):
            QMessageBox.warning(self, "Słabe hasło", PASSWORD_HINT)
            self.password_input.setFocus()
            return

        if password != repeat_password:
            QMessageBox.warning(self, "Błąd walidacji", "Hasła nie są identyczne.")
            self.password_repeat_input.clear()
            self.password_repeat_input.setFocus()
            return

        self.submit_btn.setEnabled(False)
        self.submit_btn.setText("Tworzenie...")

        success, error_msg = self.api.create_user(
            email=email,
            role=role,
            first_name=first_name,
            last_name=last_name,
            new_password=password,
            repeat_new_password=repeat_password,
        )

        if success:
            QMessageBox.information(self, "Sukces", f"Użytkownik {email} został utworzony.")
            self.accept()
        else:
            QMessageBox.critical(self, "Błąd", f"Nie udało się utworzyć użytkownika.\n{error_msg}")
            self.submit_btn.setEnabled(True)
            self.submit_btn.setText("Utwórz użytkownika")