"""Service for authentication and user management."""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.users_repo import UserRepository
from app.schemas.auth import UserRegister, UserLogin, Token, UserOut
from app.core.security import verify_password, create_access_token


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repo = UserRepository(db)

    def register(self, payload: UserRegister) -> UserOut:
        existing = self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        user = self.repo.create(payload.email, payload.password)
        return UserOut.model_validate(user)

    def login(self, payload: UserLogin) -> Token:
        user = self.repo.get_by_email(payload.email)
        if not user or not verify_password(payload.password, str(user.hashed_password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = create_access_token(subject=str(user.id))
        return Token(access_token=token)
