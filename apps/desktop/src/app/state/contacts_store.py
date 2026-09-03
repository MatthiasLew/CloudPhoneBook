"""State store for contacts management."""

from PySide6.QtCore import QObject, Signal
from app.api.contacts_api import ContactsApi
from app.storage.local_cache import LocalCache
from app.domain.models import ContactItem


class ContactsStore(QObject):
    contacts_loaded = Signal(list)
    contact_added = Signal(object)
    contact_updated = Signal(object)
    contact_deleted = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, contacts_api: ContactsApi, cache: LocalCache) -> None:
        super().__init__()
        self.api = contacts_api
        self.cache = cache
        self.contacts: list[ContactItem] = []
        self.current_query: str = ""

    def load_cached(self) -> None:
        cached_data = self.cache.load_contacts()
        if cached_data:
            self.contacts = [
                ContactItem(
                    id=c["id"],
                    user_id=c.get("user_id", ""),
                    first_name=c["first_name"],
                    last_name=c.get("last_name", ""),
                    phone=c["phone"],
                    email=c.get("email"),
                    address=c.get("address"),
                    notes=c.get("notes"),
                )
                for c in cached_data
            ]
            self.contacts_loaded.emit(self.contacts)

    def fetch_contacts(self, query: str | None = None) -> None:
        self.current_query = query or ""
        try:
            res = self.api.list_contacts(query=query)
            items = res.get("items", [])
            self.contacts = [
                ContactItem(
                    id=c["id"],
                    user_id=c.get("user_id", ""),
                    first_name=c["first_name"],
                    last_name=c.get("last_name", ""),
                    phone=c["phone"],
                    email=c.get("email"),
                    address=c.get("address"),
                    notes=c.get("notes"),
                )
                for c in items
            ]
            if not query:
                # Save full list in cache
                self.cache.save_contacts(items)
            self.contacts_loaded.emit(self.contacts)
        except Exception as e:
            self.error_occurred.emit(f"Nie udalo sie pobrac kontaktow: {e}")

    def add_contact(self, payload: dict) -> bool:
        try:
            res = self.api.create_contact(payload)
            item = ContactItem(
                id=res["id"],
                user_id=res.get("user_id", ""),
                first_name=res["first_name"],
                last_name=res.get("last_name", ""),
                phone=res["phone"],
                email=res.get("email"),
                address=res.get("address"),
                notes=res.get("notes"),
            )
            self.contacts.append(item)
            self.contact_added.emit(item)
            self.fetch_contacts(self.current_query)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Blad dodawania kontaktu: {e}")
            return False

    def update_contact(self, contact_id: str, payload: dict) -> bool:
        try:
            res = self.api.update_contact(contact_id, payload)
            item = ContactItem(
                id=res["id"],
                user_id=res.get("user_id", ""),
                first_name=res["first_name"],
                last_name=res.get("last_name", ""),
                phone=res["phone"],
                email=res.get("email"),
                address=res.get("address"),
                notes=res.get("notes"),
            )
            self.contact_updated.emit(item)
            self.fetch_contacts(self.current_query)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Blad aktualizacji kontaktu: {e}")
            return False

    def delete_contact(self, contact_id: str) -> bool:
        try:
            self.api.delete_contact(contact_id)
            self.contacts = [c for c in self.contacts if c.id != contact_id]
            self.contact_deleted.emit(contact_id)
            self.fetch_contacts(self.current_query)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Blad usuwania kontaktu: {e}")
            return False
