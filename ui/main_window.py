# ui/main_window.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, \
    QHBoxLayout, QPushButton

from api.client import APIClient
from ui.users_window import UsersWindow


class MainWindow(QMainWindow):
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api = api_client
        self.users_window = None

        self.setWindowTitle("ExpenseSplitter - Panel Główny")
        self.resize(800, 600)

        central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(10)

        top_bar = QHBoxLayout()
        title = QLabel("Twoje wydatki")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        top_bar.addWidget(title)
        top_bar.addStretch()
        self.layout.addLayout(top_bar)

        if self.api.user_role and "ADMIN" in self.api.user_role.upper():
            users_btn = QPushButton("👥 Użytkownicy")
            users_btn.clicked.connect(self.open_users_window)
            top_bar.addWidget(users_btn)

        # Test (bez autyoryzacji)
        users_btn = QPushButton("👥 Użytkownicy")
        users_btn.clicked.connect(self.open_users_window)
        top_bar.addWidget(users_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Tytuł", "Kwota", "Mój bilans", "Data"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.layout.addWidget(self.table)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def load_data(self):
        self.table.setRowCount(0)
        data = self.api.get_expenses()

        if not data:
            return

        self.table.setRowCount(len(data))

        for row, expense in enumerate(data):
            title_item = QTableWidgetItem(expense.title)

            date = expense.expense_date.split("T")[0] if expense.expense_date else "Brak daty"
            date_item = QTableWidgetItem(date)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            amount_item = QTableWidgetItem(f"{expense.amount_total:.2f} PLN")
            amount_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            balance_text = f"+{expense.my_balance:.2f} PLN" if expense.my_balance > 0 else f"{expense.my_balance:.2f} PLN"
            balance_item = QTableWidgetItem(balance_text)
            balance_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            balance_item.setForeground(QColor("green") if expense.my_balance > 0 else QColor("red"))

            self.table.setItem(row, 0, title_item)
            self.table.setItem(row, 1, date_item)
            self.table.setItem(row, 2, amount_item)
            self.table.setItem(row, 3, balance_item)

    def open_users_window(self):
        if self.users_window is None or not self.users_window.isVisible():
            self.users_window = UsersWindow(self.api)
        self.users_window.show()
        self.users_window.raise_()
        self.users_window.activateWindow()
        self.close()