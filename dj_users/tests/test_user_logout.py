"""Test User Logout functionality."""
import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model


pytestmark = [pytest.mark.django_db]


# noinspection HardcodedPassword
class TestUserLogout:
    """Test logout of users."""

    USER_MODEL = get_user_model()

    LOGOUT_URL = reverse("account_logout")  # Assuming default allauth URL names

    USERNAME = "testuser"
    USER_EMAIL = "test_user@provided.com"
    PASSWORD = "testpassword123"

    @pytest.fixture(autouse=True)
    def setup_method(self, db) -> None:
        """Set up a user for testing log out."""
        self.USER_MODEL.objects.create_user(
            self.USERNAME, self.USER_EMAIL, self.PASSWORD
        )

    def test_logout(self, client) -> None:
        """Test logout."""
        # First, log the user in
        client.login(username=self.USERNAME, password=self.PASSWORD)

        # Then, logout
        response = client.get(self.LOGOUT_URL, follow=True)

        # Verify that the user has been logged out
        assert not response.context["user"].is_authenticated
        assert response.status_code == 200
        # Update the expected redirect URL based on your application's behavior
