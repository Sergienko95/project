from typing import Any

from django.contrib.auth import get_user_model
from django.db import models

from .tag import Tag

User = get_user_model()


class ProfileManager(models.Manager):
    pass


class Profile(models.Model):
    objects = ProfileManager()

    user: Any = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="+",
    )
    preferences: Any = models.TextField(blank=True, null=True)
    search_text: Any = models.TextField(blank=True, null=True)
    search_tags: Any = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="+",
    )

    class Meta:
        ordering = ["pk"]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(" f"pk={self.pk}" f")"
