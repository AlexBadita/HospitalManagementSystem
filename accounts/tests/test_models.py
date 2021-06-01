from django.test import TestCase
from accounts.models import *


class TestModels(TestCase):

    def test_account_model(self):
        account = Account()
        account.email = 'testaccount@gmail.com'
        account.first_name = 'test'
        account.last_name = 'account'
        account.save()

        record = Account.objects.get(pk=1)
        self.assertEqual(record, account)

    def test_patient_model(self):
        patient = Patient()
        patient.account = Account.objects.create(email='testaccount@gmail.com', first_name='test', last_name='account')
        patient.phone_number = '014281021'
        patient.save()

        record = Patient.objects.get(account_id=patient.account.id)
        self.assertEqual(record, patient)

    def test_doctor_model(self):
        doctor = Doctor()
        doctor.account = Account.objects.create(email='testaccount@gmail.com', first_name='test', last_name='account')
        doctor.specialization = 'ORL'
        doctor.save()

        record = Doctor.objects.get(account_id=doctor.account.id)
        self.assertEqual(record, doctor)

    def test_appointment_model(self):
        appointment = Appointment()
        appointment.save()

        record = Appointment.objects.get(pk=1)
        self.assertEqual(record, appointment)