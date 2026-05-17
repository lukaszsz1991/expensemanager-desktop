# ui/user_details_dialog.py
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QPushButton, QFrame, QMessageBox, QLineEdit, QComboBox
)

from api.client import APIClient


class UserDetailsDialog(QDialog):
    user_changed = pyqtSignal()

    def __init__(self, api_client: APIClient, user_id: str, parent=None):
        super().__init__(parent)
        self.api = api_client
        self._user_id = user_id

        self.setWindowTitle("Szczegóły użytkownika")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setFixedSize(460, 460)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(14)

        title = QLabel("Szczegóły użytkownika")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._id_label = QLabel()
        self._id_label.setStyleSheet("color: gray; font-size: 11px;")
        self._id_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        form.addRow("ID:", self._id_label)

        self._email_input = QLineEdit()
        form.addRow("E-mail:", self._email_input)

        self._first_name_input = QLineEdit()
        form.addRow("Imię:", self._first_name_input)

        self._last_name_input = QLineEdit()
        form.addRow("Nazwisko:", self._last_name_input)

        self._role_combo = QComboBox()
        self._role_combo.addItems(["USER", "ADMIN"])
        form.addRow("Rola:", self._role_combo)

        self._2fa_label = QLabel()
        form.addRow("2FA:", self._2fa_label)

        self._identities_label = QLabel()
        self._identities_label.setWordWrap(True)
        form.addRow("Dostawcy:", self._identities_label)

        self._created_label = QLabel()
        form.addRow("Utworzono:", self._created_label)

        self._updated_label = QLabel()
        form.addRow("Zaktualizowano:", self._updated_label)

        deleted_layout = QHBoxLayout()
        self._deleted_label = QLabel()

        deleted_layout.addWidget(self._deleted_label)

        self._delete_btn = QPushButton("🗑 Usuń użytkownika")
        self._delete_btn.setStyleSheet("color: #c0392b;")
        self._delete_btn.clicked.connect(self._handle_delete)
        deleted_layout.addWidget(self._delete_btn)
        deleted_layout.addStretch()
        form.addRow("Usunięto:", self._deleted_label)

        main_layout.addLayout(form)
        main_layout.addLayout(deleted_layout)
        main_layout.addStretch()

        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line2)

        buttons = QHBoxLayout()

        reset_btn = QPushButton("🔑 Resetuj hasło")
        reset_btn.clicked.connect(self._handle_reset_password)
        buttons.addWidget(reset_btn)

        change_pwd_btn = QPushButton("🔒 Zmień hasło")
        change_pwd_btn.clicked.connect(self._handle_change_password)
        buttons.addWidget(change_pwd_btn)

        buttons.addStretch()

        self._save_btn = QPushButton("💾 Zapisz zmiany")
        self._save_btn.setStyleSheet("font-weight: bold;")
        self._save_btn.clicked.connect(self._handle_save)
        buttons.addWidget(self._save_btn)

        main_layout.addLayout(buttons)
        self.setLayout(main_layout)
        self._load_user(user_id)

    def _load_user(self, user_id: str):
        data, error = self.api.get_user_details(user_id)

        if error:
            self._id_label.setText(f"Błąd: {error}")
            return

        self._id_label.setText(data.get("id", "—"))
        self._email_input.setText(data.get("email", ""))
        self._first_name_input.setText(data.get("firstName") or "")
        self._last_name_input.setText(data.get("lastName") or "")

        role = data.get("role", "USER")
        index = self._role_combo.findText(role)
        if index >= 0:
            self._role_combo.setCurrentIndex(index)

        self._2fa_label.setText("✅ Włączone" if data.get("isTwoFactorAuthEnabled") else "❌ Wyłączone")

        identities = data.get("identities", [])
        if identities:
            providers = ", ".join(i.get("provider", "") for i in identities)
            self._identities_label.setText(providers)
        else:
            self._identities_label.setText("Brak")

        self._created_label.setText(self._fmt_date(data.get("createdAt")))
        self._updated_label.setText(self._fmt_date(data.get("updatedAt")))

        deleted = data.get("deletedAt")
        if deleted:
            self._deleted_label.setText(self._fmt_date(deleted))
            self._deleted_label.setStyleSheet("color: #c0392b;")
        else:
            self._deleted_label.setText("—")

    def _handle_save(self):
        email = self._email_input.text().strip()
        first_name = self._first_name_input.text().strip()
        last_name = self._last_name_input.text().strip()
        role = self._role_combo.currentText()

        if not email:
            QMessageBox.warning(self, "Błąd walidacji", "E-mail jest wymagany.")
            self._email_input.setFocus()
            return

        self._save_btn.setEnabled(False)
        self._save_btn.setText("Zapisywanie...")

        success, error_msg = self.api.update_user(
            user_id=self._user_id,
            email=email,
            role=role,
            first_name=first_name,
            last_name=last_name,
        )

        if success:
            QMessageBox.information(self, "Sukces", "Dane użytkownika zostały zaktualizowane.")
            self.user_changed.emit()
            self._load_user(self._user_id)
        else:
            QMessageBox.critical(self, "Błąd", f"Nie udało się zaktualizować danych.\n{error_msg}")

        self._save_btn.setEnabled(True)
        self._save_btn.setText("💾 Zapisz zmiany")

    def _handle_reset_password(self):
        if not self._confirm(f"Czy na pewno chcesz wysłać reset hasła dla:\n{self._email_input.text()}?"):
            return

        success, error_msg = self.api.reset_user_password(self._user_id)
        if success:
            QMessageBox.information(self, "Sukces", "E-mail z resetem hasła został wysłany.")
        else:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wysłać resetu hasła.\n{error_msg}")

    def _handle_delete(self):
        if not self._confirm(
                f"Czy na pewno chcesz usunąć użytkownika:\n{self._email_input.text()}?\n\nOperacja jest nieodwracalna."):
            return

        success, error_msg = self.api.delete_user(self._user_id)
        if success:
            QMessageBox.information(self, "Sukces", "Użytkownik został usunięty.")
            self.user_changed.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "Błąd", f"Nie udało się usunąć użytkownika.\n{error_msg}")

    def _confirm(self, message: str) -> bool:
        msg = QMessageBox(self)
        msg.setWindowTitle("Potwierdzenie")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Question)
        tak_btn = msg.addButton("Tak", QMessageBox.ButtonRole.YesRole)
        msg.addButton("Nie", QMessageBox.ButtonRole.NoRole)
        msg.exec()
        return msg.clickedButton() == tak_btn

    @staticmethod
    def _fmt_date(value: str | None) -> str:
        if not value:
            return "—"
        try:
            date, time = value.split("T")
            return f"{date} {time[:5]}"
        except Exception:
            return value

    def _handle_change_password(self):
        from ui.change_password_dialog import ChangePasswordDialog
        dialog = ChangePasswordDialog(
            self.api,
            self._user_id,
            self._email_input.text(),
            parent=self
        )
        dialog.exec()