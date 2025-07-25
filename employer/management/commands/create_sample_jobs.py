from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employer.models import Employer, Job
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Create sample jobs for testing'

    def handle(self, *args, **options):
        # Create a sample employer if it doesn't exist
        user, created = User.objects.get_or_create(
            username='sample_employer@example.com',
            defaults={
                'email': 'sample_employer@example.com',
                'first_name': 'Sample',
                'last_name': 'Employer',
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write('Created sample employer user')
        
        # Create employer profile
        employer, created = Employer.objects.get_or_create(
            user=user,
            defaults={
                'company_name': 'TechCorp Solutions',
                'designation': 'HR Manager',
                'department': 'Human Resources',
                'phone': '+91-9876543210',
                'company_email': 'hr@techcorp.com',
                'company_phone': '+91-9876543211',
                'address': '123 Tech Park, Bangalore',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'country': 'India',
                'pincode': '560001',
                'is_verified': True,
            }
        )
        
        if created:
            self.stdout.write('Created sample employer profile')
        
        # Sample job data
        sample_jobs = [
            {
                'title': 'Senior Python Developer',
                'location': 'Mumbai, Maharashtra',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': 800000,
                'salary_max': 1500000,
                'description': 'We are looking for a Senior Python Developer to join our dynamic team. You will be responsible for developing and maintaining high-quality software solutions.',
                'requirements': '• 5+ years of experience in Python development\n• Strong knowledge of Django, Flask, or FastAPI\n• Experience with databases (PostgreSQL, MySQL)\n• Knowledge of cloud platforms (AWS, Azure, GCP)\n• Excellent problem-solving skills',
                'benefits': '• Competitive salary\n• Health insurance\n• Flexible working hours\n• Professional development opportunities\n• Annual bonus',
                'skills_required': 'Python, Django, PostgreSQL, AWS, Git, Docker',
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'Frontend React Developer',
                'location': 'Delhi, NCR',
                'job_type': 'full-time',
                'experience_level': 'mid',
                'salary_min': 600000,
                'salary_max': 1200000,
                'description': 'Join our frontend team to build amazing user experiences. We are looking for a React developer who is passionate about creating beautiful and functional web applications.',
                'requirements': '• 3+ years of experience in React development\n• Strong knowledge of JavaScript, TypeScript\n• Experience with state management (Redux, Context API)\n• Knowledge of modern CSS and responsive design\n• Experience with testing frameworks',
                'benefits': '• Competitive salary\n• Remote work options\n• Health and dental insurance\n• Learning and development budget\n• Team events and activities',
                'skills_required': 'React, JavaScript, TypeScript, Redux, CSS3, HTML5, Jest',
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': 'DevOps Engineer',
                'location': 'Bangalore, Karnataka',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': 1000000,
                'salary_max': 2000000,
                'description': 'We are seeking a DevOps Engineer to help us build and maintain our cloud infrastructure. You will be responsible for automating deployment processes and ensuring system reliability.',
                'requirements': '• 5+ years of experience in DevOps\n• Strong knowledge of AWS, Azure, or GCP\n• Experience with Docker and Kubernetes\n• Knowledge of CI/CD pipelines\n• Experience with monitoring and logging tools',
                'benefits': '• Competitive salary\n• Stock options\n• Health insurance\n• Flexible working hours\n• Conference and training budget',
                'skills_required': 'AWS, Docker, Kubernetes, Jenkins, Terraform, Ansible, Linux',
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'UX/UI Designer',
                'location': 'Remote',
                'job_type': 'contract',
                'experience_level': 'mid',
                'salary_min': 500000,
                'salary_max': 800000,
                'description': 'We are looking for a talented UX/UI Designer to create beautiful and intuitive user interfaces. You will work closely with our product and development teams.',
                'requirements': '• 3+ years of experience in UX/UI design\n• Proficiency in Figma, Sketch, or Adobe XD\n• Strong understanding of user-centered design principles\n• Experience with design systems\n• Portfolio showcasing your work',
                'benefits': '• Competitive contract rate\n• Flexible working hours\n• Remote work\n• Opportunity for full-time conversion\n• Creative freedom',
                'skills_required': 'Figma, Sketch, Adobe XD, Prototyping, User Research, Design Systems',
                'is_active': True,
                'is_featured': False,
            },
            {
                'title': 'Data Scientist',
                'location': 'Hyderabad, Telangana',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': 1200000,
                'salary_max': 2500000,
                'description': 'Join our data science team to build machine learning models and derive insights from large datasets. You will work on cutting-edge AI/ML projects.',
                'requirements': '• 5+ years of experience in data science\n• Strong knowledge of Python, R, or Julia\n• Experience with machine learning frameworks\n• Knowledge of statistics and mathematics\n• Experience with big data technologies',
                'benefits': '• Competitive salary\n• Health insurance\n• Flexible working hours\n• Research and development opportunities\n• Conference attendance',
                'skills_required': 'Python, TensorFlow, PyTorch, Pandas, NumPy, Scikit-learn, SQL',
                'is_active': True,
                'is_featured': True,
            },
            {
                'title': 'Product Manager',
                'location': 'Pune, Maharashtra',
                'job_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': 1500000,
                'salary_max': 3000000,
                'description': 'We are looking for a Product Manager to drive product strategy and execution. You will work closely with engineering, design, and business teams.',
                'requirements': '• 5+ years of experience in product management\n• Strong analytical and strategic thinking\n• Experience with agile methodologies\n• Excellent communication skills\n• Technical background preferred',
                'benefits': '• Competitive salary\n• Stock options\n• Health insurance\n• Flexible working hours\n• Professional development',
                'skills_required': 'Product Strategy, Agile, Analytics, User Research, Roadmapping, Stakeholder Management',
                'is_active': True,
                'is_featured': False,
            },
        ]
        
        # Create sample jobs
        created_count = 0
        for job_data in sample_jobs:
            job, created = Job.objects.get_or_create(
                title=job_data['title'],
                employer=employer,
                defaults={
                    **job_data,
                    'employer': employer,
                    'company_name': employer.company_name,
                    'created_at': timezone.now() - timedelta(days=created_count),
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created job: {job.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample jobs')
        ) 