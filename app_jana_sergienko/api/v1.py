from random import randint  # noqa: DUO102

from faker import Faker
from faker.providers import address
from faker.providers import phone_number
from fastapi import FastAPI
from fastapi import Query
from pydantic import BaseModel
from pydantic import Field

app = FastAPI()

fake = Faker("ru_RU")
fake.add_provider(phone_number)
fake.add_provider(address)


class Contact(BaseModel):
    pk: int
    name: str
    age: int = Field(ge=18, le=81)
    address: str
    phone: str


@app.get("/v1/contacts")
def list_contacts() -> list[Contact]:
    return []


@app.get("/v2/contacts")
def list_contacts_v2(
    n: int = Query(1, ge=0),  # noqa: VNE001,B008
) -> list[Contact]:
    contacts = [
        Contact(
            pk=pk,
            name=fake.name(),
            age=randint(18, 81),  # noqa: S311
            phone=fake.phone_number(),
            address=fake.address(),
        )
        for pk in range(0, n)
    ]
    return contacts
