from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
