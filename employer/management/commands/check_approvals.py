from django.core.management.base import BaseCommand
from employer.models import Employer
from django.utils import timezone

class Command(BaseCommand):
    help = 'Check employer approval status'

    def add_arguments(self, parser):
        parser.add_argument(
            '--status',
            type=str,
            choices=['all', 'pending', 'approved', 'rejected'],
            default='all',
            help='Filter by approval status'
        )

    def handle(self, *args, **options):
        status_filter = options['status']
        
        self.stdout.write(self.style.SUCCESS('=== EMPLOYER APPROVAL STATUS ==='))
        
        if status_filter == 'all':
            employers = Employer.objects.all()
        elif status_filter == 'pending':
            employers = Employer.objects.filter(is_approved=False)
        elif status_filter == 'approved':
            employers = Employer.objects.filter(is_approved=True)
        elif status_filter == 'rejected':
            employers = Employer.objects.filter(is_approved=False)
        
        if not employers.exists():
            self.stdout.write(self.style.WARNING('No employers found with the specified criteria.'))
            return
        
        for employer in employers:
            status_icon = "✅" if employer.is_approved else "⏳"
            status_text = "APPROVED" if employer.is_approved else "PENDING"
            
            self.stdout.write(
                f"{status_icon} {employer.company_name} | "
                f"User: {employer.user.email} | "
                f"Status: {status_text} | "
                f"Created: {employer.created_at.strftime('%Y-%m-%d %H:%M')}"
            )
            
            if employer.is_approved and employer.approval_date:
                self.stdout.write(
                    f"   └─ Approved on: {employer.approval_date.strftime('%Y-%m-%d %H:%M')}"
                )
            
            if employer.approval_notes:
                self.stdout.write(f"   └─ Notes: {employer.approval_notes}")
        
        # Summary
        total = Employer.objects.count()
        approved = Employer.objects.filter(is_approved=True).count()
        pending = Employer.objects.filter(is_approved=False).count()
        
        self.stdout.write(self.style.SUCCESS(f'\n=== SUMMARY ==='))
        self.stdout.write(f"Total Employers: {total}")
        self.stdout.write(f"Approved: {approved}")
        self.stdout.write(f"Pending: {pending}") 