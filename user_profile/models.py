import datetime

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='profile'
    )
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=20)
    surname = models.CharField('Отчество', max_length=20)
    date_of_birth = models.CharField('Дата рождения', max_length=10)
    phone_regex = RegexValidator(
        regex=r'^\+375\d{9}$',
        message='Введите номер в формате +375..........',
    )
    phone_number = models.CharField(max_length=13, validators=[phone_regex], null=True)
    passport_number = models.CharField('Номер паспорта', max_length=14, null=True)
    GENDER_CHOICES = [
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    ]
    gender = models.CharField('Пол', max_length=10, choices=GENDER_CHOICES)
    registration = models.CharField('Регистрация', max_length=50)

    def __str__(self) -> str:
        return self.first_name

    def get_absolute_url(self) -> str:
        return reverse("user_profile:detail_profile", kwargs={"pk": self.pk})

    @property
    def age(self) -> int:
        birthday = datetime.datetime.strptime(self.date_of_birth, '%Y-%m-%d').date()
        today = datetime.date.today()
        age = (
            today.year
            - birthday.year
            - ((today.month, today.day) < (birthday.month, birthday.day))
        )
        return age


class ProfileDoctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile_doctor'
    )
    image = models.ImageField(upload_to="profile_images/")
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=20)
    surname = models.CharField('Отчество', max_length=20)
    speciality = models.CharField('Специальность', max_length=20)
    date_of_birth = models.CharField('Дата рождения', max_length=10)
    phone_regex = RegexValidator(
        regex=r'^\+375\d{9}$',
        message='Введите номер в формате +375..........',
    )
    phone_number = models.CharField(max_length=13, validators=[phone_regex], null=True)

    def __str__(self) -> str:
        return self.first_name

    def get_absolute_url(self) -> str:
        return reverse("user_profile:detail_profile_doctor", kwargs={"pk": self.pk})

    @property
    def age(self) -> int:
        birthday = datetime.datetime.strptime(self.date_of_birth, '%Y-%m-%d').date()
        today = datetime.date.today()
        age = (
            today.year
            - birthday.year
            - ((today.month, today.day) < (birthday.month, birthday.day))
        )
        return age


class Treatment(models.Model):
    patient = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='received_treatments'
    )
    creator = models.ForeignKey(
        ProfileDoctor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_treatments',
    )
    date = models.DateTimeField(auto_now_add=True)
    disability = models.CharField(
        "Временная не трудоспособность:", max_length=10, null=True
    )
    scabies = models.BooleanField("Чесотка", null=True)
    pedeculosis = models.BooleanField("Педикулез", null=True)
    MOOD_CHOICES = [
        ('Амбулаторный', 'Амбулаторный'),
        ('Стационарный', 'Стационарный'),
    ]
    mode = models.CharField('Режим', max_length=20, choices=MOOD_CHOICES, null=True)
    temperature = models.CharField('Температура', max_length=10, null=True)
    arterial_pressure = models.CharField(
        'Артериальное давление', max_length=10, null=True
    )
    pulse = models.CharField('Пульс', max_length=10, null=True)
    complaints = models.CharField("Жалобы:", max_length=500, null=True)
    anamnesis = models.CharField("Анамнез:", max_length=500, null=True)
    general_state = models.CharField("Общее состояние:", max_length=500, null=True)
    SKIN_CHOICES = [
        ('Блкдно-розовые', 'Бледно-розовые'),
        ('Икторичные', 'Икторичные'),
        ('Бледные', 'Бледные'),
        ('Теплые', 'Теплые'),
        ('Сухие', 'Сухие'),
    ]
    skin = models.CharField(
        'Кожные покровы:', max_length=20, choices=SKIN_CHOICES, null=True
    )
    peritoneal_symptoms = models.CharField(
        'Перитонеальные симптомы:', max_length=500, null=True
    )
    ARTERIAL_PULSATION_CHOICES = [
        ('Сохранена', 'Сохранена'),
        ('Ослабленная', 'Ослабленная'),
    ]
    arterial_pulsation = models.CharField(
        'Артериальная пульсация:',
        max_length=20,
        choices=ARTERIAL_PULSATION_CHOICES,
        null=True,
    )
    stool = models.BooleanField("Стул нарушен:", null=True)
    urination = models.BooleanField("Мочеиспускание нарушено:", null=True)
    diagnosis = models.CharField("Диагноз:", max_length=100, null=True)
    treatment = models.CharField("Лечение:", max_length=300, null=True)
    recommendations = models.CharField("Рекомендации:", max_length=300, null=True)
    test_oak = models.BooleanField("ОАК:", null=True)
    test_oam = models.BooleanField("ОАМ:", null=True)
    test_bak = models.BooleanField("БАК:", null=True)
    test_kog = models.BooleanField("Коагудограмма:", null=True)
    test_x_ray = models.BooleanField("Ренген:", null=True)
    test_ecg = models.BooleanField("ЭКГ:", null=True)
    test_ultrasound = models.BooleanField("УЗИ:", null=True)

    def get_absolute_url(self) -> str:
        return reverse("user_profile:detail_treatment", kwargs={"pk": self.pk})


class Reservation(models.Model):
    reserved_user = models.ForeignKey(
        'user_profile.Profile',
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    reserved_doctor = models.ForeignKey(
        'user_profile.ProfileDoctor',
        on_delete=models.CASCADE,
        related_name='reservation',
    )
    AVAILABLE_TIME_CHOICES = [
        ('9:00', '9:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
    ]
    booking_date = models.DateField()
    available_time = models.CharField(
        'Время бронирования:', max_length=20, choices=AVAILABLE_TIME_CHOICES
    )

    def get_absolute_url(self) -> str:
        return reverse("user_profile:detail_reservation", kwargs={"pk": self.pk})
