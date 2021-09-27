from django.contrib import admin
from .models import UsersInfo, DoctorInfo, UsersInfoAdminView
                        
# Register your models here.


admin.site.register(UsersInfo,UsersInfoAdminView)
admin.site.register(DoctorInfo)
