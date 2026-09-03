"""Token storage for user authentication sessions."""

import os
import json
from pathlib import Path


class SecureTokenStorage:
    def __init__(self, app_name: str = "CloudPhoneBook") -> None:
        if os.name == "nt":
            base_dir = Path(os.environ.get("APPDATA", Path.home())) / app_name
        else:
            base_dir = Path.home() / ".config" / app_name

        base_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = base_dir / "auth_session.json"

    def save_session(self, token: str, email: str, user_id: str) -> None:
        data = {
            "token": token,
            "email": email,
            "user_id": user_id,
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_session(self) -> dict[str, str] | None:
        if not self.file_path.exists():
            return None
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def clear_session(self) -> None:
        if self.file_path.exists():
            try:
                self.file_path.unlink()
            except Exception:
                pass
