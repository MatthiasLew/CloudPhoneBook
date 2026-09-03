"""Desktop application domain models."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ContactItem:
    id: str
    user_id: str
    first_name: str
    last_name: str
    phone: str
    email: str | None
    address: str | None
    notes: str | None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name


@dataclass
class UserSession:
    user_id: str
    email: str
    token: str
    is_authenticated: bool = True


@dataclass
class AppSettings:
    theme: str = "dark"
    table_layout: dict[str, Any] | None = None
