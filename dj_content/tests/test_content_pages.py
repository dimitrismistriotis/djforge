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


class TestRobotsTxt:
    """Test the robots.txt view."""

    def test_robots_txt_returns_200_text_plain(self, client) -> None:
        """Test robots.txt returns 200 and plain text content type."""
        response = client.get(reverse("robots_txt"))

        assert response.status_code == 200
        assert response["Content-Type"].startswith("text/plain")

    def test_robots_txt_lists_content_pages(self, client) -> None:
        """Test robots.txt advertises public dj_content pages."""
        response = client.get(reverse("robots_txt"))
        body = response.content.decode()

        assert f"Allow: {reverse('dj_content:about-us')}" in body
        assert f"Allow: {reverse('dj_content:cookies-policy')}" in body
        assert f"Allow: {reverse('dj_content:license')}" in body

    def test_robots_txt_disallows_auth_paths(self, client) -> None:
        """Test robots.txt disallows login and authenticated paths."""
        response = client.get(reverse("robots_txt"))
        body = response.content.decode()

        assert "User-agent: *" in body
        assert "Disallow: /accounts/" in body
        assert "Disallow: /admin/" in body
        assert "Disallow: /dashboard/" in body
        assert "Disallow: /users/" in body
        assert "Disallow: /chat/" in body
        assert "Disallow: /impersonate/" in body
