from django.shortcuts import render, redirect
from .models import Donut
from django.contrib.auth import login, logout, authenticate
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nazwa użytkownika',
        }),
        error_messages={
            'required': 'Nazwa użytkownika nie może być pusta.'
        },
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hasło',
        }),
        error_messages={
            'required': 'Hasło nie może być puste.',
        },
    )

class RegisterForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Imię',
        }),
        error_messages={
            'required': 'Proszę wprowadzić nazwę użytkownika.'
        },
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nazwa użytkownika',
        }),
        error_messages={
            'required': 'Proszę wprowadzić nazwę użytkownika.'
        },
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Hasło',
        }),
        error_messages={
            'required': 'Hasło nie może być puste.',
        },
    )

def home(request):
    donuts = Donut.objects.filter(is_custom_base=False)
    return render(request, 'home.html', {'donuts':donuts})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
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