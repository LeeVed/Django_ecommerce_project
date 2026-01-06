from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "country", "phone_number", "is_staff", "is_active")
    list_filter = ("country", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "first_name", "last_name", "phone_number", "country")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Персональная информация"), {
            "fields": ("first_name", "last_name", "avatar", "phone_number", "country")
        }),
        (_("Права и разрешения"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            "classes": ("collapse",)
        }),
        (_("Важные даты"), {
            "fields": ("last_login", "date_joined"),
            "classes": ("collapse",)
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "first_name", "last_name"),
        }),
    )
    readonly_fields = ("last_login", "date_joined")
