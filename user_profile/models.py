from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='profile'
    )
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=20)
    surname = models.CharField('Отчество', max_length=20)
    date_of_birth = models.CharField('Дата рождения', max_length=10)

    GENDER_CHOICES = [
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    ]
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES)
    registration = models.CharField('Регистрация', max_length=50)

    def __str__(self) -> str:
        return self.first_name

    def get_absolute_url(self) -> str:
        return reverse("user_profile:detail_profile", kwargs={"pk": self.pk})


@receiver(post_save, sender=User)
def create_user_profile(
    sender: models.Model, instance: User, created: bool, **kwargs
) -> None:
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender: models.Model, instance: User, **kwargs) -> None:
    instance.profile.save()
