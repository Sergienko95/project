from pydantic import BaseModel


class ContactSchema(BaseModel):
    name: str
    age: int | None = None
    phone: str | None = None
