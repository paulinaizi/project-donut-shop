from django.shortcuts import render, redirect
from .models import Donut
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm, RegisterForm

def home(request):
    donuts = Donut.objects.filter(is_custom_base=False)
    return render(request, 'home.html', {'donuts':donuts})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Niepoprawne dane logowania.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})