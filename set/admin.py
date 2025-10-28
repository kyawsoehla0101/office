from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "is_active", "joined_date", "department")
    list_filter = ("position", "is_active")
    search_fields = ("full_name", "position")
    ordering = ("-joined_date",)
