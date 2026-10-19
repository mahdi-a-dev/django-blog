from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import Profile

user = get_user_model()

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=250,
        widget=forms.TextInput,
        required=False
    )
    last_name = forms.CharField(
        max_length=250,
        widget=forms.TextInput,
        required=False
    )
    description = forms.CharField(
        max_length=500,
        widget=forms.Textarea,
        required=False
    )
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "image", "description"]

class RegisterForm(UserCreationForm):
    class Meta:
        model = user
        fields = ["email"]

class LoginForm(AuthenticationForm):
    # Even though we have changed the unique user identifier to the email address,
    # The field name here must still be 'username',
    # so that user identification is performed using the email, but under the field name 'username',
    # Its because 'AuthenticationForm' uses the 'username.'
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput
    )
    
    error_messages = {
        "invalid_login": "Email or password is invalid."
    }
