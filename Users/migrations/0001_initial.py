# Generated by Django 3.2.7 on 2021-09-21 04:58

import Users.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('status', models.CharField(blank=True, default='pending', max_length=20)),
                ('doctor', models.ManyToManyField(related_name='doctor_user', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ManyToManyField(related_name='patient_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsersInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('doctor', 'Doctor'), ('patient', 'Patient')], default='patient', max_length=10)),
                ('age', models.IntegerField()),
                ('city', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=10)),
                ('mobile_number', models.IntegerField()),
                ('profile_picture', models.ImageField(blank=True, upload_to=Users.models.path_and_rename)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Symptoms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_pressure', models.IntegerField()),
                ('blood_sugar', models.IntegerField()),
                ('bmi', models.IntegerField()),
                ('hemoglobin', models.IntegerField()),
                ('platelets', models.IntegerField()),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.appointment')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertise', models.CharField(max_length=30)),
                ('qualification', models.CharField(max_length=30)),
                ('user_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Users.usersinfo')),
            ],
        ),
        migrations.CreateModel(
            name='CurrentAppointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointments', models.IntegerField(blank=True, default=0)),
                ('doctor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
