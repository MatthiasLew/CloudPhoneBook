"""State store for user authentication session."""

from PySide6.QtCore import QObject, Signal
from app.api.auth_api import AuthApi
from app.api.client import ApiClient
from app.storage.secure_token import SecureTokenStorage
from app.domain.models import UserSession


class SessionStore(QObject):
    authenticated = Signal(UserSession)
    unauthenticated = Signal()
    error_occurred = Signal(str)

    def __init__(self, api_client: ApiClient, storage: SecureTokenStorage) -> None:
        super().__init__()
        self.api_client = api_client
        self.storage = storage
        self.auth_api = AuthApi(api_client)
        self.current_session: UserSession | None = None

    def restore_session(self) -> bool:
        saved = self.storage.load_session()
        if saved and "token" in saved:
            self.api_client.set_token(saved["token"])
            try:
                profile = self.auth_api.get_me()
                self.current_session = UserSession(
                    user_id=profile["id"],
                    email=profile["email"],
                    token=saved["token"],
                )
                self.authenticated.emit(self.current_session)
                return True
            except Exception:
                self.logout()
        return False

    def login(self, email: str, password: str) -> bool:
        try:
            res = self.auth_api.login(email=email, password=password)
            token = res["access_token"]
            self.api_client.set_token(token)

            profile = self.auth_api.get_me()
            session = UserSession(
                user_id=profile["id"],
                email=profile["email"],
                token=token,
            )
            self.current_session = session
            self.storage.save_session(token=token, email=profile["email"], user_id=profile["id"])
            self.authenticated.emit(session)
            return True
        except Exception as e:
            msg = "Blad logowania: Niepoprawny email lub haslo."
            self.error_occurred.emit(msg)
            return False

    def register(self, email: str, password: str) -> bool:
        try:
            self.auth_api.register(email=email, password=password)
            return self.login(email=email, password=password)
        except Exception as e:
            self.error_occurred.emit(f"Blad rejestracji: {e}")
            return False

    def logout(self) -> None:
        self.current_session = None
        self.api_client.set_token(None)
        self.storage.clear_session()
        self.unauthenticated.emit()
