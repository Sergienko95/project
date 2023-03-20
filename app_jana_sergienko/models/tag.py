from typing import Any
from typing import cast

from django.db import models


class TagManager(models.Manager):
    def get_by_natural_key(self, name: str) -> "Tag":
        return cast(Tag, self.get(name=name))


class Tag(models.Model):
    objects = TagManager()

    name: Any = models.TextField(blank=True, null=True, unique=True)

    class Meta:
        ordering = ["name", "pk"]

    def natural_key(self) -> tuple[str]:
        return (self.name,)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"pk={self.pk}, "
            f"name={self.name!r}, "
            f")"
        )
