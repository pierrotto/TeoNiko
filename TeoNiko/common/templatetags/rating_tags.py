from django import template
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

register = template.Library()

@register.simple_tag
def rating_url(obj):
    ct = ContentType.objects.get_for_model(obj, for_concrete_model=False)
    return reverse('common:rate', args=[ct.app_label, ct.model, obj.pk])
