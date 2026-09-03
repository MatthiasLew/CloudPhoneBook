"""Repository for user settings data access."""

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import UserSettings
from app.schemas.settings import SettingsUpdate


class SettingsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_user_id(self, user_id: str) -> UserSettings:
        settings = self.db.execute(
            select(UserSettings).where(UserSettings.user_id == user_id)
        ).scalar_one_or_none()

        if not settings:
            settings = UserSettings(user_id=user_id, theme="dark", table_layout_json={})
            self.db.add(settings)
            self.db.commit()
            self.db.refresh(settings)

        return settings

    def update_for_user_id(self, user_id: str, payload: SettingsUpdate) -> UserSettings:
        settings = self.get_by_user_id(user_id)
        settings.theme = payload.theme
        settings.table_layout_json = payload.table_layout_json
        self.db.commit()
        self.db.refresh(settings)
        return settings
