"""State store for user and application settings."""

from PySide6.QtCore import QObject, Signal
from app.api.settings_api import SettingsApi
from app.domain.models import AppSettings


class SettingsStore(QObject):
    theme_changed = Signal(str)
    settings_loaded = Signal(object)
    error_occurred = Signal(str)

    def __init__(self, settings_api: SettingsApi) -> None:
        super().__init__()
        self.api = settings_api
        self.settings = AppSettings()

    def fetch_settings(self) -> None:
        try:
            res = self.api.get_settings()
            self.settings.theme = res.get("theme", "dark")
            self.settings.table_layout = res.get("table_layout_json", {})
            self.theme_changed.emit(self.settings.theme)
            self.settings_loaded.emit(self.settings)
        except Exception as e:
            self.error_occurred.emit(f"Nie udalo sie pobrac ustawien: {e}")

    def update_theme(self, theme: str) -> None:
        self.settings.theme = theme
        self.theme_changed.emit(theme)
        try:
            self.api.update_settings(theme=theme, table_layout=self.settings.table_layout)
        except Exception:
            pass

    def update_table_layout(self, table_layout: dict) -> None:
        self.settings.table_layout = table_layout
        try:
            self.api.update_settings(theme=self.settings.theme, table_layout=table_layout)
        except Exception:
            pass
