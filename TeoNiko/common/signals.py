from django.contrib.auth import user_logged_in
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Avg, Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from .models import Rating, LikedItem
from ..jewels.models import Jewel


def _recalc_for(obj):
    if not hasattr(obj, "rating_avg") or not hasattr(obj, "rating_count"):
        return
    agg = Rating.objects.filter(
        content_type__model=obj._meta.model_name,
        content_type__app_label=obj._meta.app_label,
        object_id=obj.pk,
    ).aggregate(avg=Avg("rating"), cnt=Count("id"))
    obj.rating_avg = round(agg["avg"] or 0, 2)
    obj.rating_count = agg["cnt"] or 0
    obj.save(update_fields=["rating_avg", "rating_count"])


@receiver(post_save, sender=Rating)
def rating_saved(sender, instance, **kwargs):
    _recalc_for(instance.content_object)


@receiver(post_delete, sender=Rating)
def rating_deleted(sender, instance, **kwargs):
    _recalc_for(instance.content_object)

@receiver(user_logged_in)
def migrate_guest_data(sender, request, user, **kwargs):
    sk = request.session.get("guest_key") or request.session.session_key
    if not sk:
        return

    with transaction.atomic():
        guest_ratings = (
            Rating.objects
            .select_for_update()
            .filter(session_key=sk, user__isnull=True)
        )

        for r in guest_ratings:
            try:
                ur = Rating.objects.get(
                    content_type=r.content_type,
                    object_id=r.object_id,
                    user=user
                )
                if ur.updated_at >= r.updated_at:
                    r.delete()
                else:
                    ur.rating = r.rating
                    ur.updated_at = timezone.now()
                    ur.save(update_fields=["rating", "updated_at"])
                    r.delete()
            except Rating.DoesNotExist:
                r.user = user
                r.session_key = None
                r.save(update_fields=["user", "session_key"])

        guest_likes = (
            LikedItem.objects
            .select_for_update()
            .filter(session_key=sk, user__isnull=True)
        )

        for li in guest_likes:
            existing = (
                LikedItem.objects
                .filter(user=user, jewel=li.jewel)
                .first()
            )
            if existing:
                if li.created_at and (not existing.created_at or li.created_at > existing.created_at):
                    existing.created_at = li.created_at
                    existing.save(update_fields=["created_at"])
                li.delete()
            else:
                li.user = user
                li.session_key = None
                li.save(update_fields=["user", "session_key"])

def _ensure_guest_key(request):
    sk = request.session.get('guest_key')
    if not sk:
        request.session.save()
        sk = request.session.session_key
        request.session['guest_key'] = sk
    return sk

@receiver(user_logged_in)
def migrate_guest_data(sender, request, user, **kwargs):
    sk = request.session.get('guest_key') or request.session.session_key
    if not sk:
        return

    with transaction.atomic():
        ct_jewel = ContentType.objects.get_for_model(Jewel)
        guest_qs = (Rating.objects
                    .select_for_update()
                    .filter(session_key=sk, user__isnull=True))

        for r in guest_qs:
            try:
                ur = Rating.objects.get(
                    content_type=r.content_type,
                    object_id=r.object_id,
                    user=user
                )

                if ur.updated_at >= r.updated_at:
                    r.delete()
                else:
                    ur.rating = r.rating
                    ur.updated_at = timezone.now()
                    ur.save(update_fields=['rating', 'updated_at'])
                    r.delete()
            except Rating.DoesNotExist:
                r.user = user
                r.session_key = None
                r.save(update_fields=['user', 'session_key'])