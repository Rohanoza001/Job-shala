from django.shortcuts import render

# Create your views here.

def homepage(request):
    return render(request, 'core/homepage.html')

def login(request):
    return render(request, 'core/login.html')
