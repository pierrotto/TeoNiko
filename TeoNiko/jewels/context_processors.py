from TeoNiko.jewels.models import Category


def nav_categories(request):
    return {
        "categories": Category.objects.order_by("name")
    }
