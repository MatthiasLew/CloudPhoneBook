"""Shared models, DTOs and errors for CloudPhoneBook."""

from shared.dtos import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    ContactCreate,
    ContactUpdate,
    ContactResponse,
    ContactListResponse,
    ContactFilterParams,
    UserSettingsDTO,
)
from shared.errors import (
    AppError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    ConflictError,
)

__all__ = [
    "UserRegisterRequest",
    "UserLoginRequest",
    "TokenResponse",
    "UserResponse",
    "ContactCreate",
    "ContactUpdate",
    "ContactResponse",
    "ContactListResponse",
    "ContactFilterParams",
    "UserSettingsDTO",
    "AppError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "ConflictError",
]
