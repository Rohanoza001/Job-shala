from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Employer, Job, Message
from job.models import JobSeeker, JobApplication
from .forms import JobPostForm, ApplicationStatusForm, MessageForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def employer_signup(request):
    """Employer signup page with multi-step form"""
    # Check if user is already logged in
    if request.user.is_authenticated:
        # Check if they already have an employer profile
        try:
            employer = Employer.objects.get(user=request.user)
            messages.info(request, 'You are already logged in.')
            return redirect('employer_dashboard')
        except Employer.DoesNotExist:
            # User is logged in but doesn't have an employer profile
            # Allow them to complete their profile
            pass
    
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()
            
            # Company information
            company_name = request.POST.get('company_name', '').strip()
            designation = request.POST.get('designation', '').strip()
            department = request.POST.get('department', '').strip()
            phone = request.POST.get('phone', '').strip()
            company_website = request.POST.get('company_website', '').strip()
            company_email = request.POST.get('company_email', '').strip()
            company_phone = request.POST.get('company_phone', '').strip()
            
            # Address information
            address = request.POST.get('address', '').strip()
            city = request.POST.get('city', '').strip()
            state = request.POST.get('state', '').strip()
            country = request.POST.get('country', '').strip()
            pincode = request.POST.get('pincode', '').strip()
            
            # GST information
            gst_number = request.POST.get('gst_number', '').strip()
            
            # Handle file uploads
            company_logo = request.FILES.get('company_logo')
            
            # Check if user is already logged in
            if request.user.is_authenticated:
                # User is logged in but needs to complete employer profile
                user = request.user
                
                # Update user information if provided
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name
                user.save()
                
                # Create Employer profile for existing user
                employer = Employer.objects.create(
                    user=user,
                    company_name=company_name or "Not provided",
                    designation=designation or "Not provided",
                    department=department or "Not provided",
                    phone=phone or "Not provided",
                    company_website=company_website or "",
                    company_email=company_email or user.email,
                    company_phone=company_phone or phone or "Not provided",
                    address=address or "Not provided",
                    city=city or "Not provided",
                    state=state or "Not provided",
                    country=country or "Not provided",
                    pincode=pincode or "Not provided",
                    gst_number=gst_number or "",
                    company_logo=company_logo,
                    is_approved=False  # Requires admin approval
                )
                
                messages.success(request, f'Welcome to Job Shala, {user.get_full_name()}! Your employer account has been created and is pending approval.')
                return redirect('employer_dashboard')
            else:
                # New user registration
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
                    return render(request, 'employer/signup.html')
                
                if password != confirm_password:
                    messages.error(request, 'Passwords do not match.')
                    return render(request, 'employer/signup.html')
                
                if len(password) < 8:
                    messages.error(request, 'Password must be at least 8 characters long.')
                    return render(request, 'employer/signup.html')
                
                # Email validation
                if '@' not in email or '.' not in email:
                    messages.error(request, 'Please enter a valid email address.')
                    return render(request, 'employer/signup.html')
                
                # Check if user already exists
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'A user with this email already exists.')
                    return render(request, 'employer/signup.html')
                
                if User.objects.filter(username=email).exists():
                    messages.error(request, 'A user with this email already exists.')
                    return render(request, 'employer/signup.html')
                
                # Create new user
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Create Employer profile
                employer = Employer.objects.create(
                    user=user,
                    company_name=company_name or "Not provided",
                    designation=designation or "Not provided",
                    department=department or "Not provided",
                    phone=phone or "Not provided",
                    company_website=company_website or "",
                    company_email=company_email or email,
                    company_phone=company_phone or phone or "Not provided",
                    address=address or "Not provided",
                    city=city or "Not provided",
                    state=state or "Not provided",
                country=country or "Not provided",
                pincode=pincode or "Not provided",
                gst_number=gst_number or "",
                company_logo=company_logo,
                is_approved=False  # Requires admin approval
            )
            
            # Log the user in
            auth_login(request, user)
            messages.success(request, f'Welcome to Job Shala, {user.get_full_name()}! Your employer account has been created and is pending approval.')
            return redirect('employer_dashboard')
            
        except Exception as e:
            messages.error(request, 'An error occurred while creating your account. Please try again.')
            return render(request, 'employer/signup.html')
    
    # Pass user information to template for pre-filling if user is logged in
    context = {}
    if request.user.is_authenticated:
        context['user'] = request.user
        context['is_existing_user'] = True
    
    return render(request, 'employer/signup.html', context)

@login_required
def employer_dashboard(request):
    """Employer dashboard with statistics and recent activity"""
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        messages.error(request, "Please complete your employer profile first.")
        return redirect('employer_signup')
    
    # Get statistics
    total_jobs = Job.objects.filter(employer=employer).count()
    active_jobs = Job.objects.filter(employer=employer, is_active=True).count()
    total_applications = JobApplication.objects.filter(job__employer=employer).count()
    recent_applications = JobApplication.objects.filter(
        job__employer=employer,
        applied_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    # Get recent applications
    recent_apps = JobApplication.objects.filter(
        job__employer=employer
    ).select_related('job', 'job_seeker__user').order_by('-applied_at')[:5]
    
    # Get recent jobs
    recent_jobs = Job.objects.filter(employer=employer).order_by('-created_at')[:5]
    
    # Get unread messages count
    unread_messages = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()
    
    context = {
        'employer': employer,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'recent_applications': recent_applications,
        'recent_apps': recent_apps,
        'recent_jobs': recent_jobs,
        'unread_messages': unread_messages,
    }
    return render(request, 'employer/dashboard.html', context)

@login_required
def post_job(request):
    """Post a new job"""
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        messages.error(request, "Please complete your employer profile first.")
        return redirect('employer_signup')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.company_name = employer.company_name
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('employer_jobs')
    else:
        form = JobPostForm()
    
    context = {
        'form': form,
        'employer': employer,
    }
    return render(request, 'employer/post_job.html', context)

@login_required
def employer_jobs(request):
    """View all jobs posted by the employer"""
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        messages.error(request, "Please complete your employer profile first.")
        return redirect('employer_signup')
    
    jobs = Job.objects.filter(employer=employer).order_by('-created_at')
    
    # Filtering
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        jobs = jobs.filter(is_active=True)
    elif status_filter == 'inactive':
        jobs = jobs.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'jobs': page_obj,
        'employer': employer,
        'status_filter': status_filter,
    }
    return render(request, 'employer/jobs.html', context)

@login_required
def edit_job(request, job_id):
    """Edit an existing job"""
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        messages.error(request, "Please complete your employer profile first.")
        return redirect('employer_signup')
    
    job = get_object_or_404(Job, id=job_id, employer=employer)
    
    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('employer_jobs')
    else:
        form = JobPostForm(instance=job)
    
    context = {
        'form': form,
        'job': job,
        'employer': employer,
    }
    return render(request, 'employer/post_job.html', context)

@login_required
def job_applications(request, job_id):
    """View applications for a specific job"""
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        messages.error(request, "Please complete your employer profile first.")
        return redirect('employer_signup')
    
    job = get_object_or_404(Job, id=job_id, employer=employer)
    applications = JobApplication.objects.filter(job=job).select_related('job_seeker__user')
    
    # Filtering
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(applications, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'job': job,
        'applications': page_obj,
        'employer': employer,
        'status_filter': status_filter,
    }
    return render(request, 'employer/job_applications.html', context)

@login_required
def application_detail(request, application_id):
    """View detailed information about a specific application"""
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        messages.error(request, "Please complete your employer profile first.")
        return redirect('employer_signup')
    
    application = get_object_or_404(JobApplication, id=application_id, job__employer=employer)
    
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            
            # Check if this is a final decision
            if application.is_final_decision(new_status):
                if application.decision_made:
                    messages.error(request, 'A final decision has already been made on this application. You cannot change it.')
                    return redirect('application_detail', application_id=application.id)
                else:
                    # Mark as decision made
                    application.decision_made = True
                    application.decision_date = timezone.now()
            
            form.save()
            application.save()  # Save the decision tracking fields
            
            status_display = dict(JobApplication.STATUS_CHOICES)[new_status]
            messages.success(request, f'Application status updated to "{status_display}" successfully!')
            return redirect('application_detail', application_id=application.id)
    else:
        form = ApplicationStatusForm(instance=application)
    
    context = {
        'application': application,
        'form': form,
        'employer': employer,
    }
    return render(request, 'employer/application_detail.html', context)

@login_required
def all_applications(request):
    """View all applications across all jobs"""
    # Check if user is an employer
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        # Check if user is a job seeker
        try:
            job_seeker = JobSeeker.objects.get(user=request.user)
            messages.error(request, "This page is for employers only. You are registered as a job seeker.")
            return redirect('job_seeker_dashboard')  # Redirect to job seeker dashboard
        except JobSeeker.DoesNotExist:
            # User has no profile - they need to complete employer signup
            messages.error(request, "Please complete your employer profile first.")
            return redirect('employer_signup')
    
    applications = JobApplication.objects.filter(
        job__employer=employer
    ).select_related('job', 'job_seeker__user')
    
    # Filtering
    status_filter = request.GET.get('status')
    job_filter = request.GET.get('job')
    
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    if job_filter:
        applications = applications.filter(job_id=job_filter)
    
    # Pagination
    paginator = Paginator(applications, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get jobs for filter dropdown
    jobs = Job.objects.filter(employer=employer).order_by('title')
    
    context = {
        'applications': page_obj,
        'employer': employer,
        'jobs': jobs,
        'status_filter': status_filter,
        'job_filter': job_filter,
    }
    return render(request, 'employer/all_applications.html', context)

@login_required
def employer_messages(request):
    """View all messages/conversations"""
    # Check if user is an employer
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        # Check if user is a job seeker
        try:
            job_seeker = JobSeeker.objects.get(user=request.user)
            messages.error(request, "This page is for employers only. You are registered as a job seeker.")
            return redirect('job_seeker_dashboard')  # Redirect to job seeker dashboard
        except JobSeeker.DoesNotExist:
            # User has no profile - they need to complete employer signup
            messages.error(request, "Please complete your employer profile first.")
            return redirect('employer_signup')
    
    # Get all messages for this user
    user_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender', 'receiver').order_by('-created_at')
    
    # Group by conversation partner
    conversations_dict = {}
    for message in user_messages:
        if message.sender == request.user:
            other_user = message.receiver
        else:
            other_user = message.sender
        
        if other_user.id not in conversations_dict:
            conversations_dict[other_user.id] = {
                'other_user': other_user,
                'latest_message': message,
                'unread_count': 0
            }
        else:
            # Update unread count
            if message.receiver == request.user and not message.is_read:
                conversations_dict[other_user.id]['unread_count'] += 1
    
    # Convert to list and sort by latest message
    conversation_list = list(conversations_dict.values())
    conversation_list.sort(key=lambda x: x['latest_message'].created_at, reverse=True)
    
    context = {
        'conversations': conversation_list,
        'employer': employer,
    }
    return render(request, 'employer/messages.html', context)

@login_required
def conversation_detail(request, user_id):
    """View conversation with a specific user"""
    # Check if user is an employer
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        # Check if user is a job seeker
        try:
            job_seeker = JobSeeker.objects.get(user=request.user)
            messages.error(request, "This page is for employers only. You are registered as a job seeker.")
            return redirect('job_seeker_dashboard')  # Redirect to job seeker dashboard
        except JobSeeker.DoesNotExist:
            # User has no profile - they need to complete employer signup
            messages.error(request, "Please complete your employer profile first.")
            return redirect('employer_signup')
    
    other_user = get_object_or_404(User, id=user_id)
    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')
    
    # Mark messages as read
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.save()
            return redirect('conversation_detail', user_id=user_id)
    else:
        form = MessageForm()
    
    context = {
        'messages': messages_list,
        'other_user': other_user,
        'form': form,
        'employer': employer,
    }
    return render(request, 'employer/conversation_detail.html', context)

@login_required
def send_message_ajax(request):
    """AJAX endpoint for sending messages"""
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        
        if receiver_id and subject and message_text:
            receiver = get_object_or_404(User, id=receiver_id)
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver,
                subject=subject,
                message=message_text
            )
            return JsonResponse({
                'success': True,
                'message_id': message.id,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M')
            })
    
    return JsonResponse({'success': False})

@login_required
def quick_status_update(request, application_id):
    """Quick status update for applications"""
    if request.method != 'POST':
        return redirect('all_applications')
    
    # Check if user is an employer
    try:
        employer = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        # Check if user is a job seeker
        try:
            job_seeker = JobSeeker.objects.get(user=request.user)
            messages.error(request, "This page is for employers only. You are registered as a job seeker.")
            return redirect('job_seeker_dashboard')
        except JobSeeker.DoesNotExist:
            messages.error(request, "Please complete your employer profile first.")
            return redirect('employer_signup')
    
    application = get_object_or_404(JobApplication, id=application_id, job__employer=employer)
    new_status = request.POST.get('status')
    
    if new_status in ['applied', 'reviewing', 'shortlisted', 'interviewed', 'hired', 'rejected', 'withdrawn']:
        # Check if this is a final decision
        if application.is_final_decision(new_status):
            if application.decision_made:
                messages.error(request, 'A final decision has already been made on this application. You cannot change it.')
            else:
                # Mark as decision made
                application.decision_made = True
                application.decision_date = timezone.now()
                application.status = new_status
                application.save()
                
                status_display = dict(JobApplication.STATUS_CHOICES)[new_status]
                messages.success(request, f'Application status updated to "{status_display}" successfully!')
        else:
            # Non-final decision, can always change
            application.status = new_status
            application.save()
            
            status_display = dict(JobApplication.STATUS_CHOICES)[new_status]
            messages.success(request, f'Application status updated to "{status_display}" successfully!')
    else:
        messages.error(request, 'Invalid status provided.')
    
    # Redirect back to the referring page
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('all_applications')

@login_required
def approval_status(request):
    """Check employer approval status"""
    # Check if user is an employer
    try:
        employer = Employer.objects.get(user=request.user)
        context = {
            'employer': employer,
            'is_approved': employer.is_approved,
            'approval_date': employer.approval_date,
            'approval_notes': employer.approval_notes,
            'created_date': employer.created_at,
        }
        return render(request, 'employer/approval_status.html', context)
    except Employer.DoesNotExist:
        # Check if user is a job seeker
        try:
            job_seeker = JobSeeker.objects.get(user=request.user)
            messages.error(request, "This page is for employers only. You are registered as a job seeker.")
            return redirect('job_seeker_dashboard')  # Redirect to job seeker dashboard
        except JobSeeker.DoesNotExist:
            # User has no profile - they need to complete employer signup
            messages.error(request, "Please complete your employer profile first.")
            return redirect('employer_signup')
