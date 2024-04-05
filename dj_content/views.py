"""Views for dj_content app."""

from pathlib import Path

from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render

from .utilities import read_file_into_array


_LICENSE_FILE = Path(__file__).parent.parent / "License.md"


def about_us(request: HttpRequest) -> HttpResponse:
    """Return a about_us for the dj_content app."""
    return render(request, "dj_content/about_us.html")


def health(_request: HttpRequest) -> HttpResponse:
    """Return a health for the dj_content app."""
    return HttpResponse("OK")


def license(request: HttpRequest) -> HttpResponse:
    """Return the license of the dj_content app from License.md."""
    license_lines = read_file_into_array(_LICENSE_FILE)

    return render(request, "dj_content/license.html", {"license_lines": license_lines})
