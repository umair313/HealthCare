
from django import forms
from .models import Appointment, Symptom, TestResult, Medicine, Disease



class AppointmentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"id":"datepicker"}))

    class Meta:
        model = Appointment
        fields = ["date","time"]

class SymtomsForm(forms.ModelForm):
    symptom = forms.Textarea()
    class Meta:
        model = Symptom
        fields = ["symptom"]



class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ["blood_pressure","blood_sugar","bmi","hemoglobin","platelets"]



class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["medicine"]

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ["disease"]