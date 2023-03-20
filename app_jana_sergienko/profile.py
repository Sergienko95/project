from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from app_jana_sergienko.bob import usecases
from app_jana_sergienko.models import Profile


class ProfileDetailsView(LoginRequiredMixin, generic.DetailView):
    model = Profile

    def get_object(self, queryset: Any = None) -> Any:
        return usecases.GetProfileUseCase(user=self.request.user)()


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    fields = ["preferences"]
    model = Profile
    success_url = "/~/jana_sergienko/profile/"

    def get_object(self, queryset: Any = None) -> Any:
        return usecases.GetProfileUseCase(user=self.request.user)()
