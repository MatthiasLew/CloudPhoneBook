"""Login and Registration Window."""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QStackedWidget,
    QFormLayout,
)
from PySide6.QtCore import Qt, Signal
from app.state.session_store import SessionStore


class LoginWindow(QWidget):
    login_success = Signal()

    def __init__(self, session_store: SessionStore, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.session_store = session_store

        self.setWindowTitle("CloudPhoneBook — Logowanie")
        self.setFixedSize(380, 420)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        # Header Title
        title_label = QLabel("CloudPhoneBook", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 5px;")
        main_layout.addWidget(title_label)

        subtitle_label = QLabel("Nowoczesna ksiazka telefoniczna w chmurze", self)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #9ca3af; margin-bottom: 15px;")
        main_layout.addWidget(subtitle_label)

        # Stacked widget for Login / Register toggle
        self.stack = QStackedWidget(self)

        # Page 0: Login
        login_page = QWidget()
        login_layout = QFormLayout(login_page)
        login_layout.setSpacing(10)

        self.login_email = QLineEdit(self)
        self.login_email.setPlaceholderText("np. jan@example.com")
        self.login_password = QLineEdit(self)
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password.setPlaceholderText("Twoje haslo")

        login_layout.addRow(QLabel("Adres E-mail:"), self.login_email)
        login_layout.addRow(QLabel("Haslo:"), self.login_password)

        self.login_btn = QPushButton("Zaloguj sie", self)
        self.to_register_btn = QPushButton("Nie masz konta? Zarejestruj sie", self)
        self.to_register_btn.setObjectName("secondaryButton")

        login_layout.addRow(self.login_btn)
        login_layout.addRow(self.to_register_btn)
        self.stack.addWidget(login_page)

        # Page 1: Register
        register_page = QWidget()
        reg_layout = QFormLayout(register_page)
        reg_layout.setSpacing(10)

        self.reg_email = QLineEdit(self)
        self.reg_email.setPlaceholderText("np. jan@example.com")
        self.reg_password = QLineEdit(self)
        self.reg_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_password.setPlaceholderText("Haslo (min. 6 znakow)")

        reg_layout.addRow(QLabel("Adres E-mail:"), self.reg_email)
        reg_layout.addRow(QLabel("Haslo:"), self.reg_password)

        self.register_btn = QPushButton("Zaloz konto", self)
        self.to_login_btn = QPushButton("Masz juz konto? Zaloguj sie", self)
        self.to_login_btn.setObjectName("secondaryButton")

        reg_layout.addRow(self.register_btn)
        reg_layout.addRow(self.to_login_btn)
        self.stack.addWidget(register_page)

        main_layout.addWidget(self.stack)

        # Connect actions
        self.login_btn.clicked.connect(self._handle_login)
        self.register_btn.clicked.connect(self._handle_register)
        self.to_register_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.to_login_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.session_store.error_occurred.connect(self._show_error)

    def _handle_login(self) -> None:
        email = self.login_email.text().strip()
        password = self.login_password.text().strip()
        if not email or not password:
            QMessageBox.warning(self, "Uwaga", "Wprowadz email i haslo.")
            return

        if self.session_store.login(email=email, password=password):
            self.login_success.emit()
            self.close()

    def _handle_register(self) -> None:
        email = self.reg_email.text().strip()
        password = self.reg_password.text().strip()
        if not email or len(password) < 6:
            QMessageBox.warning(self, "Uwaga", "Podaj prawidlowy email i haslo (min. 6 znakow).")
            return

        if self.session_store.register(email=email, password=password):
            self.login_success.emit()
            self.close()

    def _show_error(self, message: str) -> None:
        QMessageBox.critical(self, "Blad", message)
