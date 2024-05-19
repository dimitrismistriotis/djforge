"""Test Contact Us View."""
import pytest

from django.urls import reverse
from django.core import mail
from django.test import Client
from django.test import override_settings

from ..models import ContactUsEntry

pytestmark = [pytest.mark.django_db]


class TestContactView:
    """Test Contact Us View."""

    TARGET_URL = reverse("dj_contact_us:contact-us")

    _CORRECT_QUERY_DATA = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, I have a question.",
    }

    _INVALID_QUERY_DATA = {  # Invalid data
        "name": "",
        "email": "invalid-email",
        "message": "",
    }

    @override_settings(DISPATCHING_EMAILS=False)  # Does not matter for this test
    def test_contact_view_get(self, client: Client) -> None:
        """Test dropped from synthetic, in progress."""
        response = client.get(self.TARGET_URL)

        assert response.status_code == 200

    @override_settings(DISPATCHING_EMAILS=False)  # Does not matter for this test
    def test_contact_view_post_valid_data(self, client: Client) -> None:
        """Test dropped from synthetic, in progress."""
        response = client.post(self.TARGET_URL, self._CORRECT_QUERY_DATA)

        assert response.status_code == 302
        assert response.url == self.TARGET_URL
        assert ContactUsEntry.objects.count() == 1

    @override_settings(DISPATCHING_EMAILS=False)  # Does not matter for this test
    def test_contact_view_post_invalid_data(self, client: Client) -> None:
        """Test dropped from synthetic, in progress."""
        data = {"name": "", "email": "invalid-email", "message": ""}

        response = client.post(self.TARGET_URL, data)

        assert response.status_code == 200
        assert ContactUsEntry.objects.count() == 0
        # assert len(mail.outbox) == 0

    @override_settings(DISPATCHING_EMAILS=True)
    def test_email_sent(self, client: Client) -> None:
        """Test that an email is sent when the view is called."""
        client.post(self.TARGET_URL, self._CORRECT_QUERY_DATA)

        # assert len(mail.outbox) == 2  # One email to the user, one to the admin
        assert mail.outbox[0].subject == "New Contact Form Submission"
        assert (
            self._CORRECT_QUERY_DATA["email"] in mail.outbox[0].to
        )  # Check if the recipient is correct

    @override_settings(DISPATCHING_EMAILS=True)
    def test_no_email_sent_with_invalid_data(self, client: Client) -> None:
        """Test that no email is sent when invalid data is provided."""
        client.post(self.TARGET_URL, self._INVALID_QUERY_DATA)

        assert len(mail.outbox) == 0  # Check that no email was sent
