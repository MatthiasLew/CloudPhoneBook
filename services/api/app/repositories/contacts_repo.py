"""Repository for contacts data access."""

from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_
from app.db.models import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


class ContactsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: str, contact_id: str) -> Contact | None:
        return self.db.execute(
            select(Contact).where(Contact.id == contact_id, Contact.user_id == user_id)
        ).scalar_one_or_none()

    def list(
        self,
        user_id: str,
        query: str | None = None,
        limit: int = 50,
        offset: int = 0
    ) -> tuple[list[Contact], int]:
        base_stmt = select(Contact).where(Contact.user_id == user_id)

        if query and query.strip():
            q_like = f"%{query.strip()}%"
            filter_condition = or_(
                Contact.first_name.ilike(q_like),
                Contact.last_name.ilike(q_like),
                Contact.phone.ilike(q_like),
                Contact.email.ilike(q_like),
                Contact.address.ilike(q_like),
            )
            base_stmt = base_stmt.where(filter_condition)

        # Count total
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = self.db.scalar(count_stmt) or 0

        # Fetch page ordered by first_name, last_name
        stmt = base_stmt.order_by(Contact.first_name.asc(), Contact.last_name.asc()).offset(offset).limit(limit)
        items = list(self.db.execute(stmt).scalars().all())

        return items, total

    def create(self, user_id: str, payload: ContactCreate) -> Contact:
        contact = Contact(
            user_id=user_id,
            first_name=payload.first_name.strip(),
            last_name=payload.last_name.strip(),
            phone=payload.phone.strip(),
            email=str(payload.email) if payload.email else None,
            address=payload.address.strip() if payload.address else None,
            notes=payload.notes.strip() if payload.notes else None,
        )
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact

    def update(self, contact: Contact, payload: ContactUpdate) -> Contact:
        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            if value is not None and isinstance(value, str):
                setattr(contact, key, value.strip())
            else:
                setattr(contact, key, value)

        self.db.commit()
        self.db.refresh(contact)
        return contact

    def delete(self, contact: Contact) -> None:
        self.db.delete(contact)
        self.db.commit()
