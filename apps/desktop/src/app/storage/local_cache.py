"""Local cache for contacts and offline resilience."""

import os
import json
from pathlib import Path
from typing import Any


class LocalCache:
    def __init__(self, app_name: str = "CloudPhoneBook") -> None:
        if os.name == "nt":
            base_dir = Path(os.environ.get("APPDATA", Path.home())) / app_name
        else:
            base_dir = Path.home() / ".config" / app_name

        base_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = base_dir / "contacts_cache.json"

    def save_contacts(self, contacts: list[dict[str, Any]]) -> None:
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(contacts, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def load_contacts(self) -> list[dict[str, Any]]:
        if not self.cache_file.exists():
            return []
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def clear(self) -> None:
        if self.cache_file.exists():
            try:
                self.cache_file.unlink()
            except Exception:
                pass
