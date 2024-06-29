"""Test Content Pages."""

import pytest
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


class TestContentPages:
    """Test Content Pages."""

    @pytest.mark.parametrize(
        "url_name",
        [
            "dj_content:about-us",
            "dj_content:cookies-policy",
            "dj_content:health",
            "dj_content:license",
        ],
    )
    def test_content_page_returns_200(self, client, url_name) -> None:
        """Test page returns a 200 response."""
        response = client.get(reverse(url_name))

        assert response.status_code == 200

    def test_license_page_contains_license(self, client) -> None:
        """Test license page contains the license."""
        response = client.get(reverse("dj_content:license"))

        assert "License" in response.content.decode()
        assert "DJ-FORGE" in response.content.decode()
