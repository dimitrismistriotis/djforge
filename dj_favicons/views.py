"""Views for the dj_favicons app."""
from pathlib import Path

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import FileResponse
from django.shortcuts import render

_FAVICON_LOCATION = Path(__file__).parent / "static" / "dj_favicons" / "favicon.ico"


def favicon(_request: HttpRequest) -> FileResponse:
    """Return a favicon.ico file.

    Follows approach discussed here: https://stackoverflow.com/a/65990187/1622
    """
    return FileResponse(_FAVICON_LOCATION.open("rb"))


def manifest_dot_json(request: HttpRequest) -> HttpResponse:
    """Return manifest.json file pointing to proper icon locations

    Reference: https://developer.mozilla.org/en-US/docs/Web/Manifest
    """
    return render(request, "dj_favicons/manifest.json", content_type="application/json")
