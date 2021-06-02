from django.shortcuts import render


def home(request):
    print(request.user)
    return render(request, 'hospital_app/home.html')
