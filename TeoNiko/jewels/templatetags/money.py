# TeoNiko/jewels/templatetags/money.py
from decimal import Decimal, ROUND_HALF_UP
from django import template

register = template.Library()
RATE = Decimal("1.95583")  # fixed BGN -> EUR per your request

@register.filter
def to_eur(value, places=2):
    try:
        d = Decimal(str(value)) / RATE
    except Exception:
        return ""
    q = Decimal("1").scaleb(-int(places))  # 0.01 for 2 places
    return f"{d.quantize(q, rounding=ROUND_HALF_UP)}"
