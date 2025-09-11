from TeoNiko.common.models import LikedItem
from TeoNiko.jewels.models import Category


def nav_categories(request):
    return {
        "categories": Category.objects.order_by("name")
    }

def wishlist_count(request):
    if request.user.is_authenticated:
        qs = LikedItem.objects.filter(user=request.user)
    else:
        key = request.session.get("guest_key") or request.session.session_key
        if not key:
            return {"wishlist_count": 0}
        qs = LikedItem.objects.filter(session_key=key)
    return {"wishlist_count": qs.count()}
