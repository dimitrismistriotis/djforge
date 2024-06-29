"""Test User Login functionality."""

import pytest
from django.contrib.auth import get_user_model

pytestmark = [pytest.mark.django_db]


# noinspection HardcodedPassword
class UserLoginLogoutBase:
    """Base Class to test login and logout of users."""

    USER_MODEL = get_user_model()

    USERNAME = "testuser"
    USER_EMAIL = "test_user@provided.com"
    PASSWORD = "testpassword123"

    @pytest.fixture(autouse=True)
    def setup_method(self, db) -> None:
        """Set up a user for testing login."""
        # Set up a user for testing login
        self.USER_MODEL.objects.create_user(
            self.USERNAME, self.USER_EMAIL, self.PASSWORD
        )

    class Meta:
        """Meta class to define abstract model."""

        abstract = True
