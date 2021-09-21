from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models import fields

from django.db.models.fields.related import ForeignKey, OneToOneField
import os


YEAR = [ year for year in range(1990,2050) ]
MONTHS = ["January","Feburary","March","Aprill","May","June","July","Auguest","September","October","November","December"]


def path_and_rename(instance, filename):
    try:
        upload_to = "Images/"
        ext = filename.split('.')[-1]
        username = instance.user.username
        print(username)
        if username:
            filename = f"Users_profile_pictures/{username}.{ext}"
        path = os.path.join(upload_to,filename)
        return path
    except:
        raise ValueError("Instance error")


class UsersInfo(models.Model):
    
    user = OneToOneField(User,on_delete=models.CASCADE)
    doctor = "doctor"
    patient = "patient"
    user_type = [
        (doctor,"Doctor"),
        (patient,"Patient")
    ]
    role = models.CharField(max_length=10,choices=user_type,default=patient)
    # age = models.IntegerField(null=True,blank=True)
    age = models.IntegerField()
    city = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    mobile_number = models.IntegerField()
    profile_picture = models.ImageField(upload_to = path_and_rename,blank=True)

    
    def __str__(self) -> str:
        return f"(username : {self.user.username}),(role : {self.role})"

class UsersInfoAdminView(admin.ModelAdmin):
    list_display = ["user_id","role","age","city","country","mobile_number"]

class DoctorInfo(models.Model):
    user_info = OneToOneField(UsersInfo,on_delete=models.CASCADE)
    expertise = models.CharField(max_length=30)
    qualification = models.CharField(max_length=30)



    def __str__(self) -> str:
        return f"(Username : {self.user_info.user.username}), (expertise, {self.expertise}),\
            (qualification : {self.qualification})"


# Appontments

class Appointment(models.Model):

    patient = models.ForeignKey(User,on_delete=models.CASCADE,related_name="appointment_patient")
    doctor = models.ForeignKey(User,on_delete=models.CASCADE,related_name="appointment_doctor")
    
    # patient = models.ForeignKey(UsersInfo,on_delete=models.CASCADE,null=True, blank=True)
    # doctor = models.ForeignKey(DoctorInfo,on_delete=models.CASCADE,null=True, blank=True)

    
    # patient = models.ManyToManyField(User, related_name="patient_user")
    # doctor = models.ManyToManyField(User,related_name="doctor_user")



    date = models.DateField(blank=False)
    time = models.TimeField(blank=False)
    status = models.CharField(default="pending",blank=True, max_length=20)

    def __str__(self) -> str:
        return f"(Status :{self.status})"
    
class Symptoms(models.Model):
    appointment = ForeignKey(Appointment,on_delete=models.CASCADE)
    blood_pressure = models.IntegerField(blank=False)
    blood_sugar = models.IntegerField(blank=False)
    bmi = models.IntegerField(blank=False)
    hemoglobin = models.IntegerField(blank=False)
    platelets = models.IntegerField(blank=False)

    def __str__(self) -> str:
        return f"[(Blood Pressure: {self.blood_pressure}),(BMI: {self.bmi}),(Blood Sugar :{self.blood_sugar})]"




class CurrentAppointments(models.Model):
    doctor = models.OneToOneField(User,on_delete=models.CASCADE)
    appointments = models.IntegerField(default=0, blank=True)

    def __str__(self) -> str:
        return f"[('doctor','{self.doctor}'),('appointments','{self.appointments}')]"
