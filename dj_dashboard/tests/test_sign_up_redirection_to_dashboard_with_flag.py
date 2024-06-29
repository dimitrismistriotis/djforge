"""Test Sign Up Redirects Users to Dashboard with Specific Flag."""

import pytest
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


class TestUserSignupRedirect:
    """Test Sign Up Redirects Users to Dashboard with Specific Flag."""

    SIGNUP_URL = reverse("account_signup")

    # noinspection HardcodedPassword
    def test_signup_redirects_to_dashboard_on_success(self, client):
        """Test that a successful signup redirects the user to "/dashboard?signup"."""
        user_details = {
            "username": "user@example.com",
            "password1": "ReallySecureP4$$word!",
            "password2": "ReallySecureP4$$word!",
            "email": "user@example.com",
        }

        response = client.post(self.SIGNUP_URL, user_details, follow=True)

        # Check if the response redirected to "/dashboard/signup".
        dashboard_url_post_sign_up = reverse("dj_dashboard:dashboard_post_sign_up")
        assert response.status_code == 200

        assert response.request["PATH_INFO"] == dashboard_url_post_sign_up

        assert response.context["user"].is_authenticated
