"""Main Application Window."""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QStatusBar,
    QLabel,
)
from app.state.session_store import SessionStore
from app.state.contacts_store import ContactsStore
from app.state.settings_store import SettingsStore
from app.ui.widgets.search_bar import SearchBar
from app.ui.widgets.contacts_table import ContactsTableView
from app.ui.dialogs.contact_edit_dialog import ContactEditDialog
from app.ui.dialogs.settings_dialog import SettingsDialog
from app.domain.models import ContactItem


class MainWindow(QMainWindow):
    def __init__(
        self,
        session_store: SessionStore,
        contacts_store: ContactsStore,
        settings_store: SettingsStore,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.session_store = session_store
        self.contacts_store = contacts_store
        self.settings_store = settings_store

        self.setWindowTitle("CloudPhoneBook — Twoje kontakty")
        self.resize(900, 600)

        # Central Widget & Layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # Top Action Bar
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setSpacing(10)

        self.search_bar = SearchBar(self)
        self.add_contact_btn = QPushButton("+ Dodaj kontakt", self)
        self.refresh_btn = QPushButton("Odswiez", self)
        self.refresh_btn.setObjectName("secondaryButton")
        self.settings_btn = QPushButton("Ustawienia", self)
        self.settings_btn.setObjectName("secondaryButton")
        self.logout_btn = QPushButton("Wyloguj", self)
        self.logout_btn.setObjectName("secondaryButton")

        top_bar_layout.addWidget(self.search_bar, stretch=1)
        top_bar_layout.addWidget(self.add_contact_btn)
        top_bar_layout.addWidget(self.refresh_btn)
        top_bar_layout.addWidget(self.settings_btn)
        top_bar_layout.addWidget(self.logout_btn)

        main_layout.addLayout(top_bar_layout)

        # Contacts Table View
        self.table_view = ContactsTableView(self)
        main_layout.addWidget(self.table_view, stretch=1)

        # Status Bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("Liczba kontaktow: 0", self)
        self.user_label = QLabel("", self)
        self.status_bar.addWidget(self.status_label)
        self.status_bar.addPermanentWidget(self.user_label)

        # Connect Signals
        self.search_bar.search_triggered.connect(self._on_search)
        self.add_contact_btn.clicked.connect(self._on_add_contact)
        self.refresh_btn.clicked.connect(self._on_refresh)
        self.settings_btn.clicked.connect(self._on_open_settings)
        self.logout_btn.clicked.connect(self._on_logout)

        self.table_view.edit_requested.connect(self._on_edit_contact)
        self.table_view.delete_requested.connect(self._on_delete_contact)

        self.contacts_store.contacts_loaded.connect(self._on_contacts_loaded)
        self.contacts_store.error_occurred.connect(self._show_error)

        self._update_user_display()

    def load_initial_data(self) -> None:
        self._update_user_display()
        self.contacts_store.load_cached()
        self.contacts_store.fetch_contacts()
        self.settings_store.fetch_settings()

    def _update_user_display(self) -> None:
        if self.session_store.current_session:
            self.user_label.setText(f"Zalogowany jako: {self.session_store.current_session.email}")
        else:
            self.user_label.setText("")

    def _on_search(self, query: str) -> None:
        self.contacts_store.fetch_contacts(query=query)

    def _on_refresh(self) -> None:
        self.search_bar.clear()
        self.contacts_store.fetch_contacts()

    def _on_contacts_loaded(self, contacts: list[ContactItem]) -> None:
        self.table_view.update_contacts(contacts)
        self.status_label.setText(f"Liczba kontaktow: {len(contacts)}")

    def _on_add_contact(self) -> None:
        dialog = ContactEditDialog(parent=self)
        if dialog.exec() == ContactEditDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.contacts_store.add_contact(data)

    def _on_edit_contact(self, contact: ContactItem) -> None:
        dialog = ContactEditDialog(contact=contact, parent=self)
        if dialog.exec() == ContactEditDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.contacts_store.update_contact(contact.id, data)

    def _on_delete_contact(self, contact: ContactItem) -> None:
        reply = QMessageBox.question(
            self,
            "Potwierdzenie usuniecia",
            f"Czy na pewno chcesz usunac kontakt: {contact.full_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.contacts_store.delete_contact(contact.id)

    def _on_open_settings(self) -> None:
        dialog = SettingsDialog(settings_store=self.settings_store, parent=self)
        dialog.exec()

    def _on_logout(self) -> None:
        reply = QMessageBox.question(
            self,
            "Wylogowanie",
            "Czy na pewno chcesz sie wylogowac?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.session_store.logout()
            self.close()

    def _show_error(self, error_msg: str) -> None:
        self.status_bar.showMessage(f"Blad: {error_msg}", 5000)
