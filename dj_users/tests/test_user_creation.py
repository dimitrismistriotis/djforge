"""Tests related to creating users."""

import pytest

from django.contrib.auth import get_user_model

pytestmark = [pytest.mark.django_db]


class TestUserCreation:
    """Test the creation of users."""

    USER_MODEL = get_user_model()

    def test_create_user(self):
        """Test creating a user."""
        user = self.USER_MODEL.objects.create_user(
            username="person@example.com", email="person@example.com"
        )

        assert user
        assert self.USER_MODEL.objects.exists()

    def test_user_is_also_created_with_trivial_password(self):
        """Test that the user is created with a trivial password.

        Validation does not apply at this level:

        > By default, validators are used in the forms to reset or change
        > passwords and in the createsuperuser and change password management
        > commands. Validators aren’t applied at the model level,
        > for example in User.objects.create_user() and create_superuser(),
        > because we assume that developers, not users,
        > interact with Django at that level and also because model validation
        > doesn't automatically run as part of creating models.

        Source: https://docs.djangoproject.com/en/dev/topics/auth/passwords/
        """
        user = self.USER_MODEL.objects.create_user(
            username="person@example.com", email="person@example.com", password="123456"
        )

        assert user
        assert self.USER_MODEL.objects.exists()

    def test_create_super_user(self):
        """Test creating a super user."""
        user = self.USER_MODEL.objects.create_superuser(
            email="person@example.com", password="SuperSecretPassword123!"
        )

        assert user
        assert self.USER_MODEL.objects.exists()
        assert user.is_staff
        assert user.is_superuser
