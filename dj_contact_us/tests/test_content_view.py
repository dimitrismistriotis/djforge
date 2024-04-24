"""Test Contact Us View."""
import pytest

from django.urls import reverse
# from django.core import mail

from ..models import ContactUsEntry

pytestmark = [pytest.mark.django_db]


class TestContactView:
    """Test Contact Us View."""

    TARGET_URL = reverse("dj_contact_us:contact-us")

    def test_contact_view_get(self, client) -> None:
        """Test dropped from synthetic, in progress."""
        response = client.get(self.TARGET_URL)
        assert response.status_code == 200

    def test_contact_view_post_valid_data(self, client) -> None:
        """Test dropped from synthetic, in progress."""
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Hello, I have a question.",
        }

        response = client.post(self.TARGET_URL, data)

        assert response.status_code == 302
        assert response.url == self.TARGET_URL
        assert ContactUsEntry.objects.count() == 1
        # assert len(mail.outbox) == 2  # One email to the user, one to the admin

    def test_contact_view_post_invalid_data(self, client) -> None:
        """Test dropped from synthetic, in progress."""
        data = {"name": "", "email": "invalid-email", "message": ""}

        response = client.post(self.TARGET_URL, data)

        assert response.status_code == 200
        assert ContactUsEntry.objects.count() == 0
        # assert len(mail.outbox) == 0
