from django import forms
from .models import *


class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['name', 'email_address', 'password', 'dateOfBirth']


class LogInForm(forms.Form):
    email_address = forms.EmailField()
    password = forms.CharField(max_length=4096)
