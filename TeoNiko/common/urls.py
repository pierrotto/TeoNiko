from django.urls import path
from TeoNiko.common import views

urlpatterns = [
    path("", views.home, name="home"),
    path("likes/toggle/<int:jewel_id>/", views.toggle_like, name="toggle-like"),
    path("wishlist/", views.wishlist, name="wishlist"),
]
