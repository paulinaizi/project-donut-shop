from django.shortcuts import render
from .models import Donut

def home(request):
    donuts = Donut.objects.filter(is_custom_base=False)
    return render(request, 'home.html', {'donuts':donuts})

def about(request):
    return render(request, 'about.html', {})