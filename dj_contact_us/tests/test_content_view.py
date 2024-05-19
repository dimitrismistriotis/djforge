"""Test Contact Us View."""
import pytest

from django.urls import reverse
from django.core import mail

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

    def test_email_sent(self, client, user):
        """Test that an email is sent when the view is called."""
        # Arrange
        client.force_login(user)
        data = {
            # Provide any required data for the view
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Test Subject",
            "message": "Test Message",
        }

        # Act
        response = client.post(reverse("your_app:your_view_name"), data=data)

        # Assert
        assert response.status_code == 200  # Replace with the expected status code
        assert len(mail.outbox) == 1  # Check if one email was sent
        assert mail.outbox[0].subject == data["subject"]  # Check if the subject matches
        assert data["email"] in mail.outbox[0].to  # Check if the recipient is correct

    def test_no_email_sent_with_invalid_data(self, client, user):
        """Test that no email is sent when invalid data is provided."""
        # Arrange
        client.force_login(user)
        data = {
            # Provide invalid data for the view
            "name": "",
            "email": "invalid_email",
            "subject": "",
            "message": "",
        }

        # Act
        response = client.post(reverse("your_app:your_view_name"), data=data)

        # Assert
        assert (
            response.status_code == 400
        )  # Replace with the expected status code for invalid data
        assert len(mail.outbox) == 0  # Check that no email was sent
