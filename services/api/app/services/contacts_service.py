"""Service for contacts business logic."""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.contacts_repo import ContactsRepository
from app.schemas.contact import ContactCreate, ContactUpdate, ContactOut, ContactListResponse


class ContactsService:
    def __init__(self, db: Session) -> None:
        self.repo = ContactsRepository(db)

    def list_contacts(
        self,
        user_id: str,
        query: str | None = None,
        limit: int = 50,
        offset: int = 0
    ) -> ContactListResponse:
        items, total = self.repo.list(user_id=user_id, query=query, limit=limit, offset=offset)
        return ContactListResponse(
            items=[ContactOut.model_validate(c) for c in items],
            total=total,
            limit=limit,
            offset=offset,
        )

    def get_contact(self, user_id: str, contact_id: str) -> ContactOut:
        contact = self.repo.get_by_id(user_id=user_id, contact_id=contact_id)
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found"
            )
        return ContactOut.model_validate(contact)

    def create_contact(self, user_id: str, payload: ContactCreate) -> ContactOut:
        contact = self.repo.create(user_id=user_id, payload=payload)
        return ContactOut.model_validate(contact)

    def update_contact(self, user_id: str, contact_id: str, payload: ContactUpdate) -> ContactOut:
        contact = self.repo.get_by_id(user_id=user_id, contact_id=contact_id)
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found"
            )
        updated = self.repo.update(contact=contact, payload=payload)
        return ContactOut.model_validate(updated)

    def delete_contact(self, user_id: str, contact_id: str) -> None:
        contact = self.repo.get_by_id(user_id=user_id, contact_id=contact_id)
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found"
            )
        self.repo.delete(contact)
