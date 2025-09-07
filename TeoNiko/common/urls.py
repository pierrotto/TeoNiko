from django.urls import path
from TeoNiko.common import views

urlpatterns = [
    path("", views.home, name="home"),
]