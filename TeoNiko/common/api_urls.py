from django.urls import path
from TeoNiko.common import views

app_name = "common_api"

urlpatterns = [
    path("rate/jewel/<int:pk>/", views.rate, name="rate-jewel"),
]
