from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser from environment variables'

    def handle(self, *args, **options):
        # Get credentials from environment variables
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not password:
            self.stdout.write(
                self.style.ERROR('DJANGO_SUPERUSER_PASSWORD environment variable not set!')
            )
            return

        # Check if superuser already exists (using email, not username)
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser with email "{email}" already exists. Skipping creation.')
            )
            return

        # Create superuser (no username needed!)
        User.objects.create_superuser(
            email=email,
            password=password
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Superuser "{email}" created successfully!')
        )