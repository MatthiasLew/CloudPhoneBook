"""Contacts API endpoints."""

from typing import Any
from app.api.client import ApiClient


class ContactsApi:
    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def list_contacts(self, query: str | None = None, limit: int = 200, offset: int = 0) -> dict[str, Any]:
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if query and query.strip():
            params["query"] = query.strip()
        return self.client.get("/contacts", params=params)

    def create_contact(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.client.post("/contacts", payload)

    def update_contact(self, contact_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.client.put(f"/contacts/{contact_id}", payload)

    def delete_contact(self, contact_id: str) -> None:
        self.client.delete(f"/contacts/{contact_id}")
