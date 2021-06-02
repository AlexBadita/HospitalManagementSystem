from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Account, Patient, Doctor, Appointment


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        account = super().save(commit=False)
        account.is_patient = True
        account.save()
        patient = Patient.objects.create(account=account)
        patient.phone_number = self.cleaned_data.get('phone_number')
        patient.save()
        return account


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=60)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email')


class UpdatePatientForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = Account
        fields = ('phone_number',)


class AddDoctorForm(UserCreationForm):
    email = forms.EmailField(max_length=60)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    specialization = forms.CharField(max_length=50)
    opening_hour = forms.TimeField()
    closing_hour = forms.TimeField()

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'specialization', 'opening_hour', 'closing_hour', 'password1',
                  'password2')

    @transaction.atomic
    def save(self):
        account = super().save(commit=False)
        account.is_doctor = True
        account.save()
        doctor = Doctor.objects.create(account=account)
        doctor.specialization = self.cleaned_data.get('specialization')
        doctor.opening_hour = self.cleaned_data.get('opening_hour')
        doctor.closing_hour = self.cleaned_data.get('closing_hour')
        doctor.save()
        return account


class MakeAppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(),
                                    empty_label="Doctor Name and Specialization", to_field_name="account_id")
    date = forms.DateField()
    time = forms.TimeField()

    class Meta:
        model = Appointment
        fields = ('doctor', 'date', 'time')