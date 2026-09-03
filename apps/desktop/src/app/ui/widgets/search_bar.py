"""Search bar with live debounced search."""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PySide6.QtCore import Signal, QTimer


class SearchBar(QWidget):
    search_triggered = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Szukaj kontaktow (imie, nazwisko, telefon, email)...")
        self.input_field.setClearButtonEnabled(True)

        self.clear_btn = QPushButton("Wyczysc", self)
        self.clear_btn.setObjectName("secondaryButton")

        layout.addWidget(self.input_field)
        layout.addWidget(self.clear_btn)

        # Debounce timer (300ms)
        self.debounce_timer = QTimer(self)
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.setInterval(300)

        self.input_field.textChanged.connect(self._on_text_changed)
        self.debounce_timer.timeout.connect(self._emit_search)
        self.clear_btn.clicked.connect(self.clear)

    def _on_text_changed(self, text: str) -> None:
        self.debounce_timer.start()

    def _emit_search(self) -> None:
        self.search_triggered.emit(self.input_field.text().strip())

    def clear(self) -> None:
        self.input_field.clear()
        self.search_triggered.emit("")
