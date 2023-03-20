from typing import Any
from typing import cast

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models import QuerySet
from django.http import HttpResponse
from django.views import generic

from app_jana_sergienko.bob import usecases
from app_jana_sergienko.models import Contact
from app_jana_sergienko.models import Tag
from app_jana_sergienko.schemas import ContactSchema


class ContactForm(forms.Form):
    name = forms.CharField(label="Name:")
    age = forms.IntegerField(label="Age:")
    phone = forms.CharField(label="Phone:")


class SearchResultsView(LoginRequiredMixin, generic.ListView):
    model = Contact
    success_url = "/~/jana_sergienko/contacts/"
    extra_context = {
        "form": ContactForm(),
    }

    def get_queryset(self) -> Any:
        query = self.request.GET.get("search")
        object_list = Contact.objects.filter(
            Q(name__icontains=query)
            | Q(age__icontains=query)
            | Q(phone__icontains=query)
        )

        return object_list


class ContactListView(LoginRequiredMixin, generic.ListView):
    model = Contact

    def get_queryset(self) -> QuerySet:
        qs = cast(QuerySet, super().get_queryset())

        qs = self._apply_user_filter(qs)
        qs = self._apply_tags_filter(qs)

        return qs

    def get_context_data(self, **kwargs: dict) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

        profile = usecases.GetProfileUseCase(user=self.request.user)()
        search_text = cast(str, profile.search_text)
        ctx["search_text"] = search_text

        tags_assigned = profile.search_tags.all()
        ctx["tags_assigned"] = tags_assigned

        tags_unassigned = (
            Tag.objects.filter(contacts__pk__in=self.get_queryset())
            .exclude(pk__in=tags_assigned)
            .distinct()
        )
        ctx["tags_unassigned"] = tags_unassigned

        return ctx

    def _apply_user_filter(self, queryset: QuerySet) -> QuerySet:
        queryset = queryset.filter(owner=self.request.user)
        return queryset

    def _apply_tags_filter(self, queryset: QuerySet) -> QuerySet:
        profile = usecases.GetProfileUseCase(user=self.request.user)()
        for tag in profile.search_tags.all():
            queryset = queryset.filter(tags__pk=tag.pk)
        return queryset


class ContactCreateView(LoginRequiredMixin, generic.CreateView):
    model = Contact
    fields: Any = "__all__"
    success_url = "/~/jana_sergienko/contacts/"
    template_name = "app_jana_sergienko/addContacts.html"
    extra_context = {
        "form": ContactForm(),
    }


class ContactsView(LoginRequiredMixin, generic.FormView):
    form_class = ContactForm
    success_url = "/~/jana_sergienko/contacts/"
    template_name = "app_jana_sergienko/contacts.html"

    def get_context_data(self, **kwargs: dict) -> dict:
        object_list = super().get_context_data(**kwargs)

        get_all_contacts = usecases.GetAllContactsUseCase()
        object_list["object_list"] = get_all_contacts()

        return object_list

    def form_valid(self, form: forms.Form) -> HttpResponse:
        contact = ContactSchema.parse_obj(form.cleaned_data)

        save_contact = usecases.SaveContactUseCase(contact)
        save_contact()

        return super().form_valid(form)


class ContactDetailsView(LoginRequiredMixin, generic.DetailView):
    model = Contact

    def get_context_data(self, **kwargs: dict) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

        tags_assigned = usecases.GetTagsAssignedUseCase(contact=self.object)()
        tags_unassigned = usecases.GetTagsUnassignedUseCase(
            contact=self.object
        )()

        ctx.update(
            {
                "tags_assigned": tags_assigned,
                "tags_unassigned": tags_unassigned,
            }
        )

        return ctx


class ContactDeleteView(  # type: ignore
    LoginRequiredMixin, generic.DeleteView
):
    model = Contact
    success_url = "/~/jana_sergienko/contacts/"


class ContactUpdateView(LoginRequiredMixin, generic.UpdateView):
    extra_context = {"action": "Update"}
    fields: Any = "__all__"
    model = Contact

    def get_success_url(self) -> str:
        return f"/~/jana_sergienko/contacts/{self.object.pk}/"
