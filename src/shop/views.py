from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Donut, Coating, Sprinkle, TopCoating
from .forms import LoginForm, RegisterForm


def home(request):
    base_donut = Donut.objects.get(is_custom_base=True)
    donuts = Donut.objects.filter(is_custom_base=False)
    coatings = Coating.objects.all()
    sprinkles = Sprinkle.objects.all()
    top_coatings = TopCoating.objects.all()
    return render(request, 'home.html', {'base_donut':base_donut, 'donuts':donuts, 'coatings':coatings, 'sprinkles':sprinkles, 'top_coatings':top_coatings})


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
                return redirect(request.GET.get('next', 'home'))
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