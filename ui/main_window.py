# ui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.api = api_client
        self.setWindowTitle("ExpenseSplitter - Panel Główny")
        self.resize(800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Zalogowano pomyślnie! Tu będą Twoje wydatki."))

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)