from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from TeoNiko import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('TeoNiko.common.urls')),
    path('category/', include('TeoNiko.jewels.category_urls')),
    path('jewel/', include('TeoNiko.jewels.jewel_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
