from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (view_appointment,
                        pending_appointment,complete_appointment,
                        makeAppointmentForm,attend_appointment_form,
                        bookAppointment, all_appointments,
                        disease_chart_data, get_appointments_by_month)

urlpatterns = [

    path("make/appointment/<int:doctor_id>/",makeAppointmentForm,name = "make-Appointment-form"),
    path("book/appointment/<int:doctor_id>",bookAppointment,name="book"),

    
    # doctor
    path("attend/appointmet/<int:id>/",attend_appointment_form,name="attend-appointment"),
    path("complete/appointment/<int:id>/",complete_appointment,name="complete-appointment"),
    path("appointments/",all_appointments,name="appointments"),
    # doctor ajax requests urls
    path("data/chart/disease/",disease_chart_data,name="disease-chart-data"),
    path("data/chart/appointments",get_appointments_by_month,name="month-appointment"),
    # common in patient and doctor
    path("view/appointment/<int:id>/",view_appointment,name="view-appointment"),
    
    # ajax request for pending apoointment count
    path("appointment/pending/",pending_appointment,name="pending-appointment"),




]