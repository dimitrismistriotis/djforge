"""Admin file for dj_register_interest app."""
from django.contrib import admin

from .models import Interest


class InterestAdmin(admin.ModelAdmin):
    """Admin class for Interest model."""

    list_display = (
        "name",
        "email",
        "github_handle",
        "created_at",
    )
    search_fields = (
        "email",
        "github_handle",
    )

    ordering = ("-id",)


admin.site.register(Interest, InterestAdmin)
