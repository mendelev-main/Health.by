from django import forms
from django.core.exceptions import ValidationError

from .models import Reservation


class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['booking_date']
        widgets = {'booking_date': forms.DateInput(attrs={'type': 'date'})}


class AvailableTimeSelectForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['available_time']

    def clean_available_time(self):
        existing_reservations = Reservation.objects.filter(
            booking_date=self.instance.booking_date,
            available_time=self.cleaned_data['available_time'],
            reserved_doctor=self.instance.reserved_doctor,
        )

        if existing_reservations.exists():
            raise ValidationError('This time slot is already booked.')

        return self.cleaned_data['available_time']

    available_time = forms.ChoiceField(
        choices=Reservation.AVAILABLE_TIME_CHOICES, required=True
    )
