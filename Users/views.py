from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import (MedicineForm, userRegistrationForm ,UserInfoForm,
                        DoctorInfoForm, SymtomsForm, TestResultForm, DiseaseForm)
from .models import (UsersInfo, DoctorInfo, Appointment, 
                        CurrentAppointments, Medicine, Disease)





info_message = "Please Select Data and time and check for availale slot.\
If the slot is availbe then you can provide other information and book your Appointment."


# for uer login
# from django.contrib.auth import authenticate, logout, login as auth_login


# Create your views here.
def Home(request):
    user = request.user
    if user.is_authenticated:
        user_info = UsersInfo.objects.filter(user=user).first()
        if user_info:
            return render(request,"users/dashboard.html",context={"user_info":user_info,"dashboard":True})
    return render(request,"users/index.html")


def register(request): 
    if request.method == "POST":
        # if request is post then get the froms data in relevant forms
        registration_form = userRegistrationForm(request.POST)
        doctor_info_form = DoctorInfoForm(request.POST)
        # as their is also a image file field so 
        # we need request.FILES object to get that
        user_info_form = UserInfoForm(request.POST, request.FILES or None)
        # check form for validation
        if registration_form.is_valid() and user_info_form.is_valid():
            # if form is valid save user
            user = registration_form.save()
            user.save()
            # save user_info
            #  
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.save()
            # if role is doctor then add additional doctor information for doctor
            if user_info.role == "doctor" and doctor_info_form.is_valid():
                # save doctor information in doctor model 
                doctor_info = doctor_info_form.save(commit=False)
                doctor_info.user_info = user_info
                doctor_info.save()
                # if user is doctor then add appointments to 0 
                CurrentAppointments.objects.create(doctor = user)
            # redirect to login after successfull register
            return redirect('login')
        else:
            # if forms are invalid the resend the forms with errors
            context = {
                        "formRegistration": registration_form,
                        "formUserInfo": user_info_form,
                        "formDoctorInfo": doctor_info_form
                    }
            # display some errors
            print(registration_form.errors)
            print(user_info_form.errors)
            print(doctor_info_form.errors)

            return render(request, "users/register.html" , context=context)

    # if request is get then do the following
    registration_form = userRegistrationForm()
    user_info_form = UserInfoForm()
    doctor_info_form = DoctorInfoForm()
    context = {
        "formRegistration": registration_form,
        "formUserInfo": user_info_form,
        "formDoctorInfo": doctor_info_form
    }
    return render(request, "users/register.html" , context=context)




@login_required
def profile_view(request):
    # current user profile view
    # get the current user
    # get user info
    # craete context
    # if doctor then get doctor infomation
    # add this to context     
    user = request.user
    user_info = UsersInfo.objects.filter(user=user).first()
    context = {"user_info": user_info,"profile":True}
    if user_info.role == "doctor":
        doctor_info = DoctorInfo.objects.filter(user_info=user_info).first()
        context["doctor_info"] = doctor_info
    return render(request,"users/profile.html",context=context)


@login_required
def doctors_list_view(request):
    user = request.user
    doctors = DoctorInfo.objects.all()
    user_info = UsersInfo.objects.filter(user = user).first()
    return render(request, "users/doctors.html",context={"doctors":doctors,"user_info":user_info})


@login_required
def doctor_profile(request,doctor_id):
    user = User.objects.filter(id=doctor_id).first()
    user_info= UsersInfo.objects.filter(user = request.user).first()
    if user:
        doctor_user_info = UsersInfo.objects.filter(user=user).first()
        doctor_info = DoctorInfo.objects.filter(user_info=doctor_user_info).first()
        
    return render(request, "users/doctor_profile.html",context={"doctor_profile":True,"doctor_info":doctor_info,"user_info":user_info})


@login_required
def makeAppointmentForm(request,doctor_id):
    user_info = UsersInfo.objects.filter(user=request.user).first()
    symptoms_From = SymtomsForm()
    test_result_form = TestResultForm()
    user_doctor = User.objects.filter(id=doctor_id).first()
    if user_doctor:
        current = CurrentAppointments.objects.filter(doctor=user_doctor).first()
        if current:
            if current.appointments >= 0 and current.appointments < 10 :
                messages.info(request,info_message)
                messages.success(request,"Slot is available. you can make appointment.")
                return render(request, "users/makeAppointment.html", context={
                                            "do_appointment": True,
                                            "user_info":user_info,
                                            "symptomForm": symptoms_From,
                                            "test_result_form": test_result_form,
                                            "doctor_id": user_doctor.id
                })
            else:
                messages.error(request,"Slot is not available for this doctor.")
                return render(request, "users/appointmentErrorPage.html", context={"do_appointment": True,
                "user_info":user_info,"doctor_id": user_doctor.id})
    else:
        return redirect('doctors')


@login_required
def bookAppointment(request,doctor_id):
    # Bokk an appointment
    user_info = UsersInfo.objects.filter(user=request.user).first()
    symptoms_From = SymtomsForm()
    test_result_form = TestResultForm()
    user_doctor = User.objects.filter(id=doctor_id).first()
    if request.method == "POST":
        # get date and time fro mrequest
        date = request.POST["date"]
        time = request.POST["time"]
        symptoms_form = SymtomsForm(request.POST)
        test_result_form = TestResultForm(request.POST)
        # first check if there is already an appointment for given date and time
        if Appointment.objects.filter(date = date, time = time).first():
            messages.info(request,info_message)
            messages.success(request,"Slot is available. you can make appointment.")
            messages.error(request,"Selected date and time is not available. please select other date and time.")
            return render(request, "users/makeAppointment.html", context={
                                            "do_appointment": True,
                                            "user_info":user_info,
                                            "symptomForm": symptoms_From,
                                            "test_result_form": test_result_form,
                                            "doctor_id": user_doctor.id
                })
        # geting doctor and patient  user form User
       
        patient_user = request.user
        doctor_user = User.objects.filter(id=doctor_id).first()
        
        # book the appointment
        new_appointment = Appointment.objects.create(patient=patient_user,doctor=doctor_user,
                                                        date=date, time=time, status = "pending")

        # symptoms         
        symptoms = symptoms_form.save(commit=False)
        symptoms.appointment = new_appointment
        symptoms.save()

        # test results
        test_result = test_result_form.save(commit=False)
        test_result.appointment = new_appointment
        test_result.save()

        # medicine 
        medicine = Medicine.objects.create(appointment= new_appointment)
        medicine.save()

        # Disease 
        disease = Disease.objects.create(appointment = new_appointment)
        disease.save()
        
        # update doctors current active appointments
        current = CurrentAppointments.objects.filter(doctor=doctor_user).first()
        current.appointments += 1
        current.save()
        messages.success(request,"Your Appointment booked successfully.")
        return render(request, "users/appointmentErrorPage.html", context={"do_appointment": True,
                "user_info":user_info,"doctor_id": user_doctor.id})

    return redirect('doctors')

@login_required
def all_appointments(request):
    user = request.user
    if user:
        if user.usersinfo.role == "patient" :
            _all_appointmments = Appointment.objects.filter(patient = user)
            return render(request, "users/appointments.html",context={"appointments":_all_appointmments})
        else:
            _all_appointmments = Appointment.objects.filter(doctor = user)
            return render(request, "users/appointments.html",context={"appointments":_all_appointmments})
    return HttpResponse("Lose return from All_appointment view")

@login_required
def patients(request):
    user = request.user
    if user.usersinfo.role == "doctor":
        appointments = user.appointment_doctor.all()
        return render(request,"users/patients.html",context={"doctor_app":appointments})



@login_required
def patient_profile(request,patient_id):
    patient = User.objects.filter(id=patient_id).first()
    return render(request, "users/patient_profile.html",context={"patient":patient})




@login_required
def view_appointment(request,id):
    appointment = Appointment.objects.filter(id=id).first()
    
    symptom = appointment.symptom_set.first()
    test = appointment.testresult_set.first()
    medicine = appointment.medicine_set.first()
    disease = appointment.disease_set.first()
    context = {
        "symptom" : symptom,
        "test": test,
        "medicine":medicine,
        "disease": disease,
    }
    return render(request, "users/view_appointment.html",context=context)

@login_required
def attend_appointment_form(request,id):
    appointment = Appointment.objects.filter(id=id).first()
    symptom = appointment.symptom_set.first()
    test = appointment.testresult_set.first()
    medicine = MedicineForm()
    disease = DiseaseForm()
    context = {
        "symptom" : symptom,
        "test": test,
        "medicine":medicine,
        "disease": disease,
    }
    return render(request, "users/attend_appointment.html",context=context)