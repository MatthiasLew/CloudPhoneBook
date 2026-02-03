from fastapi import APIRouter, status, HTTPException
from app.schemas.contact import ContactOut
from uuid import uuid4

router = APIRouter(prefix="/contacts", tags=["contacts"])

MOCK_CONTACTS: list[ContactOut] = [
    ContactOut(id="1", first_name="Jan", last_name="Kowalski", phone="123456789", email="jan@example.com"),
    ContactOut(id="2", first_name="Ala", last_name="Nowak", phone="987654321", email=None),
]


@router.get("", response_model=list[ContactOut])
def list_contacts():
    return MOCK_CONTACTS


@router.post("", response_model=ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(payload: ContactOut):
    new_contact = ContactOut(
        id=str(uuid4()),
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone=payload.phone,
        email=str(payload.email) if payload.email is not None else None,
    )
    MOCK_CONTACTS.append(new_contact)
    return new_contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: str):
    for i, c in enumerate(MOCK_CONTACTS):
        if c.id == contact_id:
            del MOCK_CONTACTS[i]
            return

    raise HTTPException(status_code=404, detail="Contact not found")
