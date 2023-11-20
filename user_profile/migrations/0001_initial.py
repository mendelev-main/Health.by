# Generated by Django 4.2.6 on 2023-11-20 20:25

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name='profile',
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'image',
                    models.ImageField(
                        blank=True, null=True, upload_to='profile_images/'
                    ),
                ),
                ('first_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=20, verbose_name='Фамилия')),
                ('surname', models.CharField(max_length=20, verbose_name='Отчество')),
                (
                    'date_of_birth',
                    models.CharField(max_length=10, verbose_name='Дата рождения'),
                ),
                (
                    'phone_number',
                    models.CharField(
                        max_length=13,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message='Введите номер в формате +375..........',
                                regex='^\\+375\\d{9}$',
                            )
                        ],
                    ),
                ),
                (
                    'passport_number',
                    models.CharField(
                        max_length=14, null=True, verbose_name='Номер паспорта'
                    ),
                ),
                (
                    'gender',
                    models.CharField(
                        choices=[('M', 'Мужчина'), ('F', 'Женщина')],
                        max_length=10,
                        verbose_name='Пол',
                    ),
                ),
                (
                    'registration',
                    models.CharField(max_length=50, verbose_name='Регистрация'),
                ),
            ],
        ),
        migrations.CreateModel(
            name='ProfileDoctor',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('image', models.ImageField(upload_to='profile_images/')),
                ('first_name', models.CharField(max_length=20, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=20, verbose_name='Фамилия')),
                ('surname', models.CharField(max_length=20, verbose_name='Отчество')),
                (
                    'speciality',
                    models.CharField(max_length=20, verbose_name='Специальность'),
                ),
                (
                    'date_of_birth',
                    models.CharField(max_length=10, verbose_name='Дата рождения'),
                ),
                (
                    'phone_number',
                    models.CharField(
                        max_length=13,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message='Введите номер в формате +375..........',
                                regex='^\\+375\\d{9}$',
                            )
                        ],
                    ),
                ),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='profile_doctor',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('date', models.DateTimeField(auto_now_add=True)),
                (
                    'disability',
                    models.CharField(
                        max_length=10,
                        null=True,
                        verbose_name='Временная не трудоспособность:',
                    ),
                ),
                ('scabies', models.BooleanField(null=True, verbose_name='Чесотка')),
                (
                    'pedeculosis',
                    models.BooleanField(null=True, verbose_name='Педикулез'),
                ),
                (
                    'mode',
                    models.CharField(
                        choices=[
                            ('Амбулаторный', 'Амбулаторный'),
                            ('Стационарный', 'Стационарный'),
                        ],
                        max_length=20,
                        null=True,
                        verbose_name='Режим',
                    ),
                ),
                (
                    'temperature',
                    models.CharField(
                        max_length=10, null=True, verbose_name='Температура'
                    ),
                ),
                (
                    'arterial_pressure',
                    models.CharField(
                        max_length=10, null=True, verbose_name='Артериальное давление'
                    ),
                ),
                (
                    'pulse',
                    models.CharField(max_length=10, null=True, verbose_name='Пульс'),
                ),
                (
                    'complaints',
                    models.CharField(max_length=500, null=True, verbose_name='Жалобы:'),
                ),
                (
                    'anamnesis',
                    models.CharField(
                        max_length=500, null=True, verbose_name='Анамнез:'
                    ),
                ),
                (
                    'general_state',
                    models.CharField(
                        max_length=500, null=True, verbose_name='Общее состояние:'
                    ),
                ),
                (
                    'skin',
                    models.CharField(
                        choices=[
                            ('Блкдно-розовые', 'Бледно-розовые'),
                            ('Икторичные', 'Икторичные'),
                            ('Бледные', 'Бледные'),
                            ('Теплые', 'Теплые'),
                            ('Сухие', 'Сухие'),
                        ],
                        max_length=20,
                        null=True,
                        verbose_name='Кожные покровы:',
                    ),
                ),
                (
                    'peritoneal_symptoms',
                    models.CharField(
                        max_length=500,
                        null=True,
                        verbose_name='Перитонеальные симптомы:',
                    ),
                ),
                (
                    'arterial_pulsation',
                    models.CharField(
                        choices=[
                            ('Сохранена', 'Сохранена'),
                            ('Ослабленная', 'Ослабленная'),
                        ],
                        max_length=20,
                        null=True,
                        verbose_name='Артериальная пульсация:',
                    ),
                ),
                ('stool', models.BooleanField(null=True, verbose_name='Стул нарушен:')),
                (
                    'urination',
                    models.BooleanField(
                        null=True, verbose_name='Мочеиспускание нарушено:'
                    ),
                ),
                (
                    'diagnosis',
                    models.CharField(
                        max_length=100, null=True, verbose_name='Диагноз:'
                    ),
                ),
                (
                    'treatment',
                    models.CharField(
                        max_length=300, null=True, verbose_name='Лечение:'
                    ),
                ),
                (
                    'recommendations',
                    models.CharField(
                        max_length=300, null=True, verbose_name='Рекомендации:'
                    ),
                ),
                ('test_oak', models.BooleanField(null=True, verbose_name='ОАК:')),
                ('test_oam', models.BooleanField(null=True, verbose_name='ОАМ:')),
                ('test_bak', models.BooleanField(null=True, verbose_name='БАК:')),
                (
                    'test_kog',
                    models.BooleanField(null=True, verbose_name='Коагудограмма:'),
                ),
                ('test_x_ray', models.BooleanField(null=True, verbose_name='Ренген:')),
                ('test_ecg', models.BooleanField(null=True, verbose_name='ЭКГ:')),
                (
                    'test_ultrasound',
                    models.BooleanField(null=True, verbose_name='УЗИ:'),
                ),
                (
                    'creator',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='created_treatments',
                        to='user_profile.profiledoctor',
                    ),
                ),
                (
                    'patient',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='received_treatments',
                        to='user_profile.profile',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('booking_date', models.DateField()),
                (
                    'available_time',
                    models.CharField(
                        choices=[
                            ('9:00', '9:00'),
                            ('10:00', '10:00'),
                            ('11:00', '11:00'),
                            ('12:00', '12:00'),
                            ('13:00', '13:00'),
                            ('14:00', '14:00'),
                            ('15:00', '15:00'),
                            ('16:00', '16:00'),
                            ('17:00', '17:00'),
                        ],
                        max_length=20,
                        verbose_name='Время бронирования:',
                    ),
                ),
                (
                    'reserved_doctor',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='reservation',
                        to='user_profile.profiledoctor',
                    ),
                ),
                (
                    'reserved_user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='reservations',
                        to='user_profile.profile',
                    ),
                ),
            ],
        ),
    ]
