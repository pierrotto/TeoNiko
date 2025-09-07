import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from TeoNiko.common.models import Rating
from TeoNiko.jewels.models import Category, Jewel


def home(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'common\home-page.html', context)

@require_POST
def rate(request, pk):
    obj = get_object_or_404(Jewel, pk=pk)
    ct = ContentType.objects.get_for_model(Jewel)

    try:
        payload = json.loads(request.body.decode("utf-8")) if request.body else request.POST
    except Exception:
        payload = request.POST

    raw = payload.get("rating") or payload.get("value")
    try:
        val = int(raw)
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "error": "invalid-rating"}, status=400)

    val = max(1, min(5, val))

    if request.user.is_authenticated:
        ident = {"user": request.user}
    else:
        if not request.session.session_key:
            request.session.create()
        ident = {"session_key": request.session.session_key}

    Rating.objects.update_or_create(
        content_type=ct,
        object_id=obj.pk,
        defaults={"rating": val},
        **ident,
    )

    obj.refresh_from_db(fields=["rating_avg", "rating_count"])
    return JsonResponse({
        "ok": True,
        "avg": float(obj.rating_avg or 0),
        "count": int(obj.rating_count or 0),
    })