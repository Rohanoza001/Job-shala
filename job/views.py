from django.shortcuts import render

# Create your views here.

def signup(request):
    """Job seeker signup page with multi-step form"""
    return render(request, 'job/signup.html')
