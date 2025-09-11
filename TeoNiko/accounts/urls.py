from django.urls import path
from .views import auth_portal, account_settings, account_entry
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", account_entry, name="account-entry"),
    path("auth/", auth_portal, name="auth-portal"),
    path("profile/", account_settings, name="account-settings"),
    path("logout/", LogoutView.as_view(), name="logout"),

]