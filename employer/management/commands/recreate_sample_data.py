from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employer.models import Employer, Job
from django.utils import timezone
from decimal import Decimal

class Command(BaseCommand):
    help = 'Recreate sample employers and jobs'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create or get user for Nutan
        user, created = User.objects.get_or_create(
            email='Rohanoza272@gmail.com',
            defaults={
                'username': 'nutan_hr',
                'first_name': 'Nutan',
                'last_name': 'HR',
                'is_active': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(f'✅ Created user: {user.email}')
        else:
            self.stdout.write(f'✅ Found existing user: {user.email}')
        
        # Create or update Nutan employer
        employer, created = Employer.objects.get_or_create(
            user=user,
            defaults={
                'company_name': 'Nutan',
                'designation': 'HR Manager',
                'department': 'Human Resources',
                'phone': '+91-9876543210',
                'company_website': 'https://nutan.com',
                'company_email': 'hr@nutan.com',
                'company_phone': '+91-9876543210',
                'address': '123 Tech Park, Pune',
                'city': 'Pune',
                'state': 'Maharashtra',
                'country': 'India',
                'pincode': '411001',
                'is_approved': True,
                'is_verified': True,
                'approval_date': timezone.now(),
            }
        )
        
        if created:
            self.stdout.write(f'✅ Created employer: {employer.company_name}')
        else:
            # Update existing employer to approved status
            employer.is_approved = True
            employer.is_verified = True
            employer.approval_date = timezone.now()
            employer.save()
            self.stdout.write(f'✅ Updated employer: {employer.company_name}')
        
        # Create sample jobs
        sample_jobs = [
            {
                'title': 'Senior Python Developer',
                'location': 'Pune, Maharashtra',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': Decimal('800000'),
                'salary_max': Decimal('1200000'),
                'description': 'We are looking for an experienced Python developer to join our team.',
                'requirements': '5+ years of Python experience, Django, PostgreSQL',
                'skills_required': 'Python, Django, PostgreSQL, REST APIs',
            },
            {
                'title': 'Frontend React Developer',
                'location': 'Mumbai, Maharashtra',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'salary_min': Decimal('600000'),
                'salary_max': Decimal('900000'),
                'description': 'Join our frontend team to build amazing user experiences.',
                'requirements': '3+ years of React experience, TypeScript',
                'skills_required': 'React, TypeScript, HTML, CSS, JavaScript',
            },
            {
                'title': 'DevOps Engineer',
                'location': 'Bangalore, Karnataka',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': Decimal('900000'),
                'salary_max': Decimal('1400000'),
                'description': 'Help us scale our infrastructure and deployment processes.',
                'requirements': '5+ years of DevOps experience, AWS, Docker',
                'skills_required': 'AWS, Docker, Kubernetes, CI/CD, Linux',
            },
            {
                'title': 'UX/UI Designer',
                'location': 'Remote',
                'job_type': 'contract',
                'experience_level': 'mid',
                'salary_min': Decimal('500000'),
                'salary_max': Decimal('800000'),
                'description': 'Create beautiful and intuitive user interfaces.',
                'requirements': '3+ years of design experience, Figma, Adobe Creative Suite',
                'skills_required': 'Figma, Adobe Creative Suite, User Research, Prototyping',
            },
            {
                'title': 'Data Scientist',
                'location': 'Hyderabad, Telangana',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': Decimal('1000000'),
                'salary_max': Decimal('1500000'),
                'description': 'Build machine learning models and data-driven solutions.',
                'requirements': '5+ years of data science experience, Python, ML',
                'skills_required': 'Python, Machine Learning, Statistics, SQL, Pandas',
            },
        ]
        
        created_jobs = 0
        for job_data in sample_jobs:
            job, created = Job.objects.get_or_create(
                employer=employer,
                title=job_data['title'],
                defaults={
                    'company_name': employer.company_name,
                    'location': job_data['location'],
                    'job_type': job_data['job_type'],
                    'experience_level': job_data['experience_level'],
                    'salary_min': job_data['salary_min'],
                    'salary_max': job_data['salary_max'],
                    'description': job_data['description'],
                    'requirements': job_data['requirements'],
                    'skills_required': job_data['skills_required'],
                    'is_active': True,
                }
            )
            if created:
                created_jobs += 1
                self.stdout.write(f'✅ Created job: {job.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully created {created_jobs} new jobs!')
        )
        
        # Summary
        total_jobs = Job.objects.filter(employer=employer).count()
        active_jobs = Job.objects.filter(employer=employer, is_active=True).count()
        
        self.stdout.write(f'\n📊 Summary:')
        self.stdout.write(f'Employer: {employer.company_name} (Approved: {employer.is_approved}, Verified: {employer.is_verified})')
        self.stdout.write(f'Total Jobs: {total_jobs}')
        self.stdout.write(f'Active Jobs: {active_jobs}') 