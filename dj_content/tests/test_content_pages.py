"""Test Content Pages."""

import pytest

from django.urls import reverse

pytestmark = [pytest.mark.django_db]


class TestContentPages:
    """Test Content Pages."""

    def test_homepage_returns_200(self, client) -> None:
        """Test that health page returns a 200 response."""
        response = client.get(reverse("dj_content:health"))
        assert response.status_code == 200

    def test_about_page_returns_200(self, client) -> None:
        """Test that "About Us" page returns a 200 response."""
        response = client.get(reverse("dj_content:about-us"))
        assert response.status_code == 200
