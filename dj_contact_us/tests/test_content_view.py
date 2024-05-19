"""Test Contact Us View."""
import pytest

from django.urls import reverse
from django.core import mail

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

    def test_contact_view_get(self, client) -> None:
        """Test dropped from synthetic, in progress."""
        response = client.get(self.TARGET_URL)

        assert response.status_code == 200

    def test_contact_view_post_valid_data(self, client) -> None:
        """Test dropped from synthetic, in progress."""
        response = client.post(self.TARGET_URL, self._CORRECT_QUERY_DATA)

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

    def test_email_sent(self, client) -> None:
        """Test that an email is sent when the view is called."""
        # Arrange

        # Act
        response = client.post(self.TARGET_URL, self._CORRECT_QUERY_DATA)

        # Assert
        assert response.status_code == 200  # Replace with the expected status code
        assert len(mail.outbox) == 1  # Check if one email was sent
        # assert mail.outbox[0].subject == data["subject"]  # Check if the subject matches
        assert (
            self._CORRECT_QUERY_DATA["email"] in mail.outbox[0].to
        )  # Check if the recipient is correct

    def test_no_email_sent_with_invalid_data(self, client) -> None:
        """Test that no email is sent when invalid data is provided."""
        # Arrange

        # Act
        client.post(self.TARGET_URL, self._INVALID_QUERY_DATA)

        # Assert
        assert len(mail.outbox) == 0  # Check that no email was sent
