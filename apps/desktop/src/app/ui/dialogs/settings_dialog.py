"""Settings dialog for theme and sync preferences."""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QLabel,
    QWidget,
)
from app.state.settings_store import SettingsStore


class SettingsDialog(QDialog):
    def __init__(self, settings_store: SettingsStore, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.settings_store = settings_store
        self.setWindowTitle("Ustawienia aplikacji")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.theme_combo = QComboBox(self)
        self.theme_combo.addItem("Ciemny (Dark)", "dark")
        self.theme_combo.addItem("Jasny (Light)", "light")

        current_theme = self.settings_store.settings.theme
        idx = self.theme_combo.findData(current_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)

        form_layout.addRow(QLabel("Motyw graficzny:"), self.theme_combo)
        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.close_btn = QPushButton("Zamknij", self)
        self.close_btn.setObjectName("secondaryButton")
        self.save_btn = QPushButton("Zapisz", self)

        btn_layout.addStretch()
        btn_layout.addWidget(self.close_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)

        self.close_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self._on_save)

    def _on_save(self) -> None:
        selected_theme = self.theme_combo.currentData()
        self.settings_store.update_theme(selected_theme)
        self.accept()
