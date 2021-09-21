from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.db.models import query
from django.shortcuts import redirect, render, HttpResponse
from .forms import userRegistrationForm ,UserInfoForm,DoctorInfoForm, SymtomsForm, AppointmentForm
from .models import UsersInfo, DoctorInfo, Appointment, CurrentAppointments, Symptoms
from django.contrib.auth.decorators import login_required


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
    appointment_form = AppointmentForm()
    symptoms_From = SymtomsForm()
    user_doctor = User.objects.filter(id=doctor_id).first()
    if user_doctor:
        current = CurrentAppointments.objects.filter(doctor=user_doctor).first()
        if current:
            if current.appointments >= 0 and current.appointments < 10 :
                messages.info(request,"Please Select Data and \
                                         time and check for availale slot.\
                                         If the slot is availbe then you can provide \
                                         other information and book your Appointment.")
                messages.success(request,"Slot is available. you can make appointment.")
                return render(request, "users/makeAppointment.html", context={
                                            "do_appointment": True,
                                            "user_info":user_info,
                                            "appointmentForm": appointment_form,
                                            "symptomForm": symptoms_From,
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
    
    # if request.method == "POST":

    return redirect('doctors')

