from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import ListView

from .forms import AvailableTimeSelectForm, ReservationCreateForm
from .models import Profile, ProfileDoctor, Reservation, Treatment


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
        "speciality",
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


class ReservationCreateView(generic.CreateView):
    model = Reservation
    form_class = ReservationCreateForm
    template_name = 'user_profile/create_reservation.html'

    def form_valid(self, form):
        reserved_user = self.request.user.profile
        reserved_doctor_pk = self.kwargs['pk']
        reserved_doctor = get_object_or_404(ProfileDoctor, pk=reserved_doctor_pk)
        form.instance.reserved_user = reserved_user
        form.instance.reserved_doctor = reserved_doctor
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'user_profile:create_reservation_second_step', kwargs={'pk': self.object.pk}
        )


class AvailableTimeSelectView(generic.UpdateView):
    model = Reservation
    form_class = AvailableTimeSelectForm
    template_name = 'user_profile/create_reservation_second_step.html'

    def form_valid(self, form):
        reservation = self.get_object()

        if not form.cleaned_data.get('available_time'):
            return HttpResponseRedirect(
                reverse('user_profile:create_reservation')
                + f'?pk={reservation.reserved_doctor.pk}&error=no_time_selected'
            )

        existing_reservations = Reservation.objects.filter(
            booking_date=reservation.booking_date,
            available_time=form.cleaned_data['available_time'],
            reserved_doctor=reservation.reserved_doctor,
        )

        if existing_reservations.exists():
            raise ValidationError('Это время уже занято')

        if form.cleaned_data['available_time']:
            with transaction.atomic():
                reservation.available_time = form.cleaned_data['available_time']
                reservation.save()

        return super().form_valid(form)


class ReservationIndexView(generic.DetailView):
    model = Reservation
    context_object_name = 'reservation'
    template_name = "user_profile/detail_profile_doctor.html"


class ReservationDetailView(generic.DetailView):
    model = Reservation
    context_object_name = 'reservation'
    template_name = "user_profile/detail_reservation.html"
