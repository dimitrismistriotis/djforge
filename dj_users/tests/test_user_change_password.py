"""Tests for the user change password view from Allauth."""

import pytest

from django.urls import reverse
from django.test import Client


from .base_classes import UserLoginLogoutBase


pytestmark = [pytest.mark.django_db]


# noinspection HardcodedPassword
class TestUserChangePassword(UserLoginLogoutBase):
    """Test User Change Password functionality."""

    TARGET_URL = reverse("account_change_password")

    def test_view_is_accessible_with_get(self, client: Client) -> None:
        """Check that logged in user can access the view."""
        client.login(username=self.USER_EMAIL, password=self.PASSWORD)

        response = client.get(self.TARGET_URL)
        assert response.status_code == 200
        assert "Change Password" in str(response.content)

    def test_change_password_view(self, client: Client) -> None:
        """Correctly change password for a user."""
        client.login(username=self.USER_EMAIL, password=self.PASSWORD)

        # Test POST request to change password
        new_password: str = "NewP4ssword12!"
        response = client.post(
            reverse("account_change_password"),
            {
                "oldpassword": self.PASSWORD,
                "password1": new_password,
                "password2": new_password,
            },
        )

        assert response.status_code == 302
        #
        # This was initial synthetic test's code, with the current setup, user gets
        # redirected to the same page. Keep it in comments as it seems a better idea
        # to take them there in the future.
        #
        # assert response.url == reverse("account_change_password_done")
        assert response.url == self.TARGET_URL

    def test_user_can_log_in_with_changed_password(self, client: Client) -> None:
        """Once password is changed, user can log in with new password."""
        client.login(username=self.USER_EMAIL, password=self.PASSWORD)

        # Test POST request to change password
        new_password: str = "NewP4ssword12!"
        client.post(
            reverse("account_change_password"),
            {
                "oldpassword": self.PASSWORD,
                "password1": new_password,
                "password2": new_password,
            },
        )

        # Logout and login with new password
        client.logout()

        assert client.login(username=self.USER_EMAIL, password=new_password)

    def test_change_password_with_current_password_wrong(self, client: Client) -> None:
        """Do not change password with current password wrong."""
        client.login(username=self.USER_EMAIL, password=self.PASSWORD)

        # Issue POST request with wrong current password:
        response = client.post(
            self.TARGET_URL,
            {
                "oldpassword": "wrong_testpass",
                "password1": "differentpass",
                "password2": "differentpass",
            },
        )

        assert response.status_code == 200
        assert "Please type your current password" in str(response.content)

    def test_change_password_with_mismatched_new_passwords(
        self, client: Client
    ) -> None:
        """Do not change password if password 1 and 2 do not match."""
        client.login(username=self.USER_EMAIL, password=self.PASSWORD)

        # Issue POST request with mismatched new passwords:
        response = client.post(
            self.TARGET_URL,
            {
                "oldpassword": self.PASSWORD,
                "password1": "NewP4ssword12!",
                "password2": "NewP4ssword12!-with-more-stuff",
            },
        )

        assert response.status_code == 200
        assert "You must type the same password each time" in str(response.content)
