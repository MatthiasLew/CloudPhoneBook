from pydantic import BaseModel, EmailStr, Field


class ContactOut(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone: str = Field(min_length=1, max_length=50)
    email: EmailStr | None = None
