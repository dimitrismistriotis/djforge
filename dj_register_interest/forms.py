"""Forms for the dj_register_interest app."""
from django import forms
from .models import Interest


class InterestForm(forms.ModelForm):
    """Form for a user's interest in the project."""

    class Meta:
        model = Interest
        fields = ["name", "email", "github_handle"]
