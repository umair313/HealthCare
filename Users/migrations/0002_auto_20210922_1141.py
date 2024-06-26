# Generated by Django 3.2.7 on 2021-09-22 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Symptoms',
            new_name='TestResult',
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptom', models.CharField(default='Not examined yet', max_length=200)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.appointment')),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine', models.TextField(default='Not examined yet', max_length=500)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.appointment')),
            ],
        ),
    ]
