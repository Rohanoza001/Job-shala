from django.core.management.base import BaseCommand
from employer.models import Employer
from django.utils import timezone

class Command(BaseCommand):
    help = 'Approve employers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--company',
            type=str,
            help='Company name to approve (exact match)'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='User email to approve'
        )
        parser.add_argument(
            '--all-pending',
            action='store_true',
            help='Approve all pending employers'
        )
        parser.add_argument(
            '--notes',
            type=str,
            default='Approved via management command',
            help='Approval notes'
        )

    def handle(self, *args, **options):
        company_name = options.get('company')
        email = options.get('email')
        all_pending = options.get('all_pending')
        notes = options.get('notes')
        
        if all_pending:
            employers = Employer.objects.filter(is_approved=False)
            self.stdout.write(f'Found {employers.count()} pending employers')
        elif company_name:
            employers = Employer.objects.filter(company_name=company_name, is_approved=False)
            self.stdout.write(f'Found {employers.count()} employers with company name: {company_name}')
        elif email:
            employers = Employer.objects.filter(user__email=email, is_approved=False)
            self.stdout.write(f'Found {employers.count()} employers with email: {email}')
        else:
            self.stdout.write(self.style.ERROR('Please specify --company, --email, or --all-pending'))
            return
        
        if not employers.exists():
            self.stdout.write(self.style.WARNING('No pending employers found to approve.'))
            return
        
        approved_count = 0
        for employer in employers:
            employer.is_approved = True
            employer.approval_date = timezone.now()
            employer.approval_notes = notes
            employer.save()
            approved_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Approved: {employer.company_name} ({employer.user.email})')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully approved {approved_count} employer(s)!')
        ) 