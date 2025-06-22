"""Test User List Access Permissions."""

import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


class TestUserListAccess:
    """Test the user list view access permissions."""

    _TARGET_URL = reverse("dj_users:user_list")

    def test_user_list_access_granted_to_platform_admin(self, client) -> None:
        """Platform Administrator can access user list."""
        # Create a user and add them to the "Platform Administrators" group
        user = get_user_model().objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            password="admin_password_123",
        )
        group, _ = Group.objects.get_or_create(name="Platform Administrators")
        user.groups.add(group)

        # Login the user
        client.force_login(user)

        # Send a GET request to the user list URL
        response = client.get(self._TARGET_URL)

        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200
        assert "users" in response.context
        assert response.context["users"] is not None

    def test_user_list_access_granted_to_superuser(self, client) -> None:
        """Superuser can access user list."""
        # Create a superuser
        user = get_user_model().objects.create_superuser(
            username="superuser@example.com",
            email="superuser@example.com",
            password="super_password_123",
        )

        # Login the user
        client.force_login(user)

        # Send a GET request to the user list URL
        response = client.get(self._TARGET_URL)

        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200
        assert "users" in response.context
        assert response.context["users"] is not None

    def test_user_list_access_denied_to_regular_user(self, client) -> None:
        """Regular user cannot access user list."""
        # Create a regular user (not in Platform Administrators group)
        user = get_user_model().objects.create_user(
            username="regular@example.com",
            email="regular@example.com",
            password="regular_password_123",
        )

        # Login the user
        client.force_login(user)

        # Send a GET request to the user list URL
        response = client.get(self._TARGET_URL)

        # Assert that the response status code is 403 (Forbidden)
        assert response.status_code == 403

    def test_user_list_access_denied_to_unauthenticated_user(self, client) -> None:
        """Unauthenticated user cannot access user list."""
        # Send a GET request to the user list URL without logging in
        response = client.get(self._TARGET_URL)

        # Assert that the response status code is 302 (redirect to login page)
        assert response.status_code == 302
        assert response.url.startswith(reverse("account_login"))

    def test_user_list_displays_users_for_authorized_user(self, client) -> None:
        """User list displays all users for authorized users."""
        # Create multiple test users
        regular_user = get_user_model().objects.create_user(
            username="user1@example.com",
            email="user1@example.com",
            password="password_123",
        )
        another_user = get_user_model().objects.create_user(
            username="user2@example.com",
            email="user2@example.com",
            password="password_456",
        )

        # Create an admin user
        admin_user = get_user_model().objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            password="admin_password_123",
        )
        group, _ = Group.objects.get_or_create(name="Platform Administrators")
        admin_user.groups.add(group)

        # Login as admin
        client.force_login(admin_user)

        # Send a GET request to the user list URL
        response = client.get(self._TARGET_URL)

        # Assert successful response
        assert response.status_code == 200

        # Check that all users are displayed
        user_emails = [user.email for user in response.context["users"]]
        assert regular_user.email in user_emails
        assert another_user.email in user_emails
        assert admin_user.email in user_emails

    def test_user_list_pagination_works(self, client) -> None:
        """User list pagination works correctly."""
        # Create an admin user
        admin_user = get_user_model().objects.create_user(
            username="admin@example.com",
            email="admin@example.com",
            password="admin_password_123",
        )
        group, _ = Group.objects.get_or_create(name="Platform Administrators")
        admin_user.groups.add(group)

        # Login as admin
        client.force_login(admin_user)

        # Send a GET request to the user list URL
        response = client.get(self._TARGET_URL)

        # Assert successful response
        assert response.status_code == 200

        # Check pagination context exists
        assert "page_obj" in response.context
        assert hasattr(response.context["page_obj"], "has_other_pages")
