from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey


# Create your models here.

# Appontments

class Appointment(models.Model):

    patient = models.ForeignKey(User,on_delete=models.CASCADE,related_name="appointment_patient")
    doctor = models.ForeignKey(User,on_delete=models.CASCADE,related_name="appointment_doctor")
    
    date = models.DateField(blank=False)
    time = models.TimeField(blank=False)
    status = models.CharField(default="pending",blank=True, max_length=20)

    def __str__(self) -> str:
        return f"(Status :{self.status})"
    
class Symptom(models.Model):
    appointment = ForeignKey(Appointment,on_delete=models.CASCADE)
    symptom = models.TextField(max_length=200)

    def __str__(self) -> str:
        return f"('symptom', '{self.symptom}')"

class TestResult(models.Model):
    appointment = ForeignKey(Appointment,on_delete=models.CASCADE)
    blood_pressure = models.IntegerField(blank=False)
    blood_sugar = models.IntegerField(blank=False)
    bmi = models.IntegerField(blank=False)
    hemoglobin = models.IntegerField(blank=False)
    platelets = models.IntegerField(blank=False)

    def __str__(self) -> str:
        return f"[(Blood Pressure: {self.blood_pressure}),(BMI: {self.bmi}),(Blood Sugar :{self.blood_sugar})]"


class Medicine(models.Model):
    appointment = ForeignKey(Appointment,on_delete=models.CASCADE)
    medicine = models.TextField(max_length=500, default="Not examined yet")

    def __str__(self) -> str:
        return f"('medicine', '{self.medicine}')"


class Disease(models.Model):
    appointment = ForeignKey(Appointment,on_delete=models.CASCADE)
    disease = models.TextField(max_length=500, default="Not examined yet")


    def __str__(self) -> str:
        return f"('disease', '{self.disease}')"



class CurrentAppointments(models.Model):
    doctor = models.OneToOneField(User,on_delete=models.CASCADE)
    appointments = models.IntegerField(default=0, blank=True)

    def __str__(self) -> str:
        return f"[('doctor','{self.doctor}'),('appointments','{self.appointments}')]"
