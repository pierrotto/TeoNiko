from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from TeoNiko import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # web pages
    path("", include("TeoNiko.common.urls")),
    path("category/", include("TeoNiko.jewels.category_urls")),
    path("jewel/", include("TeoNiko.jewels.jewel_urls")),

    # API-only endpoints (AJAX)
    path("api/", include(("TeoNiko.common.api_urls", "api"), namespace="api")),

    # auth: your custom + Django auth under the same prefix
    path("accounts/", include("TeoNiko.accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
