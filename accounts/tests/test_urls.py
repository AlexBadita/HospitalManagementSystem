from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import *
from hospital_app.views import *


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('hospital-home')
        self.assertEqual(resolve(url).func, home)

    def test_register_url_is_resolved(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

    def test_profile_url_is_resolved(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, profile)

    def test_make_appointments_url_is_resolved(self):
        url = reverse('make_appointments')
        self.assertEqual(resolve(url).func, make_appointments)

    def test_view_appointments_url_is_resolved(self):
        url = reverse('view_appointments')
        self.assertEqual(resolve(url).func, view_appointments)

    def test_add_doctor_url_is_resolved(self):
        url = reverse('add_doctor')
        self.assertEqual(resolve(url).func, add_doctor)

    def test_view_doctors_url_is_resolved(self):
        url = reverse('view_doctors')
        self.assertEqual(resolve(url).func, view_doctors)

    def test_view_patients_url_is_resolved(self):
        url = reverse('view_patients')
        self.assertEqual(resolve(url).func, view_patients)