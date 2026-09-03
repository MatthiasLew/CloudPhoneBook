"""User settings API endpoints."""

from typing import Any
from app.api.client import ApiClient


class SettingsApi:
    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def get_settings(self) -> dict[str, Any]:
        return self.client.get("/me/settings")

    def update_settings(self, theme: str, table_layout: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = {
            "theme": theme,
            "table_layout_json": table_layout or {}
        }
        return self.client.put("/me/settings", payload)
