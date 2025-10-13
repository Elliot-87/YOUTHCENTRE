from django import forms
from django.contrib.auth.models import User
from .models import EmployerProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=(("jobseeker","Jobseeker"), ("employer","Employer")), initial="jobseeker")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ["company_name", "website"]
