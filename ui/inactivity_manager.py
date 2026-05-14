# ui/inactivity_manager.py
from PyQt6.QtCore import QObject, QTimer, QEvent, pyqtSignal as Signal
from PyQt6.QtWidgets import QApplication
from  config import MINUTES_TO_LOGOUT, SECONDS_TO_WARNING


INACTIVITY_TIMEOUT_MS = MINUTES_TO_LOGOUT * 60 * 1000
WARNING_BEFORE_MS = SECONDS_TO_WARNING * 1000
WARNING_AT_MS = INACTIVITY_TIMEOUT_MS - WARNING_BEFORE_MS


class InactivityManager(QObject):
    show_warning = Signal()
    logout_requested = Signal()

    def __init__(self, app: QApplication, parent=None):
        super().__init__(parent)
        self._app = app

        self._warning_timer = QTimer(self)
        self._warning_timer.setSingleShot(True)
        self._warning_timer.setInterval(WARNING_AT_MS)
        self._warning_timer.timeout.connect(self.show_warning)

        self._logout_timer = QTimer(self)
        self._logout_timer.setSingleShot(True)
        self._logout_timer.setInterval(WARNING_BEFORE_MS)
        self._logout_timer.timeout.connect(self.logout_requested)

        self._app.installEventFilter(self)

    def start(self):
        self._warning_timer.start()
        self._logout_timer.stop()

    def stop(self):
        self._warning_timer.stop()
        self._logout_timer.stop()

    def reset(self):
        self._logout_timer.stop()
        self._warning_timer.start()

    def eventFilter(self, obj, event):
        activity_events = (
            QEvent.Type.MouseMove,
            QEvent.Type.MouseButtonPress,
            QEvent.Type.KeyPress,
        )
        if event.type() in activity_events:
            if self._warning_timer.isActive():
                self._warning_timer.start()
        return False
