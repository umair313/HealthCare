from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField
from django.forms.utils import flatatt



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

    
    def __str__(self) -> str:
        return f"(username : {self.user.username}),(role : {self.role})"

class DoctorInfo(models.Model):
    user = OneToOneField(User,on_delete=models.CASCADE)
    expertise = models.CharField(max_length=30)
    qualification = models.CharField(max_length=30)



    def __str__(self) -> str:
        return f"(Username : {self.user.username}), (expertise, {self.expertise}),\
            (qualification): {self.qualification}"


    
    






