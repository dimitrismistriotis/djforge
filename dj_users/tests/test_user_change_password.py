"""Tests for the user change password view from Allauth."""

import pytest

from django.urls import reverse
from django.test import Client

from ..models import User

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user() -> User:
    """Fixture for user, should be placed in conftest.py."""
    return User.objects.create_user(username="testuser", password="testpass")


def test_change_password_view(user: User) -> None:
    """Correctly change password for a user."""
    client: Client = Client()
    client.login(username="testuser", password="testpass")

    # Test GET request to change password page
    response = client.get(reverse("account_change_password"))
    assert response.status_code == 200
    assert "Change Password" in str(response.content)

    # Test POST request to change password
    new_password: str = "newpassword"
    response = client.post(
        reverse("account_change_password"),
        {
            "oldpassword": "testpass",
            "password1": new_password,
            "password2": new_password,
        },
    )
    assert response.status_code == 302
    assert response.url == reverse("account_change_password_done")

    # Logout and login with new password
    client.logout()
    client.login(username="testuser", password=new_password)
    assert client.session.get("_auth_user_id") == str(user.id)


def test_change_password_with_invalid_data(user: User) -> None:
    """Do not change password with current password wrong."""
    client: Client = Client()
    client.login(username="testuser", password="testpass")

    # Test POST request with mismatched passwords
    response = client.post(
        reverse("account_change_password"),
        {
            "oldpassword": "wrong_testpass",
            "password1": "differentpass",
            "password2": "differentpass",
        },
    )
    assert response.status_code == 200
    assert "The two password fields didn&#39;t match." in str(response.content)

    # Test POST request with incorrect old password
    response = client.post(
        reverse("account_change_password"),
        {"oldpassword": "wrongpass", "password1": "newpass", "password2": "newpass"},
    )
    assert response.status_code == 200
    assert "Your current password was entered incorrectly." in str(response.content)


def test_change_password_with_mismatched_new_passwords(user: User) -> None:
    """Do not change password if password 1 and 2 do not match."""
    client: Client = Client()
    client.login(username="testuser", password="testpass")

    # Test POST request with mismatched new passwords
    response = client.post(
        reverse("account_change_password"),
        {"oldpassword": "testpass", "password1": "newpass1", "password2": "newpass2"},
    )
    assert response.status_code == 200
    assert "The two password fields didn&#39;t match." in str(response.content)
