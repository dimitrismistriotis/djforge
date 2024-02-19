"""Test User Login functionality."""
import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model


pytestmark = [pytest.mark.django_db]


# noinspection HardcodedPassword
class TestUserLogin:
    """Test login of users."""

    USER_MODEL = get_user_model()

    LOGIN_URL = reverse("account_login")

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

    def test_successful_login(self, client) -> None:
        """Test a successful login."""
        # Simulate a login attempt with correct credentials
        response = client.post(
            self.LOGIN_URL,
            {
                "login": self.USER_EMAIL,
                "password": self.PASSWORD,
            },
            follow=True,
        )

        # Check if the login was successful and redirected as expected
        assert response.context["user"].is_authenticated
        assert response.status_code == 200
        # Update the expected redirect URL based on your application's behavior

    def test_failed_login(self, client) -> None:
        """Test a failed login."""
        # Simulate a login attempt with incorrect password
        response = client.post(
            self.LOGIN_URL,
            {
                "login": self.USER_EMAIL,
                "password": "wrongpassword",
            },
            follow=True,
        )

        # Check if the login failed and user is not authenticated
        assert not response.context["user"].is_authenticated
        # Additionally, check for error messages or status codes if applicable
        assert "password you specified" in response.content.decode()

    def test_logout(self, client) -> None:
        """Test logout."""
        # First, log the user in
        client.login(username=self.USERNAME, password=self.PASSWORD)

        # Then, logout
        logout_url = reverse("account_logout")  # Assuming default allauth URL names
        response = client.get(logout_url, follow=True)

        # Verify that the user has been logged out
        assert not response.context["user"].is_authenticated
        assert response.status_code == 200
        # Update the expected redirect URL based on your application's behavior
