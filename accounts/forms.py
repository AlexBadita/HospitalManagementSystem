from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient
from django.db import transaction
from django.core.exceptions import ValidationError


class PatientRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    cnp = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'cnp', 'password1', 'password2']

    def clean(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists!')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = f'{user.first_name} {user.last_name}'
        user.save()
        patient = Patient.objects.create(user=user)
        patient.cnp = int(self.cleaned_data.get('cnp'))
        patient.save()
        return user