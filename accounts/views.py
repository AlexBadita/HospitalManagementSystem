from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PatientRegisterForm


def register(request):
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            messages.success(request, f'Account created for {first_name} {last_name}!')
            return redirect('hospital-home')
    else:
        form = PatientRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
