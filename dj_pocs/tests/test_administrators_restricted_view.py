"""Test View Restricted Only to Users who Belong to Administrators Group."""
import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from django.contrib.auth import get_user_model

pytestmark = [pytest.mark.django_db]


class TestAdministratorsRestrictedView:
    """Test the restricted view for "Platform Administrators" group."""

    _TARGET_URL = reverse("dj_pocs:admin_only_display")

    def test_restricted_view_access_granted(self, client) -> None:
        """User belonging to the "Platform Administrators" group can access view."""
        # Create a user and add them to the "Platform Administrators" group
        user = get_user_model().objects.create_user(
            username="person@example.com",
            email="person@example.com",
            password="correct_password_for_person",
        )
        group = Group.objects.get(name="Platform Administrators")
        user.groups.add(group)

        # Login the user
        client.force_login(user)

        # Send a GET request to the restricted view URL
        response = client.get(self._TARGET_URL)

        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200

    def test_restricted_view_access_denied(self, client) -> None:
        """User not belonging to the "Platform Administrators" group cannot access."""
        # Create a user not belonging to the "Platform Administrators" group
        user = get_user_model().objects.create_user(
            username="person@example.com",
            email="person@example.com",
            password="correct_password_for_person",
        )

        # Login the user
        client.force_login(user)

        # Send a GET request to the restricted view URL
        response = client.get(self._TARGET_URL)

        # Assert that the response status code is 302 (redirect to login page)
        assert response.status_code == 302
        assert response.url.startswith(reverse("login"))

    def test_no_access_for_not_logged_in_users(self, client) -> None:
        """Cannot access without Login."""
        # Send a GET request to the restricted view URL
        response = client.get(self._TARGET_URL)

        # Assert that the response status code is 302 (redirect to login page)
        assert response.status_code == 302
        assert response.url.startswith(reverse("login"))
