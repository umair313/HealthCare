from django.contrib import messages
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import userRegistrationForm ,UserInfoForm,DoctorInfoForm
from .models import UsersInfo, DoctorInfo
from Appointments.models import CurrentAppointments





info_message = "Please Select Data and time and check for availale slot.\
If the slot is availbe then you can provide other information and book your Appointment."



# Create your views here.


def Home(request):
    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            return HttpResponseRedirect(reverse("admin:index"))
        if user.usersinfo.role != "doctor":
            return render(request,"users/dashboard.html")
        return render(request,"users/dashboard.html" ,context={"chart":True})
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
def searchpage(request):
    return render(request,"users/searchpage.html")

@login_required
def search(request):
    if request.method == "POST":
        query = request.POST["search"]
        query = query.lower()
        doctors = []
        
        doctor_query = DoctorInfo.objects.all()
        for doctor in doctor_query:
            if query in doctor.qualification.lower() or query in doctor.expertise.lower():
                doctors.append(doctor)
        if doctors:
                return render(request, "users/doctors.html",context={"doctors":doctors})
        messages.error(request,"didnot found related doctor")
    return render(request,"users/searchpage.html")

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
    doctors = DoctorInfo.objects.all()
    return render(request, "users/doctors.html",context={"doctors":doctors})


@login_required
def doctor_profile(request,doctor_id):
    user = User.objects.filter(id=doctor_id).first()
    user_info= UsersInfo.objects.filter(user = request.user).first()
    if user:
        doctor_user_info = UsersInfo.objects.filter(user=user).first()
        doctor_info = DoctorInfo.objects.filter(user_info=doctor_user_info).first()
        
    return render(request, "users/doctor_profile.html",context={"doctor_profile":True,"doctor_info":doctor_info,"user_info":user_info})





@login_required
def patients(request):
    user = request.user
    patients = []
    if user.usersinfo.role == "doctor":
        appointments = user.appointment_doctor.all()
        for app in appointments:
            patients.append(app.patient)
        patients= list(set(patients))
        return render(request,"users/patients.html",context={"patients":patients})



@login_required
def patient_profile(request,patient_id):
    patient = User.objects.filter(id=patient_id).first()
    return render(request, "users/patient_profile.html",context={"patient":patient})




