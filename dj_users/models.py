"""User and Permissions models for the dj_users app."""

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.db import models


class User(AbstractUser):
    """Application's user model."""

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]  # Because of USERNAME_FIELD

    email = models.EmailField(_("email address"), blank=True, unique=True)

    def display(self) -> str:
        """Return a string representation of the user."""
        return f"{self.first_name} {self.last_name} ({self.email})"
