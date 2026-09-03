"""Authentication endpoints."""

from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.api.deps import get_current_user
from app.schemas.auth import UserRegister, UserLogin, Token, UserOut
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Annotated[Session, Depends(get_db)]) -> UserOut:
    """Register a new user account."""
    service = AuthService(db)
    return service.register(payload)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Annotated[Session, Depends(get_db)]) -> Token:
    """Authenticate and obtain JWT access token."""
    service = AuthService(db)
    return service.login(payload)


@router.get("/me", response_model=UserOut)
def get_current_user_profile(current_user: Annotated[User, Depends(get_current_user)]) -> UserOut:
    """Get profile details of the authenticated user."""
    return UserOut.model_validate(current_user)
