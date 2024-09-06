from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                f'Your account has been created! You are now able to log in'
            )
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(
        request,
        'users/register.html',
        {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'You are now logged in as {username}')
            return redirect('car_list')
    else:
        form = AuthenticationForm()
    return render(
        request,
        'users/login.html',
        {'form': form})
