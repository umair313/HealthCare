from django.contrib import admin
from .models import (UsersInfo, DoctorInfo, UsersInfoAdminView,
                        Appointment,currentAppintments, symptoms)
# Register your models here.


admin.site.register(UsersInfo,UsersInfoAdminView)
admin.site.register(DoctorInfo)
admin.site.register(Appointment)
admin.site.register(currentAppintments)
admin.site.register(symptoms)