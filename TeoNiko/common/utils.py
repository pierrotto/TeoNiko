def _ensure_guest_key(request):
    if not request.session.session_key:
        request.session.create()
    if not request.session.get("guest_key"):
        request.session["guest_key"] = request.session.session_key
    return request.session["guest_key"]

def like_ident(request):
    if request.user.is_authenticated:
        return {"user": request.user}
    if not request.session.session_key:
        request.session.create()
    key = request.session.setdefault("guest_key", request.session.session_key)
    return {"session_key": key}