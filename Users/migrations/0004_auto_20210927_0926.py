# Generated by Django 3.2.7 on 2021-09-27 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_auto_20210922_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currentappointments',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='disease',
            name='appointment',
        ),
        migrations.RemoveField(
            model_name='medicine',
            name='appointment',
        ),
        migrations.RemoveField(
            model_name='symptom',
            name='appointment',
        ),
        migrations.RemoveField(
            model_name='testresult',
            name='appointment',
        ),
        migrations.DeleteModel(
            name='Appointment',
        ),
        migrations.DeleteModel(
            name='CurrentAppointments',
        ),
        migrations.DeleteModel(
            name='Disease',
        ),
        migrations.DeleteModel(
            name='Medicine',
        ),
        migrations.DeleteModel(
            name='Symptom',
        ),
        migrations.DeleteModel(
            name='TestResult',
        ),
    ]
