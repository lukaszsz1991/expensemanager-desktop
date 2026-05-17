import re

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox
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


class ChangePasswordDialog(QDialog):
    def __init__(self, api_client: APIClient, user_id: str, user_email: str, parent=None):
        super().__init__(parent)
        self.api = api_client
        self._user_id = user_id

        self.setWindowTitle("Zmiana hasła")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setFixedSize(400, 260)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(14)

        title = QLabel("Zmiana hasła użytkownika")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)

        subtitle = QLabel(f"Użytkownik: {user_email}")
        subtitle.setStyleSheet("color: gray; font-size: 12px;")
        main_layout.addWidget(subtitle)

        form = QFormLayout()
        form.setSpacing(10)

        self._password_input = QLineEdit()
        self._password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._password_input.setPlaceholderText("Min. 8 znaków, A-z, cyfra, znak spec.")
        self._password_input.setToolTip(PASSWORD_HINT)
        self._password_input.textChanged.connect(self._validate_live)
        form.addRow("Nowe hasło *", self._password_input)

        self._password_repeat_input = QLineEdit()
        self._password_repeat_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._password_repeat_input.setPlaceholderText("Powtórz hasło")
        self._password_repeat_input.returnPressed.connect(self._handle_submit)
        form.addRow("Powtórz hasło *", self._password_repeat_input)

        self._error_label = QLabel()
        self._error_label.setStyleSheet("color: #c0392b; font-size: 11px;")
        self._error_label.setWordWrap(True)
        self._error_label.hide()
        form.addRow("", self._error_label)

        main_layout.addLayout(form)
        main_layout.addStretch()

        buttons = QHBoxLayout()
        cancel_btn = QPushButton("Anuluj")
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(cancel_btn)

        self._submit_btn = QPushButton("Zmień hasło")
        self._submit_btn.setStyleSheet("font-weight: bold;")
        self._submit_btn.clicked.connect(self._handle_submit)
        buttons.addWidget(self._submit_btn)

        main_layout.addLayout(buttons)
        self.setLayout(main_layout)

    def _validate_live(self, text: str):
        if not text:
            self._error_label.hide()
            self._password_input.setStyleSheet("")
            return

        if PASSWORD_REGEX.match(text):
            self._error_label.hide()
            self._password_input.setStyleSheet("border: 1px solid green;")
        else:
            self._error_label.setText(PASSWORD_HINT)
            self._error_label.show()
            self._password_input.setStyleSheet("border: 1px solid #c0392b;")

    def _handle_submit(self):
        password = self._password_input.text()
        repeat_password = self._password_repeat_input.text()

        if not password:
            QMessageBox.warning(self, "Błąd walidacji", "Hasło jest wymagane.")
            self._password_input.setFocus()
            return

        if not PASSWORD_REGEX.match(password):
            QMessageBox.warning(self, "Słabe hasło", PASSWORD_HINT)
            self._password_input.setFocus()
            return

        if password != repeat_password:
            QMessageBox.warning(self, "Błąd walidacji", "Hasła nie są identyczne.")
            self._password_repeat_input.clear()
            self._password_repeat_input.setFocus()
            return

        self._submit_btn.setEnabled(False)
        self._submit_btn.setText("Zapisywanie...")

        success, error_msg = self.api.change_user_password(
            user_id=self._user_id,
            new_password=password,
            repeat_new_password=repeat_password,
        )

        if success:
            QMessageBox.information(self, "Sukces", "Hasło zostało zmienione.")
            self.accept()
        else:
            QMessageBox.critical(self, "Błąd", f"Nie udało się zmienić hasła.\n{error_msg}")
            self._submit_btn.setEnabled(True)
            self._submit_btn.setText("Zmień hasło")