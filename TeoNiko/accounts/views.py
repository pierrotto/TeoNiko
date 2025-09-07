from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from .models import CustomerProfile
from django.conf import settings
from django.contrib.auth import login as auth_login, update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import (EmailAuthenticationForm, EmailUserCreationForm,
                    UserInfoForm, UsernameForm, CustomerProfileForm)


def account_entry(request):
    if request.user.is_authenticated:
        return redirect("account-settings")
    return redirect("auth-portal")

def auth_portal(request):
    if request.user.is_authenticated:
        return redirect("account-settings")

    next_url = (
        request.POST.get("next")
        or request.GET.get("next")
        or getattr(settings, "LOGIN_REDIRECT_URL", "/")
        or "/"
    )

    if request.method == "POST" and "login-submit" in request.POST:
        login_form = EmailAuthenticationForm(request, data=request.POST, prefix="login")
        signup_form = EmailUserCreationForm(prefix="signup")
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(next_url)

    elif request.method == "POST" and "signup-submit" in request.POST:
        login_form = EmailAuthenticationForm(request, data=None, prefix="login")
        signup_form = EmailUserCreationForm(request.POST, prefix="signup")
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect(next_url)

    else:
        login_form = EmailAuthenticationForm(request, data=None, prefix="login")
        signup_form = EmailUserCreationForm(prefix="signup")

    return render(request, "accounts/auth_portal.html", {
        "login_form": login_form,
        "signup_form": signup_form,
    })

@login_required
def account_settings(request):
    user = request.user
    profile, _ = CustomerProfile.objects.get_or_create(user=user)

    next_url = (
            request.POST.get("next")
            or request.GET.get("next")
            or reverse("home")
    )

    user_form = UserInfoForm(request.POST or None, instance=user, prefix="user")
    username_form = UsernameForm(request.POST or None, instance=user, prefix="uname")
    pwd_form = PasswordChangeForm(user, request.POST or None, prefix="pwd")
    profile_form = CustomerProfileForm(request.POST or None, instance=profile, prefix="prof")

    if request.method == "POST":
        if "save-user" in request.POST and user_form.is_valid():
            user_form.save()
            return redirect(next_url)

        if "save-username" in request.POST and username_form.is_valid():
            username_form.save()
            return redirect(next_url)

        if "save-password" in request.POST and pwd_form.is_valid():
            pwd_form.save()
            update_session_auth_hash(request, user)
            return redirect(next_url)

        if "save-profile" in request.POST and profile_form.is_valid():
            profile_form.save()
            return redirect(next_url)

    return render(request, "accounts/account_settings.html", {
        "user_form": user_form,
        "username_form": username_form,
        "pwd_form": pwd_form,
        "profile_form": profile_form,
    })
