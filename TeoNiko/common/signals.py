from django.db.models import Avg, Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Rating


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
