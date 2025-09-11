from django.db.models import Exists, OuterRef, Value, BooleanField, Count
from TeoNiko.common.models import LikedItem


class LikeAnnotateMixin:
    def with_likes(self, qs):
        request = self.request
        like_qs = LikedItem.objects.filter(jewel_id=OuterRef("pk"))

        if request.user.is_authenticated:
            like_qs = like_qs.filter(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            like_qs = like_qs.filter(session_key=request.session.session_key)

        return qs.annotate(is_liked=Exists(like_qs))
