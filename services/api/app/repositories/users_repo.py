"""Repository for user data access."""

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import User, UserSettings
from app.core.security import get_password_hash


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: str) -> User | None:
        return self.db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

    def get_by_email(self, email: str) -> User | None:
        return self.db.execute(select(User).where(User.email == email.strip().lower())).scalar_one_or_none()

    def create(self, email: str, plain_password: str) -> User:
        hashed_password = get_password_hash(plain_password)
        user = User(
            email=email.strip().lower(),
            hashed_password=hashed_password,
        )
        self.db.add(user)
        self.db.flush()

        # Create default user settings
        settings = UserSettings(user_id=user.id, theme="dark", table_layout_json={})
        self.db.add(settings)
        self.db.commit()
        self.db.refresh(user)
        return user
