"""User and Permissions models for the dj_users app."""
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.utils.translation import gettext as _
from django.db import models


class UserManager(DjangoUserManager):
    """Custom user manager for the User model."""

    def create_superuser(
        self, username=None, email=None, password=None, **extra_fields
    ):
        """Create and return a superuser with the given email and password.

        Overrides the absence of username field in the superuser creation by supplying
        email as the username field.

        Reference:
        https://simpleisbetterthancomplex.com/tutorial/
        2016/07/22/how-to-extend-django-user-model.html
        """
        return super().create_superuser(
            username=email, email=email, password=password, **extra_fields
        )


class User(AbstractUser):
    """Application's user model."""

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []  # Because of USERNAME_FIELD

    objects = UserManager()

    email = models.EmailField(_("email address"), blank=True, unique=True)

    def display(self) -> str:
        """Return a string representation of the user."""
        return f"{self.first_name} {self.last_name} ({self.email})"
