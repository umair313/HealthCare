from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.fields import ChoiceField
from django.utils.regex_helper import Choice
from .models import DoctorInfo,UsersInfo



class userRegistrationForm(UserCreationForm):

    email = forms.EmailField(label=False)
    
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password1","password2"]


role_choices = [("","--------"),("patient","Patient"),("doctor","Doctor")]

class UserInfoForm(forms.ModelForm):

    role = forms.ChoiceField(required = True, choices = role_choices,
    widget=forms.Select(attrs={"onchange":"change()"}))
    # age = forms.IntegerField(label=False,required=True)
    age = forms.IntegerField()
    city = forms.CharField(max_length=20)
    country = forms.CharField(max_length=20)
    mobile_number = forms.IntegerField()

    class Meta:
        model = UsersInfo
        fields = ("role","age","city","country","mobile_number","profile_picture")


class DoctorInfoForm(forms.ModelForm):

    qualification = forms.CharField(label=False,required=False,
                widget=forms.TextInput(attrs={"class":"form-field"}))

    expertise = forms.CharField(label=False,required=False,
                widget=forms.TextInput(attrs={"class":"form-field"}))
    
    class Meta:
        model = DoctorInfo
        fields = ["qualification","expertise"]

