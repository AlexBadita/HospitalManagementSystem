from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PatientRegisterForm


def register(request):
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            #messages.success(request, f'Account created for {first_name} {last_name}!')
            messages.success(request, f'Your account has been created!')
            return redirect('login')
    else:
        form = PatientRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')