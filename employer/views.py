from django.shortcuts import render

# Create your views here.

def employer_signup(request):
    return render(request, 'employer/signup.html')
