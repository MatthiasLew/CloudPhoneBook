"""Unit and GUI tests for Desktop application."""

import pytest
from app.domain.validators import validate_email, validate_phone, validate_contact_form
from app.domain.models import ContactItem
from app.storage.secure_token import SecureTokenStorage
from app.storage.local_cache import LocalCache
from app.ui.widgets.contacts_table import ContactsTableModel
from app.ui.themes.theme_manager import ThemeManager
from PySide6.QtCore import Qt


def test_validators():
    # Email
    assert validate_email("jan@example.com")[0] is True
    assert validate_email("invalid-email")[0] is False
    assert validate_email("")[0] is True  # optional

    # Phone
    assert validate_phone("+48 123 456 789")[0] is True
    assert validate_phone("12345")[0] is True
    assert validate_phone("")[0] is False
    assert validate_phone("ab")[0] is False

    # Contact Form
    assert validate_contact_form("Jan", "+48123456789", "jan@example.com")[0] is True
    assert validate_contact_form("", "+48123456789", None)[0] is False
    assert validate_contact_form("Jan", "abc", None)[0] is False


def test_storage_token(tmp_path):
    storage = SecureTokenStorage(app_name="TestPhoneBook")
    storage.file_path = tmp_path / "test_session.json"

    storage.save_session(token="jwt-token-123", email="user@test.com", user_id="u-1")
    loaded = storage.load_session()
    assert loaded is not None
    assert loaded["token"] == "jwt-token-123"
    assert loaded["email"] == "user@test.com"

    storage.clear_session()
    assert storage.load_session() is None


def test_local_cache(tmp_path):
    cache = LocalCache(app_name="TestPhoneBook")
    cache.cache_file = tmp_path / "test_contacts.json"

    sample = [{"id": "1", "first_name": "Jan", "phone": "123"}]
    cache.save_contacts(sample)
    loaded = cache.load_contacts()
    assert len(loaded) == 1
    assert loaded[0]["first_name"] == "Jan"

    cache.clear()
    assert cache.load_contacts() == []


def test_contacts_table_model(qapp):
    contacts = [
        ContactItem(
            id="1",
            user_id="u1",
            first_name="Jan",
            last_name="Kowalski",
            phone="123456789",
            email="jan@example.com",
            address="Warszawa",
            notes="Test",
        ),
        ContactItem(
            id="2",
            user_id="u1",
            first_name="Anna",
            last_name="Nowak",
            phone="987654321",
            email=None,
            address=None,
            notes=None,
        )
    ]
    model = ContactsTableModel(contacts)
    assert model.rowCount() == 2
    assert model.columnCount() == 6

    # Test display data
    idx_first_name = model.index(0, 0)
    assert model.data(idx_first_name, Qt.ItemDataRole.DisplayRole) == "Jan"

    idx_phone = model.index(0, 2)
    assert model.data(idx_phone, Qt.ItemDataRole.DisplayRole) == "123456789"

    # Test header data
    assert model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) == "Imie"
    assert model.headerData(1, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) == "Nazwisko"


def test_theme_manager(qapp):
    manager = ThemeManager()
    manager.apply_theme(qapp, "light")
    manager.apply_theme(qapp, "dark")
