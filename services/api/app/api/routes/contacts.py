"""Contacts REST endpoints."""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.api.deps import get_current_user
from app.schemas.contact import ContactCreate, ContactUpdate, ContactOut, ContactListResponse
from app.services.contacts_service import ContactsService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("", response_model=ContactListResponse)
def list_contacts(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    query: str | None = Query(None, description="Search term for names, phone, email, or address"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> ContactListResponse:
    """List contacts belonging to the authenticated user with optional search filter."""
    service = ContactsService(db)
    return service.list_contacts(
        user_id=str(current_user.id),
        query=query,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(
    payload: ContactCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ContactOut:
    """Create a new contact in the authenticated user's phonebook."""
    service = ContactsService(db)
    return service.create_contact(user_id=str(current_user.id), payload=payload)


@router.get("/{contact_id}", response_model=ContactOut)
def get_contact(
    contact_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ContactOut:
    """Get single contact details."""
    service = ContactsService(db)
    return service.get_contact(user_id=str(current_user.id), contact_id=contact_id)


@router.put("/{contact_id}", response_model=ContactOut)
def update_contact(
    contact_id: str,
    payload: ContactUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ContactOut:
    """Update contact details."""
    service = ContactsService(db)
    return service.update_contact(user_id=str(current_user.id), contact_id=contact_id, payload=payload)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    """Delete a contact."""
    service = ContactsService(db)
    service.delete_contact(user_id=str(current_user.id), contact_id=contact_id)
