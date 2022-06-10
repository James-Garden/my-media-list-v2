from django import forms
from django.contrib.auth.forms import UserCreationForm
from utils.validators import validate_age, validate_username
from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255)
    username = forms.CharField(max_length=24, validators=[validate_username])
    birth_date = forms.DateField(help_text='Required. Format: DD/MM/YYYY', validators=[validate_age])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'birth_date')


class EditProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.widget_type == 'select':
                visible.field.widget.attrs['class'] = 'form-select'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['birth_date', 'birth_date_privacy', 'gender', 'avatar', 'location', 'bio', 'links']
