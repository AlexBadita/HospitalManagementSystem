from django.shortcuts import render


def home(request):
    return render(request, 'hospital_app/home.html')


def contact(request):
    return render(request, 'hospital_app/contact.html')
