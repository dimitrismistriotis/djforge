"""Test the register interest view."""
import pytest
from django.shortcuts import reverse
from django.test.client import Client

pytestmark = [pytest.mark.django_db]


class TestRegisterInterestView:
    """Tests for the register interest view."""

    _TARGET_URL = reverse("dj_register_interest:register_interest")

    def test_interest_view_get(self, client: Client) -> None:
        """Test GET method of view."""
        response = client.get(self._TARGET_URL)

        assert response.status_code == 200
        assert "form" in response.context

    def test_interest_view_post_valid_data(self, client: Client) -> None:
        """Test POST of a form with valid data."""
        form_data = {
            "name": "Alice",
            "email": "alice@example.com",
            "github_handle": "alice123",
            "user_intent": "I want to test the solution",
        }
        response = client.post(self._TARGET_URL, form_data)

        # Assuming you redirect to a success page on valid data
        assert response.status_code == 302

    def test_interest_view_post_invalid_data(self, client: Client) -> None:
        """Test POST of a form with invalid data."""
        form_data = {}  # Invalid data
        response = client.post(self._TARGET_URL, form_data)

        assert response.status_code == 200  # Stays on the same page due to form errors
