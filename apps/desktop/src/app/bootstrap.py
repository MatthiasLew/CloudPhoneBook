"""Application bootstrap and lifecycle orchestrator."""

import os
from PySide6.QtWidgets import QApplication
from app.api.client import ApiClient
from app.api.contacts_api import ContactsApi
from app.api.settings_api import SettingsApi
from app.storage.secure_token import SecureTokenStorage
from app.storage.local_cache import LocalCache
from app.state.session_store import SessionStore
from app.state.contacts_store import ContactsStore
from app.state.settings_store import SettingsStore
from app.ui.themes.theme_manager import ThemeManager
from app.ui.windows.login_window import LoginWindow
from app.ui.windows.main_window import MainWindow


class AppBootstrap:
    def __init__(self, qapp: QApplication) -> None:
        self.qapp = qapp
        api_base_url = os.environ.get("API_BASE_URL", "http://localhost:8000/api/v1")

        # Infrastructure
        self.api_client = ApiClient(base_url=api_base_url)
        self.token_storage = SecureTokenStorage()
        self.local_cache = LocalCache()
        self.theme_manager = ThemeManager()

        # State Stores
        self.session_store = SessionStore(self.api_client, self.token_storage)
        self.contacts_api = ContactsApi(self.api_client)
        self.settings_api = SettingsApi(self.api_client)
        self.contacts_store = ContactsStore(self.contacts_api, self.local_cache)
        self.settings_store = SettingsStore(self.settings_api)

        # Windows
        self.login_window: LoginWindow | None = None
        self.main_window: MainWindow | None = None

        # Apply initial theme
        self.settings_store.theme_changed.connect(
            lambda theme: self.theme_manager.apply_theme(self.qapp, theme)
        )
        self.theme_manager.apply_theme(self.qapp, "dark")

        # Hook session state changes
        self.session_store.unauthenticated.connect(self._show_login)

    def run(self) -> None:
        if self.session_store.restore_session():
            self._show_main()
        else:
            self._show_login()

    def _show_login(self) -> None:
        if self.main_window:
            self.main_window.close()
            self.main_window = None

        self.login_window = LoginWindow(session_store=self.session_store)
        self.login_window.login_success.connect(self._show_main)
        self.login_window.show()

    def _show_main(self) -> None:
        if self.login_window:
            self.login_window.close()
            self.login_window = None

        self.main_window = MainWindow(
            session_store=self.session_store,
            contacts_store=self.contacts_store,
            settings_store=self.settings_store,
        )
        self.main_window.show()
        self.main_window.load_initial_data()
