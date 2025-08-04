from django.shortcuts import render

from TeoNiko.jewels.models import Category


def home(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'common\home-page.html', context)

