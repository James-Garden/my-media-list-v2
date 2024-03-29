from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from .models import User


class SignUpForm(UserCreationForm):
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

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            w, h = get_image_dimensions(avatar)
            if avatar.size > 2*1024*1024:
                raise ValidationError("Image file too large, maximum size 2MB!")
            elif w > 225 or h > 350:
                raise ValidationError("Image dimensions too large, maximum size 225x350 (WxH)!")
            return avatar
        else:
            raise ValidationError("Unable to read uploaded image, please check format and try again.")


class UsernameChangeForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
    }))

    class Meta:
        model = User
        fields = ['username']


class EmailChangeForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={
       'class': 'form-control',
       'type': 'email'
    }))

    class Meta:
        model = User
        fields = ['email']
