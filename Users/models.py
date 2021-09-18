from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.forms.utils import flatatt
import os

def path_and_rename(instance, filename):
    try:
        upload_to = "Images/"
        ext = filename.split('.')[-1]
        username = instance.user.pk
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


    
    






