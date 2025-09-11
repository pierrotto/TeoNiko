from django.conf import settings
from django.db import models

class CustomerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    phone = models.CharField(
        max_length=32,
        blank=True
    )

    address_line1 = models.CharField(
        max_length=120,
        blank=True
    )

    address_line2 = models.CharField(
        max_length=120,
        blank=True
    )

    city = models.CharField(
        max_length=80,
        blank=True
    )

    province = models.CharField(
        max_length=80,
        blank=True
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True
    )

    country = models.CharField(
        max_length=80,
        blank=True
    )

    def __str__(self):
        return f"Profile({self.user.email})"
