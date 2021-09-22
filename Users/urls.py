from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (Home, register, profile_view, patient_profile,view_appointment,complete_appointment,
                    doctors_list_view, doctor_profile,makeAppointmentForm,attend_appointment_form,
                    bookAppointment, all_appointments,patients, searchpage,search)

urlpatterns = [
    path("",Home,name="Home"),
    path("searchpage/",searchpage,name="searchpage"),
    path("search/",search,name="search"),
    path("register/",register, name="register"),
    path("login/",auth_views.LoginView.as_view(template_name="users/login.html"),name="login"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path("profile/",profile_view,name="profile"),
    path("doctors/", doctors_list_view,name="doctors"),
    path("view/doctor_profile/<int:doctor_id>/",doctor_profile,name="view-doctor-profile"),
    path("make/appointment/<int:doctor_id>/",makeAppointmentForm,name = "make-Appointment-form"),
    path("book/appointment/<int:doctor_id>",bookAppointment,name="book"),
    path("appointments/",all_appointments,name="appointments"),
    path("patients/",patients,name="patients"),
    path("patient/profile/<int:patient_id>/",patient_profile,name="patient-profile"),
    path("view/appointment/<int:id>/",view_appointment,name="view-appointment"),
    path("attend/appointmet/<int:id>/",attend_appointment_form,name="attend-appointment"),
    path("complete/appointment/<int:id>/",complete_appointment,name="complete-appointment")



]