from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cnp = models.BigIntegerField(unique=True)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()
