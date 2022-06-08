from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from utils.validators import validate_age, validate_username
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255)
    username = forms.CharField(max_length=24, validators=[validate_username])
    birth_date = forms.DateField(help_text='Required. Format: DD/MM/YYYY', validators=[validate_age])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'birth_date')
