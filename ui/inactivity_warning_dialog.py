# ui/inactivity_warning_dialog.py
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


COUNTDOWN_SECONDS = 30


class InactivityWarningDialog(QDialog):
    """
    Okno ostrzegające o zbliżającym się automatycznym wylogowaniu.
    Wyświetla odliczanie i przycisk do pozostania zalogowanym.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Automatyczne wylogowanie")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedSize(360, 160)

        self._seconds_left = COUNTDOWN_SECONDS

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        self._info_label = QLabel()
        self._info_label.setWordWrap(True)
        self._info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._info_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(self._info_label)

        self._countdown_label = QLabel()
        self._countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._countdown_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #c0392b;")
        layout.addWidget(self._countdown_label)

        buttons = QHBoxLayout()
        self._stay_btn = QPushButton("Zostań zalogowany")
        self._stay_btn.setStyleSheet("font-size: 13px; padding: 6px 16px;")
        self._stay_btn.clicked.connect(self.accept)
        buttons.addStretch()
        buttons.addWidget(self._stay_btn)
        buttons.addStretch()
        layout.addLayout(buttons)

        self.setLayout(layout)

        # Timer odliczający co sekundę
        self._tick_timer = QTimer(self)
        self._tick_timer.setInterval(1000)
        self._tick_timer.timeout.connect(self._tick)

        self._update_labels()

    def start_countdown(self):
        self._seconds_left = COUNTDOWN_SECONDS
        self._update_labels()
        self._tick_timer.start()

    def _tick(self):
        self._seconds_left -= 1
        self._update_labels()
        if self._seconds_left <= 0:
            self._tick_timer.stop()
            self.reject()  # czas minął → wylogowanie

    def _update_labels(self):
        self._info_label.setText(
            "Zostałeś/-aś nieaktywny/-a przez dłuższy czas.\n"
            "Za chwilę nastąpi automatyczne wylogowanie."
        )
        self._countdown_label.setText(f"{self._seconds_left} s")

    def closeEvent(self, event):
        # Zamknięcie okna krzyżykiem = wylogowanie
        self._tick_timer.stop()
        self.reject()
        event.accept()
