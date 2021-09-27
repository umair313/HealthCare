from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (Home, register, profile_view, patient_profile,
                        doctors_list_view,doctor_profile,patients,
                        searchpage,search)

urlpatterns = [
    # home
    path("",Home,name="Home"),
    # users
    path("register/",register, name="register"),
    path("login/",auth_views.LoginView.as_view(template_name="users/login.html"),name="login"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path("profile/",profile_view,name="profile"),
    
    # patient
    path("searchpage/",searchpage,name="searchpage"),
    path("search/",search,name="search"),
    path("view/doctor_profile/<int:doctor_id>/",doctor_profile,name="view-doctor-profile"),
    path("doctors/", doctors_list_view,name="doctors"),
    
    # doctor

    path("patients/",patients,name="patients"),

    # common in patient and doctor
    path("patient/profile/<int:patient_id>/",patient_profile,name="patient-profile"),


]