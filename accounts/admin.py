from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_active', "is_verified")
    list_filter = ('email', 'is_staff', 'is_active', "is_verified")
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        ('Authentication', {
            "fields": ("email", "password")
        }),
        ('Permissions', {
            "fields": (
                "is_staff", "is_active", "is_superuser", "is_verified"
            )
        }),
        ('Group Permissions', {
            "fields": (
                "groups", "user_permissions"
            )
        }),
        ('Important Dates', {
            "fields": (
                "last_login",
            )
        })
    )
    add_fieldsets = (
        (None, {
            "fields": ("email", "password1", "password2", "is_staff", "is_active", "is_superuser", "is_verified")
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass