"""Forms for the dj_contact_us app."""
from django import forms
from .models import ContactUsEntry


class ContactUsEntryForm(forms.ModelForm):
    """Form for ContactUsEntry model."""

    class Meta:
        """Meta class for ContactUsEntry form."""

        model = ContactUsEntry
        fields = ["name", "email", "message"]
