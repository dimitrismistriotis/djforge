"""Test Contact Us View."""
import pytest

from django.urls import reverse
from django.core import mail

from ..models import ContactForm

pytestmark = [pytest.mark.django_db]


class TestContactView:
    """Test Contact Us View."""

    def test_contact_view_get(self, client) -> None:
        """Test dropped from synthetic, in progress."""
        url = reverse("contact")
        response = client.get(url)
        assert response.status_code == 200

    def test_contact_view_post_valid_data(self, client) -> None:
        """Test dropped from synthetic, in progress."""
        url = reverse("contact")
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Hello, I have a question.",
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse("contact")
        assert ContactForm.objects.count() == 1
        assert len(mail.outbox) == 2  # One email to the user, one to the admin

    def test_contact_view_post_invalid_data(self, client) -> None:
        """Test dropped from synthetic, in progress."""
        url = reverse("contact")
        data = {"name": "", "email": "invalid-email", "message": ""}
        response = client.post(url, data)
        assert response.status_code == 200
        assert ContactForm.objects.count() == 0
        assert len(mail.outbox) == 0
