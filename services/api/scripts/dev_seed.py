"""Seed script for development and testing."""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import SessionLocal, Base, engine
from app.db.models import User, Contact, UserSettings
from app.core.security import get_password_hash

SAMPLE_CONTACTS = [
    {"first_name": "Jan", "last_name": "Kowalski", "phone": "+48 501 111 222", "email": "jan.kowalski@example.com", "address": "ul. Marszalkowska 10, Warszawa", "notes": "Kolega z zespolu IT"},
    {"first_name": "Anna", "last_name": "Nowak", "phone": "+48 502 222 333", "email": "anna.nowak@example.com", "address": "ul. Florianska 5, Krakow", "notes": "Project Manager"},
    {"first_name": "Piotr", "last_name": "Wisniewski", "phone": "+48 503 333 444", "email": "piotr.w@example.com", "address": "ul. Piotrkowska 120, Lodz", "notes": "Architekt systemow"},
    {"first_name": "Katarzyna", "last_name": "Wojcik", "phone": "+48 504 444 555", "email": "katarzyna.wojcik@example.com", "address": "ul. Swietojanska 15, Gdynia", "notes": "UI/UX Designer"},
    {"first_name": "Michal", "last_name": "Kowalczyk", "phone": "+48 505 555 666", "email": "m.kowalczyk@example.com", "address": "ul. Dluga 4, Gdansk", "notes": "DevOps Engineer"},
    {"first_name": "Magdalena", "last_name": "Kaminska", "phone": "+48 506 666 777", "email": "magda.k@example.com", "address": "ul. Lipowa 8, Bialystok", "notes": "QA Lead"},
    {"first_name": "Tomasz", "last_name": "Lewandowski", "phone": "+48 507 777 888", "email": "t.lewandowski@example.com", "address": "ul. Półwiejska 22, Poznan", "notes": "Senior Developer"},
    {"first_name": "Agnieszka", "last_name": "Zielinska", "phone": "+48 508 888 999", "email": "a.zielinska@example.com", "address": "ul. Swidnicka 30, Wroclaw", "notes": "Product Owner"},
    {"first_name": "Pawel", "last_name": "Szymanski", "phone": "+48 509 999 000", "email": "pawel.sz@example.com", "address": "ul. Krakowskie Przedmiescie 14, Lublin", "notes": "Security Specialist"},
    {"first_name": "Monika", "last_name": "Wozniak", "phone": "+48 510 123 456", "email": "m.wozniak@example.com", "address": "ul. Mariacka 3, Katowice", "notes": "Scrum Master"},
    {"first_name": "Jakub", "last_name": "Dabrowski", "phone": "+48 511 234 567", "email": "j.dabrowski@example.com", "address": "ul. Sienkiewicza 7, Kielce", "notes": "Fullstack Engineer"},
    {"first_name": "Zofia", "last_name": "Kozlowska", "phone": "+48 512 345 678", "email": "zofia.k@example.com", "address": "ul. Zeromskiego 18, Radom", "notes": "Database Administrator"},
    {"first_name": "Krzysztof", "last_name": "Jankowski", "phone": "+48 513 456 789", "email": "k.jankowski@example.com", "address": "ul. Kupiecka 9, Zielona Gora", "notes": "Backend Developer"},
    {"first_name": "Aleksandra", "last_name": "Mazur", "phone": "+48 514 567 890", "email": "ola.mazur@example.com", "address": "ul. Chrobrego 25, Szczecin", "notes": "Frontend Developer"},
    {"first_name": "Mateusz", "last_name": "Krawczyk", "phone": "+48 515 678 901", "email": "m.krawczyk@example.com", "address": "ul. Narutowicza 11, Torun", "notes": "Data Scientist"},
    {"first_name": "Karolina", "last_name": "Piotrowska", "phone": "+48 516 789 012", "email": "karolina.p@example.com", "address": "ul. Chopina 16, Opole", "notes": "Tech Recruiter"},
    {"first_name": "Marcin", "last_name": "Grabowski", "phone": "+48 517 890 123", "email": "m.grabowski@example.com", "address": "ul. Mickiewicza 40, Rzeszow", "notes": "Cloud Architect"},
    {"first_name": "Natalia", "last_name": "Pawlak", "phone": "+48 518 901 234", "email": "natalia.pawlak@example.com", "address": "ul. Kosciuszki 19, Olsztyn", "notes": "Customer Success"},
    {"first_name": "Lukasz", "last_name": "Michalski", "phone": "+48 519 012 345", "email": "l.michalski@example.com", "address": "ul. Gdanska 50, Bydgoszcz", "notes": "Mobile Developer"},
    {"first_name": "Dominika", "last_name": "Nowicka", "phone": "+48 520 123 987", "email": "d.nowicka@example.com", "address": "ul. Sikorskiego 8, Gorzow Wlkp.", "notes": "Technical Writer"},
]


def seed():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if test user exists
        test_email = "test@example.com"
        user = db.query(User).filter(User.email == test_email).first()

        if not user:
            print(f"Creating default user: {test_email}")
            user = User(
                email=test_email,
                hashed_password=get_password_hash("password123")
            )
            db.add(user)
            db.flush()

            settings = UserSettings(user_id=user.id, theme="dark", table_layout_json={})
            db.add(settings)
            db.commit()
            db.refresh(user)
            print(f"Created user with ID: {user.id}")
        else:
            print(f"User {test_email} already exists with ID: {user.id}")

        # Seed contacts
        existing_contacts = db.query(Contact).filter(Contact.user_id == user.id).count()
        if existing_contacts == 0:
            print(f"Seeding {len(SAMPLE_CONTACTS)} sample contacts...")
            for c_data in SAMPLE_CONTACTS:
                contact = Contact(
                    user_id=user.id,
                    first_name=c_data["first_name"],
                    last_name=c_data["last_name"],
                    phone=c_data["phone"],
                    email=c_data["email"],
                    address=c_data["address"],
                    notes=c_data["notes"],
                )
                db.add(contact)
            db.commit()
            print("Successfully seeded sample contacts!")
        else:
            print(f"User already has {existing_contacts} contacts in database.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
