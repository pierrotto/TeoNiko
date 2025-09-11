import json
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from TeoNiko.common.models import Rating, LikedItem
from TeoNiko.jewels.models import Category, Jewel
from .utils import _ensure_guest_key, like_ident


def _like_ident(request):
    if request.user.is_authenticated:
        return {"user": request.user}
    if not request.session.session_key:
        request.session.create()
    return {"session_key": request.session.session_key}


def home(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'common\home-page.html', context)


@require_POST
@transaction.atomic
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
    val = max(1, min(5, val))  # clamp 1..5

    if request.user.is_authenticated:
        ident = {"user": request.user}
    else:
        ident = {"session_key": _ensure_guest_key(request)}

    rating_obj, _created = Rating.objects.update_or_create(
        content_type=ct,
        object_id=obj.pk,
        defaults={"rating": val},
        **ident,
    )

    obj.refresh_from_db(fields=["rating_avg", "rating_count"])

    return JsonResponse({
        "ok": True,
        "my": int(rating_obj.rating),
        "avg": float(obj.rating_avg or 0),
        "count": int(obj.rating_count or 0),
    })


@require_POST
def toggle_like(request, jewel_id: int):
    jewel = get_object_or_404(Jewel, pk=jewel_id)

    if request.user.is_authenticated:
        ident = {"user": request.user}
    else:
        sk = _ensure_guest_key(request)
        ident = {"session_key": sk}

    with transaction.atomic():
        qs = LikedItem.objects.filter(jewel=jewel, **ident)
        if qs.exists():
            qs.delete()
            liked = False
        else:
            LikedItem.objects.create(jewel=jewel, **ident)
            liked = True

    count = LikedItem.objects.filter(**ident).count()
    return JsonResponse({"liked": liked, "jewel_id": jewel.id, "count": count})

def wishlist_qs_for_request(request):
    ident = like_ident(request)
    return (
        LikedItem.objects
        .filter(**ident)
        .select_related("jewel", "jewel__category")
    )

def wishlist(request):
    likes = wishlist_qs_for_request(request).order_by("-created_at")
    return render(request, "common/wishlist.html", {"likes": likes})
