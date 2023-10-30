from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
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
