from typing import cast

from django import forms
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView

from app_jana_sergienko.bob import usecases
from app_jana_sergienko.models import Contact
from app_jana_sergienko.models import Tag


class ContactMixin:
    def get_contact(self) -> Contact:
        assert hasattr(self, "kwargs")
        contact_pk = cast(int | str, self.kwargs.get("contact_pk") or 0)
        contact: Contact = get_object_or_404(Contact, pk=contact_pk)

        return contact


class TagMixin:
    def get_tag(self) -> Tag:
        assert hasattr(self, "kwargs")
        tag_pk = cast(int | str, self.kwargs.get("tag_pk") or 0)
        tag: Tag = get_object_or_404(Tag, pk=tag_pk)

        return tag


class TagContactView(ContactMixin, TagMixin, FormView):
    form_class = forms.Form
    http_method_names = ["post"]

    def get_success_url(self) -> str:
        contact = self.get_contact()
        return f"/~/jana_sergienko/contacts/{contact.pk}"


class TagContactAssignView(TagContactView):
    def form_valid(self, form: forms.Form) -> HttpResponse:
        contact = self.get_contact()
        tag = self.get_tag()

        contact.tags.add(tag)

        return super().form_valid(form)


class TagContactUnassignView(TagContactView):
    def form_valid(self, form: forms.Form) -> HttpResponse:
        contact = self.get_contact()
        tag = self.get_tag()

        contact.tags.remove(tag)

        return super().form_valid(form)


class TagCreateForm(forms.Form):
    tag_name = forms.CharField(required=True)


class TagCreateView(TagContactView):
    form_class = TagCreateForm

    def form_valid(self, form: TagCreateForm) -> HttpResponse:
        tag: Tag
        tag, _ = Tag.objects.get_or_create(name=form.cleaned_data["tag_name"])

        contact = self.get_contact()

        contact.tags.add(tag)

        return super().form_valid(form)


class TagSearchView(TagMixin, FormView):
    form_class = forms.Form
    http_method_names = ["post"]
    success_url = "/~/jana_sergienko/contacts/"


class TagSearchAssignView(TagSearchView):
    def form_valid(self, form: forms.Form) -> HttpResponse:
        tag = self.get_tag()

        profile = usecases.GetProfileUseCase(user=self.request.user)()
        profile.search_tags.add(tag)

        return super().form_valid(form)


class TagSearchUnassignView(TagSearchView):
    def form_valid(self, form: forms.Form) -> HttpResponse:
        tag = self.get_tag()

        profile = usecases.GetProfileUseCase(user=self.request.user)()
        profile.search_tags.remove(tag)

        return super().form_valid(form)
