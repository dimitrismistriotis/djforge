"""Models for dj_register_interest app."""
from django_extensions.db.fields import CreationDateTimeField

from django.db import models


class Interest(models.Model):
    """Model for a user's interest in the project."""

    name = models.CharField(
        verbose_name="(Optional) name of person registering interest",
        max_length=100,
        blank=True,
    )
    email = models.EmailField(
        verbose_name=(
            "Email address to use to communicate solution's availability to user"
        )
    )
    github_handle = models.CharField(
        verbose_name=(
            "(Optional) Github Handle in case solutions grants access a repository"
        ),
        max_length=100,
        blank=True,
    )
    user_intent = models.TextField(
        verbose_name=(
            "Please write a short description of what "
            "do you hope to achieve with our solution?"
        )
    )
    created = CreationDateTimeField()

    def __str__(self) -> str:
        """Str representation of Interest."""
        return f"Interest of {self.name} ({self.email}), Github: {self.github_handle}"

    def __repr__(self) -> str:
        """Repr representation of Interest."""
        return (
            f"Interest(name={self.name}, "
            f"email={self.email}, github_handle={self.github_handle})"
        )
