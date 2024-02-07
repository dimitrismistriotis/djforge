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
