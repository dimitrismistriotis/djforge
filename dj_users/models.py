"""User and Permissions models for the dj_users app."""
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Application's user model."""

    USERNAME_FIELD = "email"
