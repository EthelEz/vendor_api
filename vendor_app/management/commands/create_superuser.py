from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser with a predefined password'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='dollar_queen').exists():
            User.objects.create_superuser('dollar_queen', 'dollarqueen@gmail.com', 'Vwbuyfa@900')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser "dollar_queen"'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "dollar_queen" already exists'))