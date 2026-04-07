# ui/main_window.py
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView

from api.client import APIClient
from models import expense
from models.expense import Expense


class MainWindow(QMainWindow):
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api = api_client
        self.setWindowTitle("ExpenseSplitter - Panel Główny")
        self.resize(800, 600)

        central_widget = QWidget()
        self.layout = QVBoxLayout()
        title = QLabel("Twoje wydatki")
        self.layout.addWidget(title)

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