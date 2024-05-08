"""Admin configuration for dj_users app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class DjAdmin(UserAdmin):
    """Admin class for Users."""

    list_display = ["username"]


admin.site.register(User, DjAdmin)
