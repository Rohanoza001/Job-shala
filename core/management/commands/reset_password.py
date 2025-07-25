from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Reset user password'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='User email to reset password for'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='123456',
            help='New password (default: 123456)'
        )

    def handle(self, *args, **options):
        email = options.get('email')
        password = options.get('password')
        
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Password reset for {user.email}')
            )
            self.stdout.write(f'Username: {user.username}')
            self.stdout.write(f'Email: {user.email}')
            self.stdout.write(f'New Password: {password}')
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ User with email {email} not found')
            ) 