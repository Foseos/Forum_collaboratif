from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserIPLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "role", "is_active", "date_joined"]
    list_filter = ["role", "is_active", "is_staff"]
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Profil", {"fields": ("role", "avatar", "avatar_name", "bio")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Profil", {"fields": ("role", "avatar", "avatar_name", "bio")}),
    )


@admin.register(UserIPLog)
class UserIPLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'ip_address', 'event', 'created_at']
    list_filter = ['event', 'created_at']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['user', 'ip_address', 'event', 'created_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
