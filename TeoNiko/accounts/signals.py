from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomerProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_profile_when_user_is_created(sender, instance, created, **kwargs):

    if not created:
        return

    def _create_profile():
        CustomerProfile.objects.get_or_create(user=instance)
    transaction.on_commit(_create_profile)