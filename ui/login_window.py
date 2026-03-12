from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal as Signal, Qt


class LoginWindow(QWidget):
    login_successful = Signal()

    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.setWindowTitle("Logowanie")

        layout = QVBoxLayout()

        self.logo_label = QLabel()
        pixmap = QPixmap("ui/logo.png")
        self.logo_label.setPixmap(pixmap.scaled(150, 150))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)


        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Login (wpisz: admin)")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Hasło: (wpisz: nnn)")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        buttons_layout = QHBoxLayout()
        button_password_forgotten = QPushButton("Zapomniałem hasła")
        buttons_layout.addWidget(button_password_forgotten)
        button_submit = QPushButton("Zaloguj")
        buttons_layout.addWidget(button_submit)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)
        self.resize(300, 500)