from django.contrib import admin
from .models import CustomerProfile
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    fk_name = "user"


try:
    admin.site.unregister(UserModel)
except admin.sites.NotRegistered:
    pass

@admin.register(UserModel)
class UserAdmin(DjangoUserAdmin):
    inlines = [CustomerProfileInline]

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "city", "country")
    search_fields = ("user__email", "phone", "city", "country")

