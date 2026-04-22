from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, \
    QHeaderView, QMessageBox, QTableWidgetItem

from api.client import APIClient


class UsersWindow(QWidget):
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api = api_client
        self.current_page = 0
        self.total_pages = 1

        self.setWindowTitle("ExpenseSplitter - Zarządzanie użytkownikami")
        self.resize(900, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        top_layout = QHBoxLayout()
        title = QLabel("Użytkownicy")
        title.setStyleSheet("font-size: 18px; font-weight: bold")
        top_layout.addWidget(title)
        main_window_btn = QPushButton("🏠 Ekran główny")
        main_window_btn.setFixedWidth(240)
        main_window_btn.clicked.connect(self.back_to_main_window)
        top_layout.addWidget(main_window_btn)
        layout.addLayout(top_layout)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Szukaj użytkownika...")
        self.search_input.returnPressed.connect(self._on_search)
        search_layout.addWidget(self.search_input)

        search_btn = QPushButton("Szukaj")
        search_btn.setFixedWidth(240)
        search_layout.addWidget(search_btn)
        search_btn.clicked.connect(self._on_search)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "E-mail", "Imię", "Nazwisko"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        pagination_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Poprzednia")
        self.prev_btn.clicked.connect(self._prev_page)
        self.next_btn = QPushButton("Następna")
        self.next_btn.clicked.connect(self._next_page)
        self.page_level = QLabel("Strona 1 / 1")
        self.page_level.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.page_level)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.next_btn)
        layout.addLayout(pagination_layout)

        self.setLayout(layout)
        QTimer.singleShot(0, self.load_users)

    def load_users(self):
        query = self.search_input.text().strip()
        users, total_pages = self.api.get_users(
            query=query,
            page=self.current_page,
            size=20
        )
        self.total_pages = max(total_pages, 1)
        self._update_pagination()

        self.table.setRowCount(0)
        if not users:
            QMessageBox.information(self, "Brak wyników", "Nie znaleziono użytkowników.")
            return

        self.table.setRowCount(len(users))
        for row, user in enumerate(users):
            id_item = QTableWidgetItem(str(user.id))
            id_item.setForeground(Qt.GlobalColor.gray)
            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, QTableWidgetItem(user.email))
            self.table.setItem(row, 2, QTableWidgetItem(user.first_name))
            self.table.setItem(row, 3, QTableWidgetItem(user.last_name))


    def _on_search(self):
        self.current_page = 0
        self.load_users()

    def _prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_users()

    def _next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_users()

    def _update_pagination(self):
        self.page_level.setText(f"Strona {self.current_page + 1} / {self.total_pages}")
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled((self.current_page < self.total_pages - 1))

    def back_to_main_window(self):
        pass