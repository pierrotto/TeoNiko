# common/models.py
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator


class Rating(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='ratings'
    )

    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        default=None,
        db_index=True
    )

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(5)]
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

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
                condition=Q(session_key__isnull=False),
            ),
            models.CheckConstraint(
                name='rating_exactly_one_owner',
                check=(
                        Q(user__isnull=False, session_key__isnull=True) |
                        Q(user__isnull=True, session_key__isnull=False)
                ),
            ),
        ]


class LikedItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="liked_items",
    )

    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True
    )

    jewel = models.ForeignKey(
        "jewels.Jewel",
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "jewel"],
                name="uniq_like_user_jewel",
                condition=Q(user__isnull=False),
            ),
            models.UniqueConstraint(
                fields=["session_key", "jewel"],
                name="uniq_like_session_jewel",
                condition=~Q(session_key=False),
            ),
            models.CheckConstraint(
                name='like_exactly_one_owner',
                check=(Q(user__isnull=False, session_key__isnull=True) |
                       Q(user__isnull=True, session_key__isnull=False)),
            ),
        ]

        indexes = [
            models.Index(fields=["user", "jewel"]),
            models.Index(fields=["session_key", "jewel"]),
            models.Index(fields=["jewel", "-created_at"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        who = self.user or f"session:{self.session_key[:7]}"
        return f"{who} ❤ {self.jewel}"
