"""Service for user settings."""

from sqlalchemy.orm import Session
from app.repositories.settings_repo import SettingsRepository
from app.schemas.settings import SettingsUpdate, SettingsOut


class SettingsService:
    def __init__(self, db: Session) -> None:
        self.repo = SettingsRepository(db)

    def get_settings(self, user_id: str) -> SettingsOut:
        settings = self.repo.get_by_user_id(user_id=user_id)
        return SettingsOut.model_validate(settings)

    def update_settings(self, user_id: str, payload: SettingsUpdate) -> SettingsOut:
        updated = self.repo.update_for_user_id(user_id=user_id, payload=payload)
        return SettingsOut.model_validate(updated)
