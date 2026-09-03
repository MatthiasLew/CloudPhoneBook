"""Dialog for adding or editing contacts."""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QLabel,
    QMessageBox,
    QWidget,
)
from app.domain.models import ContactItem
from app.domain.validators import validate_contact_form


class ContactEditDialog(QDialog):
    def __init__(self, contact: ContactItem | None = None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.contact = contact
        is_edit = contact is not None

        self.setWindowTitle("Edytuj kontakt" if is_edit else "Dodaj nowy kontakt")
        self.setMinimumWidth(400)

        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.first_name_input = QLineEdit(self)
        self.last_name_input = QLineEdit(self)
        self.phone_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.address_input = QLineEdit(self)
        self.notes_input = QTextEdit(self)
        self.notes_input.setMaximumHeight(80)

        form_layout.addRow(QLabel("Imie *:"), self.first_name_input)
        form_layout.addRow(QLabel("Nazwisko:"), self.last_name_input)
        form_layout.addRow(QLabel("Telefon *:"), self.phone_input)
        form_layout.addRow(QLabel("E-mail:"), self.email_input)
        form_layout.addRow(QLabel("Adres:"), self.address_input)
        form_layout.addRow(QLabel("Notatki:"), self.notes_input)

        main_layout.addLayout(form_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Anuluj", self)
        self.cancel_btn.setObjectName("secondaryButton")
        self.save_btn = QPushButton("Zapisz", self)

        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        main_layout.addLayout(btn_layout)

        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self._on_save)

        if is_edit and contact:
            self.first_name_input.setText(contact.first_name)
            self.last_name_input.setText(contact.last_name)
            self.phone_input.setText(contact.phone)
            self.email_input.setText(contact.email or "")
            self.address_input.setText(contact.address or "")
            self.notes_input.setPlainText(contact.notes or "")

    def _on_save(self) -> None:
        first_name = self.first_name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip() or None

        valid, error = validate_contact_form(first_name=first_name, phone=phone, email=email)
        if not valid:
            QMessageBox.warning(self, "Blad walidacji", error)
            return

        self.accept()

    def get_data(self) -> dict:
        return {
            "first_name": self.first_name_input.text().strip(),
            "last_name": self.last_name_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "email": self.email_input.text().strip() or None,
            "address": self.address_input.text().strip() or None,
            "notes": self.notes_input.toPlainText().strip() or None,
        }
