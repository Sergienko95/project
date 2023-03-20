from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from app_jana_sergienko.models import Contact
from app_jana_sergienko.models import Profile
from app_jana_sergienko.models import Tag


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    actions = ["assign_to_current_user"]

    @admin.action(description="Assign contacts to current user")
    def assign_to_current_user(
        self,
        request: HttpRequest,
        queryset: QuerySet,
    ) -> None:
        queryset.update(owner=request.user)
