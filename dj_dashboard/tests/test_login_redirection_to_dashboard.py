"""Test Login Redirects Users to Dashboard."""

import pytest

from django.urls import reverse

pytestmark = [pytest.mark.django_db]


class TestLoginRedirectionToDashboard:
    """Test Login Redirects Users to Dashboard."""

    LOGIN_URL = reverse("account_login")
    DASHBOARD_URL = reverse("dj_dashboard:dashboard")

    # noinspection HardcodedPassword
    def test_login_redirects_to_dashboard_on_success(self, client, regular_user):
        """Test that a user with correct password is redirected to "/dashboard"."""
        response = client.post(
            self.LOGIN_URL,
            {
                "login": regular_user.email,
                "password": "correct_password_for_person",
            },
            follow=True,
        )

        # Check if the response redirected to dashboard URL.
        assert response.status_code == 200
        assert response.request["PATH_INFO"] == self.DASHBOARD_URL

    # noinspection HardcodedPassword
    def test_login_stays_on_login_screen_on_failure(self, client, regular_user):
        """Test that a user with incorrect password stays on the login screen."""
        response = client.post(
            self.LOGIN_URL,
            {
                "login": regular_user.email,
                "password": "wrong_password",
            },
        )

        # Check if the response did not redirect, implying stay on login screen.
        assert (
            response.status_code == 200
        )  # Assuming your login view returns 200 even on failed auth
        assert "not correct" in response.content.decode()

    def test_dashboard_access_requires_login(self, client):
        """Test that accessing the dashboard requires user to be logged in."""
        response = client.get(self.DASHBOARD_URL)

        # Assuming your app redirects unauthorized users to the login page
        assert response.status_code in [302, 403]  # 302 for redirect, 403 for Forbidden
        if response.status_code == 302:
            # Check if the response redirected to the login page.
            # Note: This assertion depends on your login flow. Some apps might redirect to a different URL.
            assert self.LOGIN_URL in response.url
