"""Test User Login functionality."""

import pytest
from django.urls import reverse

from .base_classes import UserLoginLogoutBase

pytestmark = [pytest.mark.django_db]


class TestUserLogin(UserLoginLogoutBase):
    """Test login of users."""

    LOGIN_URL = reverse("account_login")

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
