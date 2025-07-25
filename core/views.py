from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employer.models import Job

# Create your views here.

def homepage(request):
    # Get recent active jobs
    recent_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:6]
    
    context = {
        'recent_jobs': recent_jobs,
    }
    return render(request, 'core/homepage.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'job_seeker')
        
        if email and password:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                
                # Redirect based on user type and profile existence
                if user_type == 'employer':
                    # Check if user has an employer profile
                    try:
                        from employer.models import Employer
                        employer = Employer.objects.get(user=user)
                        # Check if employer is approved
                        if not employer.is_approved:
                            messages.warning(request, 'Your employer account is pending approval. You will be notified once approved.')
                        return redirect('employer_dashboard')
                    except Employer.DoesNotExist:
                        messages.error(request, 'This account does not have an employer profile. Please sign up as an employer.')
                        return redirect('employer_signup')
                else:
                    # Check if user has a job seeker profile
                    try:
                        from job.models import JobSeeker
                        job_seeker = JobSeeker.objects.get(user=user)
                        return redirect('job_listing')
                    except JobSeeker.DoesNotExist:
                        messages.error(request, 'This account does not have a job seeker profile. Please sign up as a job seeker.')
                        return redirect('job_signup')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please provide both email and password.')
    
    return render(request, 'core/login.html')

@login_required
def logout(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('homepage')
