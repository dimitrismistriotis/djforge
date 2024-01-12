"""Test for the views of the dj_favicons app."""

from django.test import Client


class TestFaviconViews:
    """Test for the favicon view."""

    def test_favicon(self, client: Client) -> None:
        """Test the favicon view."""
        response = client.get("/favicon.ico")

        assert response.status_code == 200

    def test_manifest_dot_json(self, client: Client) -> None:
        """Test the manifest.json view."""
        response = client.get("/manifest.json")

        assert response.status_code == 200

        content_json = response.json()

        for icon_entry in content_json.get("icons"):
            print(f"{icon_entry=}")
            icon_location = icon_entry.get("src")

            response_icon = client.get(icon_location)

            assert response_icon.status_code == 200
