# Generated by Django 4.2.6 on 2023-11-16 17:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user_profile', '0002_alter_treatment_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiledoctor',
            name='speciality',
            field=models.CharField(
                max_length=20, null=True, verbose_name='Специальность'
            ),
        ),
    ]
