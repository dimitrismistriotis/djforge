"""Views for dj_content app."""

from pathlib import Path

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from .utilities import read_file_into_array

_LICENSE_FILE = Path(__file__).parent.parent / "License.md"


def about_us(request: HttpRequest) -> HttpResponse:
    """Return a about_us for the dj_content app."""
    return render(
        request,
        "dj_content/about_us.html",
    )


def cookies_policy(request: HttpRequest) -> HttpResponse:
    """Return Cookies Policy Document."""
    return render(
        request,
        "dj_content/cookies_policy.html",
    )


def health(_request: HttpRequest) -> HttpResponse:
    """Return a health for the dj_content app."""
    return HttpResponse("OK")


def license(request: HttpRequest) -> HttpResponse:
    """Return the license of the dj_content app from License.md."""
    # Below removes markdown header:
    license_lines = [
        line for line in read_file_into_array(_LICENSE_FILE) if not line.startswith("#")
    ]
    # Remove first empty line if there, as it was to space out the header:
    if not license_lines[0]:
        license_lines.pop(0)

    return render(
        request,
        "dj_content/license.html",
        {
            "license_lines": license_lines,
        },
    )
