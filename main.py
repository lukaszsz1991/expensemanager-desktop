import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Tworzymy i pokazujemy główne okno
    window = MainWindow()
    window.show()

    # Uruchamiamy pętlę zdarzeń
    sys.exit(app.exec())


if __name__ == "__main__":
    main()