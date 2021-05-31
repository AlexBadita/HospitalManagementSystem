from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import RegistrationForm, UpdateUserForm, UpdatePatientForm, AddDoctorForm
from django.contrib import messages
from .models import *
import logging

logging.basicConfig(filename='./logs/logs.log', filemode='w', level=logging.INFO)


def register(request):
    logging.info('Test info log from register')
    logging.error('Test error log from register')
    logging.warning('Test warning log from register')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect("hospital-home")
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'registration_form': form})


@login_required
def profile(request):
    logging.info('Test info log from profile')
    logging.error('Test error log from profile')
    logging.warning('Test warning log from profile')

    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdatePatientForm(request.POST, instance=request.user.patient)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdatePatientForm(instance=request.user.patient)
    context = {
        'user_form': u_form,
        'patient_form': p_form
    }
    return render(request, 'accounts/profile.html', context)


def make_appointments(request):
    logging.info('Test info log from make_appointments')
    logging.error('Test error log from make_appointments')
    logging.warning('Test warning log from make_appointments')

    doctors = Doctor.objects.all()
    context = {
        'doctors': doctors
    }
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        try:
            Appointment.objects.create(doctor=Doctor.objects.get(account_id=doctor_id),
                                       patient=Account.objects.get(id=request.user.id).patient,
                                       date=date, time=time, status=True, diagnostic="", treatment="")
            error = "no"
        except Exception as e:
            error = "yes"
        context['error'] = error
        return render(request, 'accounts/patient_make_appointments.html', context)
    return render(request, 'accounts/patient_make_appointments.html', context)


def view_appointments(request):
    logging.info('Test info log from view_appointments')
    logging.error('Test error log from view_appointments')
    logging.warning('Test warning log from view_appointments')

    if request.user.is_patient:
        upcoming_appointments = Appointment.objects.filter(patient=Account.objects.get(id=request.user.id).patient,
                                                           date__gte=timezone.now(), status=True).order_by('date')
        previous_appointments = Appointment.objects.filter(patient=Account.objects.get(id=request.user.id).patient,
                                                           date__lt=timezone.now()).order_by('-date') | \
                                Appointment.objects.filter(patient=Account.objects.get(id=request.user.id).patient,
                                                           status=False).order_by('-date')
        context = {
            'upcoming_appointments': upcoming_appointments,
            'previous_appointments': previous_appointments
        }
        return render(request, 'accounts/patient_view_appointments.html', context)
    elif request.user.is_doctor:
        if request.method == 'POST':
            diagnostic = request.POST.get('diagnostic')
            treatment = request.POST.get('treatment')
            id_appointment = request.POST.get('id_appointment')
            Appointment.objects.filter(id=id_appointment).update(diagnostic=diagnostic, treatment=treatment,
                                                                 status=False)
        upcoming_appointments = Appointment.objects.filter(doctor=Account.objects.get(id=request.user.id).doctor,
                                                           date__gte=timezone.now(), status=True).order_by('date')
        previous_appointments = Appointment.objects.filter(doctor=Account.objects.get(id=request.user.id).doctor,
                                                           date__lt=timezone.now()).order_by('-date') | \
                                Appointment.objects.filter(doctor=Account.objects.get(id=request.user.id).doctor,
                                                           status=False).order_by('-date')
        context = {
            'upcoming_appointments': upcoming_appointments,
            'previous_appointments': previous_appointments
        }
        return render(request, 'accounts/doctor_view_appointments.html', context)
    elif request.user.is_superuser:
        appointments = Appointment.objects.all()
        return render(request, 'accounts/admin_view_appointments.html', {'appointments': appointments})


def delete_appointment(request, aid):
    logging.info('Test info log from delete_appointment')
    logging.error('Test error log from delete_appointment')
    logging.warning('Test warning log from delete_appointment')

    appointment = Appointment.objects.get(id=aid)
    appointment.delete()
    messages.success(request, f'Appointment successfully deleted!')
    return redirect('view_appointments')


def add_doctor(request):
    logging.info('Test info log from add_doctor')
    logging.error('Test error log from add_doctor')
    logging.warning('Test warning log from add_doctor')

    if request.method == 'POST':
        form = AddDoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Doctor account successfully created!')
            return redirect('add_doctor')
    else:
        form = AddDoctorForm()
    return render(request, 'accounts/admin_add_doctor.html', {'add_doctor_from': form})


def view_doctors(request):
    logging.info('Test info log from view_doctors')
    logging.error('Test error log from view_doctors')
    logging.warning('Test warning log from view_doctors')

    doctors = Doctor.objects.all()
    return render(request, 'accounts/admin_view_doctors.html', {'doctors': doctors})


def delete_doctor(request, aid):
    logging.info('Test info log from delete_doctor')
    logging.error('Test error log from delete_doctor')
    logging.warning('Test warning log from delete_doctor')

    doctor = Doctor.objects.get(account_id=aid)
    appointments = Appointment.objects.filter(doctor_id=aid)
    user = Account.objects.get(id=aid)
    appointments.delete()
    doctor.delete()
    user.delete()
    messages.success(request, f'Doctor successfully deleted!')
    return redirect('view_doctors')


def view_patients(request):
    logging.info('Test info log from view_patients')
    logging.error('Test error log from view_patients')
    logging.warning('Test warning log from view_patients')

    patients = Patient.objects.all()
    return render(request, 'accounts/admin_view_patients.html', {'patients': patients})


def delete_patient(request, aid):
    logging.info('Test info log from delete_patient')
    logging.error('Test error log from delete_patient')
    logging.warning('Test warning log from delete_patient')

    patient = Patient.objects.get(account_id=aid)
    appointments = Appointment.objects.filter(patient_id=aid)
    user = Account.objects.get(id=aid)
    appointments.delete()
    patient.delete()
    user.delete()
    messages.success(request, f'Patient successfully deleted!')
    return redirect('view_patients')