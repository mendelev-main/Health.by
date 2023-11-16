from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.generic import ListView

from .models import Profile, ProfileDoctor, Treatment


class ProfileCreateView(LoginRequiredMixin, generic.CreateView):
    model = Profile
    fields = [
        "image",
        "first_name",
        "last_name",
        "surname",
        "date_of_birth",
        "phone_number",
        "passport_number",
        "gender",
        "registration",
    ]
    template_name = "user_profile/create_profile.html"

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileDoctorCreateView(
    UserPassesTestMixin, LoginRequiredMixin, generic.CreateView
):
    model = ProfileDoctor
    fields = [
        "image",
        "first_name",
        "last_name",
        "surname",
        "date_of_birth",
        "phone_number",
    ]
    template_name = "user_profile/create_profile_doctor.html"

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('user_profile:create_profile'))


class ProfileDetailView(UserPassesTestMixin, generic.DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = "user_profile/detail_profile.html"

    def test_func(self):
        is_admin = self.request.user.is_staff
        is_profile_owner = self.request.user.id == self.get_object().user.id
        is_staff_profile = self.get_object().user.is_staff
        return is_admin or (not is_admin and (is_profile_owner or is_staff_profile))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        treatments = self.object.received_treatments.all()

        context['treatments'] = treatments

        return context


class ProfileDoctorDetailView(UserPassesTestMixin, generic.DetailView):
    model = ProfileDoctor
    context_object_name = 'profile_doctor'
    template_name = "user_profile/detail_profile_doctor.html"

    def test_func(self):
        is_admin = self.request.user.is_staff
        is_profile_owner = self.request.user.id == self.get_object().user.id
        is_staff_profile = self.get_object().user.is_staff
        return is_admin or (not is_admin and (is_profile_owner or is_staff_profile))


class TreatmentCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Treatment
    fields = [
        'disability',
        'scabies',
        'pedeculosis',
        'mode',
        'temperature',
        'arterial_pressure',
        'pulse',
        'complaints',
        'anamnesis',
        'general_state',
        'skin',
        'peritoneal_symptoms',
        'arterial_pulsation',
        'stool',
        'urination',
        'diagnosis',
        'treatment',
        'recommendations',
        'test_oak',
        'test_oam',
        'test_bak',
        'test_kog',
        'test_x_ray',
        'test_ecg',
        'test_ultrasound',
    ]
    template_name = "user_profile/create_treatment.html"

    def form_valid(self, form) -> HttpResponse:
        creator = self.request.user.profile_doctor
        patient_pk = self.kwargs['pk']
        patient = get_object_or_404(Profile, pk=patient_pk)
        form.instance.creator = creator
        form.instance.patient = patient

        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff


class TreatmentIndexView(generic.DetailView):
    model = Treatment
    context_object_name = 'treatment'
    template_name = "user_profile/detail_profile.html"


class TreatmentDetailView(generic.DetailView):
    model = Treatment
    context_object_name = 'treatment'
    template_name = "user_profile/detail_treatment.html"


class SearchView(UserPassesTestMixin, ListView):
    model = Profile
    template_name = 'user_profile/index.html'

    def get_queryset(self):
        queryset = Profile.objects.all()
        q = self.request.GET.get("q")
        if q:
            return queryset.filter(
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(phone_number__icontains=q)
                | Q(passport_number__icontains=q)
            )
        return queryset

    def test_func(self):
        return self.request.user.is_staff


class SearchDoctorView(ListView):
    model = ProfileDoctor
    template_name = 'user_profile/search_doctor.html'

    def get_queryset(self):
        queryset = ProfileDoctor.objects.all()
        q = self.request.GET.get("q")
        if q:
            return queryset.filter(
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(phone_number__icontains=q)
                | Q(speciality__icontains=q)
            )
        return queryset

    def test_func(self):
        return not self.request.user.is_staff
