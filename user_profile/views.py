from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic

from .models import Profile


class ProfileCreateView(LoginRequiredMixin, generic.CreateView):
    model = Profile
    fields = [
        "image",
        "first_name",
        "last_name",
        "surname",
        "date_of_birth",
        "gender",
        "registration",
    ]
    template_name = "user_profile/create_profile.html"

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileDetailView(generic.DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = "user_profile/detail_profile.html"
