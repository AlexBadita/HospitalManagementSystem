from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

