from django.contrib import admin
from .models import (UsersInfo, DoctorInfo, UsersInfoAdminView,
                        Appointment,CurrentAppointments, Symptom, Medicine, TestResult,Disease)
# Register your models here.


admin.site.register(UsersInfo,UsersInfoAdminView)
admin.site.register(DoctorInfo)
admin.site.register(Appointment)
admin.site.register(CurrentAppointments)
admin.site.register(Symptom)
admin.site.register(Medicine)
admin.site.register(TestResult)
admin.site.register(Disease)