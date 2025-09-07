from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import secrets

from TeoNiko.accounts.models import CustomerProfile

UserModel = get_user_model()

class EmailUserCreationForm(UserCreationForm):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.fields.pop("username", None)

    class Meta:
        model = UserModel
        fields = ("email", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        base = slugify(self.cleaned_data["email"].split("@")[0]) or "user"
        candidate = base
        i = 0
        while UserModel.objects.filter(username=candidate).exists():
            i += 1
            candidate = f"{base}-{i}-{secrets.token_hex(2)}"
        user.username = candidate
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ("first_name", "last_name", "email")

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise ValidationError("Email is required.")
        exists = UserModel.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists()
        if exists:
            raise ValidationError("This email is already in use.")
        return email


class UsernameForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ("username",)


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = (
            "phone",
            "address_line1", "address_line2",
            "city", "province", "postal_code", "country",
        )

