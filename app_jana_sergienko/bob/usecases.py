from dataclasses import dataclass
from typing import Type
from typing import final

import attr as attr
import attrs
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.db.models import QuerySet

from app_jana_sergienko.bob.interfaces import Storage
from app_jana_sergienko.bob.interfaces import UseCase
from app_jana_sergienko.models import Contact
from app_jana_sergienko.models import Profile
from app_jana_sergienko.models.tag import Tag
from app_jana_sergienko.schemas import ContactSchema


@final
@dataclass(slots=True)
class AverageAppendNumberUseCase(UseCase):
    storage: Storage
    number: int

    def __call__(self) -> None:
        numbers = self.storage.load()
        numbers.append(self.number)
        self.storage.store(numbers)


@final
@dataclass(slots=True)
class AverageCalculateAverageUseCase(UseCase):
    storage: Storage

    def __call__(self) -> float:
        numbers: list[int] = self.storage.load()

        summa = sum(numbers)
        if not summa:
            return 0

        return summa / len(numbers)


@final
@dataclass(slots=True)
class GetAllContactsUseCase(UseCase):
    model: Type[models.Model] = Contact

    def __call__(self) -> list:
        return list(self.model.objects.all())


@final
@dataclass(slots=True)
class SaveContactUseCase(UseCase):
    contact: ContactSchema
    model: Type[models.Model] = Contact

    def __call__(self) -> None:
        db_obj = self.model(**self.contact.dict())
        db_obj.save()


User = get_user_model()


@final
@attrs.frozen(kw_only=True)
class GetProfileUseCase(UseCase):
    user: User  # type: ignore

    def __call__(self) -> Profile:
        profile, _ = Profile.objects.get_or_create(user=self.user)
        return profile


@final
@attr.frozen(kw_only=True)
class GetTagsAssignedUseCase(UseCase):
    contact: Contact

    def __call__(self) -> QuerySet:
        qs = Tag.objects.filter(contacts__pk=self.contact.pk)
        return qs


@final
@attr.frozen(kw_only=True)
class GetTagsUnassignedUseCase(UseCase):
    contact: Contact

    def __call__(self) -> QuerySet:
        cond = Q(contacts__pk=self.contact.pk)
        qs = Tag.objects.filter(~cond)
        return qs
