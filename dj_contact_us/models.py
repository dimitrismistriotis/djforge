"""Models for the dj_contact_us app."""
from django.db import models


class ContactUsEntry(models.Model):
    """Contact Us entry."""

    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return (
            f'ContactUsEntry(email="{self.email}", created_at="{self.created_at}", '
            f'message="{self.message}", name="{self.name}")'
        )

    def __str__(self) -> str:
        """Return a description of the model."""
        return f"Contact from {self.email} on {self.created_at}"
