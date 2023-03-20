from typing import Any
from typing import cast

from django.contrib.auth import get_user_model
from django.db import models

from .tag import Tag

User = get_user_model()


class ContactManager(models.Manager):
    def get_by_natural_key(self, name: str) -> "Contact":
        return cast(Contact, self.get(name=name))


class Contact(models.Model):
    objects = ContactManager()

    name: Any = models.TextField(blank=True, null=True, unique=True)
    age: Any = models.DateField(blank=True, null=True)
    phone: Any = models.TextField(blank=True, null=True)
    indexed: Any = models.DateTimeField(blank=True, null=True, db_index=True)
    owner: Any = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="+",
    )
    tags: Any = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="contacts",
    )

    class Meta:
        ordering = ["name", "age", "pk"]

    def natural_key(self) -> tuple[str]:
        return (self.name,)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"pk={self.pk}, "
            f"name={self.name!r}, "
            f"owner={self.owner}, "
            f")"
        )
