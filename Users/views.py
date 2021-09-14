from django.shortcuts import render, HttpResponse
from .forms import userRegistrationForm ,UserInfoForm,DoctorInfoForm
# Create your views here.
def Home(request):
    return render(request,"users/index.html")

def login(request):
    return render(request,"users/login.html")

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