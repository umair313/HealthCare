from django.contrib import auth
from django.shortcuts import render, HttpResponse
from .forms import userRegistrationForm ,UserInfoForm,DoctorInfoForm
from .models import UsersInfo, DoctorInfo
from django.contrib.auth.decorators import login_required
# for uer login
# from django.contrib.auth import authenticate, logout, login as auth_login


# Create your views here.
def Home(request):
    user = request.user
    if user.is_authenticated:
        user_info = UsersInfo.objects.filter(user=user).first()
        if user_info:
            if user_info.role != "doctor":
                return render(request,"users/patient_dashboard.html",context={"user_info":user_info})
            else:
                pass
        return HttpResponse(f"already login")
    return render(request,"users/index.html")

# def login(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(username=username,password=password)
#         if user:
#             if user.is_active:
#                 auth_login(request=request,user=user)
#                 user_info = UsersInfo.objects.filter(user=user).first()
#                 if user_info:
#                     if user_info.role == "doctor":
#                         doctor_info = DoctorInfo.objects.filter(user_info=user_info).first()
#                         return HttpResponse(f"role : {doctor_info.user_info.role}")
                    
#                     return render(request,"users/patient_dashboard.html", context={"user_info":user_info})
#                 return HttpResponse("some kind of error")
#             else:
#                 return HttpResponse("user is not active!")
#         else:
#             return HttpResponse("invalid username of password")
#     return render(request,"users/login.html")

def register(request):
    if request.method == "POST":
        registration_form = userRegistrationForm(request.POST)
        doctor_info_form = DoctorInfoForm(request.POST)
        user_info_form = UserInfoForm(request.POST, request.FILES or None)
        if registration_form.is_valid() and user_info_form.is_valid():
            user = registration_form.save()
            user.save()
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.save()
            role = user_info_form.cleaned_data["role"]
            img = user_info_form.cleaned_data["profile_picture"]
            print(role)
            print(img)
            if role == "doctor" and doctor_info_form.is_valid():
                doctor_info = doctor_info_form.save(commit=False)
                doctor_info.user_info = user_info
                doctor_info.save()
            return HttpResponse(f"Success")
        else:
            context = {
                        "formRegistration": registration_form,
                        "formUserInfo": user_info_form,
                        "formDoctorInfo": doctor_info_form
                    }
            print(registration_form.errors)
            print(user_info_form.errors)
            print(doctor_info_form.errors)
            return render(request, "users/register.html" , context=context)
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
    user = request.user
    user_info = UsersInfo.objects.filter(user=user).first()
    context = {"user_info": user_info}
    if user_info.role == "doctor":
        doctor_info = DoctorInfo.objects.filter(user_info=user_info).first()
        context["doctorr_info"] = doctor_info
    return render(request,"users/profile.html",context=context)
