from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QHeaderView, QMessageBox, QTableWidgetItem
)

from api.client import APIClient
from ui.add_user_dialog import AddUserDialog


class UsersWindow(QWidget):
    logout_requested = pyqtSignal()
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

        add_user_btn = QPushButton("➕ Dodaj użytkownika")
        add_user_btn.clicked.connect(self.open_add_user_dialog)
        top_layout.addWidget(add_user_btn)

        logout_btn = QPushButton("🚪 Wyloguj")
        logout_btn.clicked.connect(self.logout_requested)
        top_layout.addWidget(logout_btn)
        layout.addLayout(top_layout)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Szukaj użytkownika...")
        self.search_input.returnPressed.connect(self._on_search)
        search_layout.addWidget(self.search_input)

        search_btn = QPushButton("Szukaj")
        search_btn.setFixedWidth(240)
        search_btn.clicked.connect(self._on_search)
        search_layout.addWidget(search_btn)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "E-mail", "Rola", "Data utworzenia"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
        header.resizeSection(0, 300)
        header.resizeSection(1, 340)
        header.resizeSection(2, 80)
        header.resizeSection(3, 160)
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

        self.table.cellDoubleClicked.connect(self._on_row_double_clicked)

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

            role_item = QTableWidgetItem(user.role)
            role_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, role_item)

            date = user.created_at.split("T")[0] if user.created_at else ""
            date_item = QTableWidgetItem(date)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, date_item)

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
        self.next_btn.setEnabled(self.current_page < self.total_pages - 1)

    def _on_row_double_clicked(self, row: int, column: int):
        id_item = self.table.item(row, 0)
        if id_item:
            from ui.user_details_dialog import UserDetailsDialog
            dialog = UserDetailsDialog(self.api, id_item.text(), parent=self)
            dialog.user_changed.connect(self.load_users)
            dialog.exec()

    def open_add_user_dialog(self):
        dialog = AddUserDialog(self.api, parent=self)
        dialog.exec()
