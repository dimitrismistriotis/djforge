"""Admin configuration for the dj_contact_us app."""
from django.contrib import admin

from .models import ContactUsEntry


class ContactUsEntryAdmin(admin.ModelAdmin):
    """Admin class for ContactUsEntry model."""

    list_display = (
        "name",
        "email",
        "message",
        "created_at",
    )
    search_fields = (
        "email",
        "name",
    )

    ordering = ("-id",)


admin.site.register(ContactUsEntry, ContactUsEntryAdmin)
