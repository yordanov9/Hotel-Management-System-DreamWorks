from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.
from django.core.exceptions import ValidationError

from hotel.models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', False)
        if not email:
            raise ValidationError('Email is required.')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

