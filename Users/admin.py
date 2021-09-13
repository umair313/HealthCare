from django.contrib import admin
from .models import UsersInfo, DoctorInfo
# Register your models here.


admin.site.register(UsersInfo)
admin.site.register(DoctorInfo)