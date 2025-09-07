# common/models.py
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator


class Rating(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id    = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             on_delete=models.SET_NULL, related_name='ratings')
    session_key = models.CharField(max_length=40, blank=True, default='')

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id', 'user'],
                name='uniq_rating_user',
                condition=Q(user__isnull=False),
            ),
            models.UniqueConstraint(
                fields=['content_type', 'object_id', 'session_key'],
                name='uniq_rating_session',
                condition=~Q(session_key=''),
            ),
        ]
