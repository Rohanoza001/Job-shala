from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from .models import JobSeeker, JobApplication
from employer.models import Job, Employer
from .forms import JobApplicationForm
import json

# Create your views here.

def signup(request):
    """Job seeker signup page with multi-step form"""
    # Redirect if user is already logged in
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('job_listing')
    
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            password = request.POST.get('password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()
            
            # Get additional form data
            address = request.POST.get('address', '').strip()
            city = request.POST.get('city', '').strip()
            state = request.POST.get('state', '').strip()
            country = request.POST.get('country', '').strip()
            pincode = request.POST.get('pincode', '').strip()
            description = request.POST.get('description', '').strip()
            
            # Basic validation
            if not first_name or not last_name or not email or not password or not confirm_password:
                missing_fields = []
                if not first_name:
                    missing_fields.append('First Name')
                if not last_name:
                    missing_fields.append('Last Name')
                if not email:
                    missing_fields.append('Email')
                if not password:
                    missing_fields.append('Password')
                if not confirm_password:
                    missing_fields.append('Confirm Password')
                
                messages.error(request, f'Please fill in all required fields: {", ".join(missing_fields)}')
                return render(request, 'job/signup.html')
            
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'job/signup.html')
            
            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return render(request, 'job/signup.html')
            
            # Email validation
            if '@' not in email or '.' not in email:
                messages.error(request, 'Please enter a valid email address.')
                return render(request, 'job/signup.html')
            
            # Phone validation
            if not phone:
                phone = "Not provided"
            
            # Address validation - make these fields optional for now
            if not address:
                address = "Not provided"
            if not city:
                city = "Not provided"
            if not state:
                state = "Not provided"
            if not country:
                country = "Not provided"
            if not pincode:
                pincode = "Not provided"
            
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'A user with this email already exists.')
                return render(request, 'job/signup.html')
            
            if User.objects.filter(username=email).exists():
                messages.error(request, 'A user with this email already exists.')
                return render(request, 'job/signup.html')
            
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Handle file uploads
            profile_picture = request.FILES.get('profile_image')
            resume = request.FILES.get('resume')
            
            # Validate file uploads
            if profile_picture and profile_picture.size > 5 * 1024 * 1024:  # 5MB limit
                messages.error(request, 'Profile picture file size must be less than 5MB.')
                return render(request, 'job/signup.html')
            
            if resume and resume.size > 5 * 1024 * 1024:  # 5MB limit
                messages.error(request, 'Resume file size must be less than 5MB.')
                return render(request, 'job/signup.html')
            
            if resume:
                allowed_extensions = ['.pdf', '.doc', '.docx']
                file_extension = resume.name.lower()
                if not any(file_extension.endswith(ext) for ext in allowed_extensions):
                    messages.error(request, 'Please upload a PDF, DOC, or DOCX file for resume.')
                    return render(request, 'job/signup.html')
            
            # Create JobSeeker profile
            job_seeker = JobSeeker.objects.create(
                user=user,
                phone=phone,
                address=address,
                city=city,
                state=state,
                country=country,
                pincode=pincode,
                description=description,
                profile_picture=profile_picture,
                resume=resume
            )
            
            # Log the user in
            auth_login(request, user)
            
            messages.success(request, f'Welcome {user.get_full_name()}! Your account has been created successfully. You can now browse and apply for jobs.')
            return redirect('job_listing')
            
        except Exception as e:
            messages.error(request, 'An error occurred while creating your account. Please try again.')
            return render(request, 'job/signup.html')
    
    return render(request, 'job/signup.html')

def job_listing(request):
    """Display all available jobs with filtering and search"""
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(company_name__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(skills_required__icontains=search_query)
        )
    
    # Filter by job type
    job_type = request.GET.get('job_type', '')
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    # Filter by experience level
    experience = request.GET.get('experience', '')
    if experience:
        jobs = jobs.filter(experience_level=experience)
    
    # Filter by location
    location = request.GET.get('location', '')
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    # Pagination
    paginator = Paginator(jobs, 10)  # 10 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get user's applications to show applied status
    user_applications = {}
    has_job_seeker_profile = False
    if request.user.is_authenticated:
        try:
            job_seeker = JobSeeker.objects.get(user=request.user)
            applications = JobApplication.objects.filter(job_seeker=job_seeker)
            user_applications = {app.job.id: app.status for app in applications}
            has_job_seeker_profile = True
        except JobSeeker.DoesNotExist:
            # Check if user has employer profile
            try:
                employer = Employer.objects.get(user=request.user)
                # User is an employer, they can view jobs but not apply
                pass
            except Employer.DoesNotExist:
                # User has no profile, show message to complete profile
                messages.warning(request, 'Please complete your profile to apply for jobs. You can sign up as a job seeker or employer.')
    
    context = {
        'jobs': page_obj,
        'search_query': search_query,
        'job_type': job_type,
        'experience': experience,
        'location': location,
        'user_applications': user_applications,
        'job_types': Job.JOB_TYPE_CHOICES,
        'experience_levels': Job.EXPERIENCE_CHOICES,
        'has_job_seeker_profile': has_job_seeker_profile,
    }
    
    return render(request, 'job/job_listing.html', context)

def job_detail(request, job_id):
    """Display detailed job information and application form"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Check if user has already applied
    has_applied = False
    application = None
    has_job_seeker_profile = False
    if request.user.is_authenticated:
        try:
            job_seeker = JobSeeker.objects.get(user=request.user)
            application = JobApplication.objects.filter(job=job, job_seeker=job_seeker).first()
            has_applied = application is not None
            has_job_seeker_profile = True
        except JobSeeker.DoesNotExist:
            # Check if user has employer profile
            try:
                employer = Employer.objects.get(user=request.user)
                # User is an employer, they can view jobs but not apply
                pass
            except Employer.DoesNotExist:
                # User has no profile
                pass
    
    # Increment view count
    job.views_count += 1
    job.save()
    
    if request.method == 'POST' and request.user.is_authenticated and not has_applied:
        if has_job_seeker_profile:
            try:
                job_seeker = JobSeeker.objects.get(user=request.user)
                form = JobApplicationForm(request.POST, request.FILES)
                if form.is_valid():
                    application = form.save(commit=False)
                    application.job = job
                    application.job_seeker = job_seeker
                    application.save()
                    
                    # Update job application count
                    job.applications_count += 1
                    job.save()
                    
                    messages.success(request, 'Your application has been submitted successfully!')
                    return redirect('job_detail', job_id=job.id)
            except JobSeeker.DoesNotExist:
                messages.error(request, 'Please complete your profile first.')
                return redirect('job_signup')
        else:
            messages.warning(request, 'Please complete your job seeker profile to apply for jobs.')
            return redirect('job_signup')
    else:
        form = JobApplicationForm()
    
    context = {
        'job': job,
        'form': form,
        'has_applied': has_applied,
        'application': application,
        'has_job_seeker_profile': has_job_seeker_profile,
    }
    
    return render(request, 'job/job_detail.html', context)

@login_required
def my_applications(request):
    """Display user's job applications"""
    try:
        job_seeker = JobSeeker.objects.get(user=request.user)
        applications = JobApplication.objects.filter(job_seeker=job_seeker).select_related('job')
        
        # Filter by status
        status_filter = request.GET.get('status', '')
        if status_filter:
            applications = applications.filter(status=status_filter)
        
        # Pagination
        paginator = Paginator(applications, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'applications': page_obj,
            'status_filter': status_filter,
            'status_choices': JobApplication.STATUS_CHOICES,
        }
        
        return render(request, 'job/my_applications.html', context)
    except JobSeeker.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('job_signup')

@login_required
def application_detail(request, application_id):
    """Display detailed application information"""
    application = get_object_or_404(JobApplication, id=application_id)
    
    # Ensure user can only view their own applications
    if application.job_seeker.user != request.user:
        messages.error(request, 'You can only view your own applications.')
        return redirect('my_applications')
    
    context = {
        'application': application,
    }
    
    return render(request, 'job/application_detail.html', context)

@login_required
def withdraw_application(request, application_id):
    """Allow users to withdraw their application"""
    if request.method == 'POST':
        application = get_object_or_404(JobApplication, id=application_id)
        
        # Ensure user can only withdraw their own applications
        if application.job_seeker.user != request.user:
            return JsonResponse({'success': False, 'message': 'Unauthorized'})
        
        if application.status == 'applied':
            application.status = 'withdrawn'
            application.save()
            return JsonResponse({'success': True, 'message': 'Application withdrawn successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Cannot withdraw application in current status'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def job_seeker_dashboard(request):
    """Job seeker dashboard with overview and quick actions"""
    try:
        job_seeker = JobSeeker.objects.get(user=request.user)
        
        # Get recent applications
        recent_applications = JobApplication.objects.filter(
            job_seeker=job_seeker
        ).select_related('job').order_by('-applied_at')[:5]
        
        # Get application statistics
        total_applications = JobApplication.objects.filter(job_seeker=job_seeker).count()
        pending_applications = JobApplication.objects.filter(
            job_seeker=job_seeker, 
            status__in=['applied', 'reviewing']
        ).count()
        shortlisted_applications = JobApplication.objects.filter(
            job_seeker=job_seeker, 
            status='shortlisted'
        ).count()
        
        # Get recommended jobs based on skills (simple implementation)
        recommended_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:5]
        
        context = {
            'job_seeker': job_seeker,
            'recent_applications': recent_applications,
            'total_applications': total_applications,
            'pending_applications': pending_applications,
            'shortlisted_applications': shortlisted_applications,
            'recommended_jobs': recommended_jobs,
        }
        
        return render(request, 'job/dashboard.html', context)
    except JobSeeker.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('job_signup')
