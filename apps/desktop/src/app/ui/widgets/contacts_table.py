"""Contacts Table widget with custom Model/View and context menu."""

from PySide6.QtWidgets import QTableView, QMenu, QHeaderView, QWidget, QAbstractItemView
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, Signal
from app.domain.models import ContactItem


class ContactsTableModel(QAbstractTableModel):
    COLUMNS = ["Imie", "Nazwisko", "Telefon", "E-mail", "Adres", "Notatki"]

    def __init__(self, contacts: list[ContactItem] | None = None) -> None:
        super().__init__()
        self._contacts: list[ContactItem] = contacts or []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._contacts)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.COLUMNS)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._contacts)):
            return None

        contact = self._contacts[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return contact.first_name
            elif col == 1:
                return contact.last_name
            elif col == 2:
                return contact.phone
            elif col == 3:
                return contact.email or ""
            elif col == 4:
                return contact.address or ""
            elif col == 5:
                return contact.notes or ""

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if 0 <= section < len(self.COLUMNS):
                return self.COLUMNS[section]
        return None

    def set_contacts(self, contacts: list[ContactItem]) -> None:
        self.beginResetModel()
        self._contacts = list(contacts)
        self.endResetModel()

    def get_contact_at(self, row: int) -> ContactItem | None:
        if 0 <= row < len(self._contacts):
            return self._contacts[row]
        return None


class ContactsTableView(QTableView):
    edit_requested = Signal(object)
    delete_requested = Signal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.model_data = ContactsTableModel()
        self.setModel(self.model_data)

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        self.doubleClicked.connect(self._on_double_click)

    def update_contacts(self, contacts: list[ContactItem]) -> None:
        self.model_data.set_contacts(contacts)

    def _get_selected_contact(self) -> ContactItem | None:
        indices = self.selectionModel().selectedRows()
        if indices:
            return self.model_data.get_contact_at(indices[0].row())
        return None

    def _on_double_click(self, index: QModelIndex) -> None:
        contact = self.model_data.get_contact_at(index.row())
        if contact:
            self.edit_requested.emit(contact)

    def _show_context_menu(self, pos) -> None:
        contact = self._get_selected_contact()
        if not contact:
            return

        menu = QMenu(self)
        edit_action = menu.addAction("Edytuj kontakt")
        delete_action = menu.addAction("Usun kontakt")

        action = menu.exec(self.viewport().mapToGlobal(pos))
        if action == edit_action:
            self.edit_requested.emit(contact)
        elif action == delete_action:
            self.delete_requested.emit(contact)
