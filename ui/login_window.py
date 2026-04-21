from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel, QMessageBox, QDialog
from PyQt6.QtCore import pyqtSignal as Signal, Qt


class LoginWindow(QDialog):
    login_successful = Signal()

    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.setWindowTitle("Logowanie")

        layout = QVBoxLayout()

        # Ustawienie modalności
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Dodanie logo
        self.logo_label = QLabel()
        pixmap = QPixmap("ui/logo.png")
        self.logo_label.setPixmap(pixmap.scaled(150, 150))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)

        # Dodanie pola loginu i hasła
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail (np. john.doe@example.com)")
        layout.addWidget(self.email_input)
        self.password_input = QLineEdit()
        self.password_input.returnPressed.connect(self.handle_login)
        self.password_input.setPlaceholderText("Hasło:")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Obsługa przycisku "Zaloguj"
        buttons_layout = QHBoxLayout()
        button_password_forgotten = QPushButton("Zapomniałem hasła")
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
