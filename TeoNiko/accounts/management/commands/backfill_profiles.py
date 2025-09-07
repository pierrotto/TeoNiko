from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from TeoNiko.accounts.models import CustomerProfile

class Command(BaseCommand):
    help = "Create missing CustomerProfile rows for existing users."

    def handle(self, *args, **options):
        User = get_user_model()
        created = 0
        for user in User.objects.all().only("id"):
            _, was_created = CustomerProfile.objects.get_or_create(user=user)
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Profiles created: {created}"))