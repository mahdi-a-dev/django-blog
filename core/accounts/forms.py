from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

user = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = user
        fields = ["email"]