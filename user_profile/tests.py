from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            image=None,
            first_name='Test',
            last_name='User',
            surname='Surname',
            date_of_birth='2000-01-01',
            phone_number='+375123456789',
            passport_number='AB1234567',
            gender='M',
            registration='Test Registration',
        )

    def test_non_staff_user_can_view_own_profile(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('user_profile:detail_profile', kwargs={'pk': self.profile.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_non_staff_user_cannot_view_other_profiles(self):
        other_user = User.objects.create_user(
            username='otheruser', password='otherpassword'
        )
        other_profile = Profile.objects.create(
            user=other_user,
            image=None,
            first_name='Other',
            last_name='User',
            surname='Surname',
            date_of_birth='1990-01-01',
            phone_number='+375987654321',
            passport_number='CD9876543',
            gender='F',
            registration='Other Registration',
        )

        self.client.login(username='testuser', password='testpassword')

        url = reverse('user_profile:detail_profile', kwargs={'pk': other_profile.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)
