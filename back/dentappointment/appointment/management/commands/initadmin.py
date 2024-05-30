from django.core.management.base import BaseCommand
from dentappointment.appointment.models import Owner

class Command(BaseCommand):
    help = 'Create a default admin user'

    def handle(self, *args, **options):
        if not Owner.objects.filter(username='admin').exists():
            Owner.objects.create_superuser(
                username='admin',
                email='admin@citassalud.com',
                password='tesca123'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created default admin user'))
        else:
            self.stdout.write(self.style.WARNING('Default admin user already exists'))