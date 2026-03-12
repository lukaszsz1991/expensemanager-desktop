from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Expanse Manager Desktop")
        self.resize(800, 600)

        # Główny układ (Layout)
        layout = QVBoxLayout()

        self.label = QLabel("Witaj w aplikacji do wydatków!")
        layout.addWidget(self.label)

        self.btn = QPushButton("Pobierz moje wydatki")
        self.btn.clicked.connect(self.on_button_click)
        layout.addWidget(self.btn)

        # Ustawienie głównego kontenera
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_button_click(self):
        self.label.setText("Łączenie z API...")
        print("Tu w przyszłości wywołamy funkcję z folderu api/")