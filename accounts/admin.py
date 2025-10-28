from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "full_name", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "role", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    search_fields = ("email", "full_name")
    ordering = ("email",)
    readonly_fields = ("id",)
