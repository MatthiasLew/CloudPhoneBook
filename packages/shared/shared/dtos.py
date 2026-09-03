"""Shared Data Transfer Objects (DTOs) for CloudPhoneBook."""

from datetime import datetime
from typing import Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """Payload for user registration."""
    email: EmailStr
    password: str = Field(min_length=6, max_length=128, description="User password (min 6 characters)")


class UserLoginRequest(BaseModel):
    """Payload for user login."""
    email: EmailStr
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    """JWT Token response after successful authentication."""
    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int = 86400


class UserResponse(BaseModel):
    """Safe user profile response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    created_at: datetime


class ContactBase(BaseModel):
    """Base contact fields."""
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(default="", max_length=100)
    phone: str = Field(min_length=1, max_length=50)
    email: EmailStr | None = None
    address: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=1000)


class ContactCreate(ContactBase):
    """Payload for creating a new contact."""
    pass


class ContactUpdate(BaseModel):
    """Payload for updating an existing contact."""
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = None
    address: str | None = None
    notes: str | None = None


class ContactResponse(ContactBase):
    """Contact representation returned to clients."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class ContactListResponse(BaseModel):
    """Paginated or listed contacts with total count."""
    items: list[ContactResponse]
    total: int
    limit: int
    offset: int


class ContactFilterParams(BaseModel):
    """Query parameters for searching and paginating contacts."""
    query: str | None = None
    limit: int = Field(default=50, ge=1, le=500)
    offset: int = Field(default=0, ge=0)


class UserSettingsDTO(BaseModel):
    """User UI and application preferences."""
    model_config = ConfigDict(from_attributes=True)

    theme: str = Field(default="dark", pattern="^(dark|light|system)$")
    table_layout_json: dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime | None = None
