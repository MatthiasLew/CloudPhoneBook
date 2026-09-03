"""User settings endpoints."""

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.api.deps import get_current_user
from app.schemas.settings import SettingsUpdate, SettingsOut
from app.services.settings_service import SettingsService

router = APIRouter(prefix="/me/settings", tags=["settings"])


@router.get("", response_model=SettingsOut)
def get_user_settings(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> SettingsOut:
    """Retrieve UI preferences and settings for the authenticated user."""
    service = SettingsService(db)
    return service.get_settings(user_id=str(current_user.id))


@router.put("", response_model=SettingsOut)
def update_user_settings(
    payload: SettingsUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> SettingsOut:
    """Update UI preferences and settings for the authenticated user."""
    service = SettingsService(db)
    return service.update_settings(user_id=str(current_user.id), payload=payload)
