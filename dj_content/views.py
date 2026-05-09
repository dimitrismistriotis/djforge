"""Views for dj_content app."""

from pathlib import Path

from django.db import transaction
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .utilities import read_file_into_array

_LICENSE_FILE = Path(__file__).parent.parent / "License.md"

_ROBOTS_CONTENT_URL_NAMES = (
    "dj_content:about-us",
    "dj_content:cookies-policy",
    "dj_content:license",
)

_ROBOTS_DISALLOWED_PATHS = (
    "/accounts/",
    "/admin/",
    "/chat/",
    "/dashboard/",
    "/impersonate/",
    "/users/",
)


@transaction.non_atomic_requests
def about_us(request: HttpRequest) -> HttpResponse:
    """Return a about_us for the dj_content app."""
    return render(
        request,
        "dj_content/about_us.html",
    )


@transaction.non_atomic_requests
def cookies_policy(request: HttpRequest) -> HttpResponse:
    """Return Cookies Policy Document."""
    return render(
        request,
        "dj_content/cookies_policy.html",
    )


@transaction.non_atomic_requests
def health(_request: HttpRequest) -> HttpResponse:
    """Return a health for the dj_content app."""
    return HttpResponse("OK")


@transaction.non_atomic_requests
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


@transaction.non_atomic_requests
def robots_txt(_request: HttpRequest) -> HttpResponse:
    """Return robots.txt advertising public content pages and disallowing auth-only paths."""
    lines = ["User-agent: *"]
    for disallowed_path in _ROBOTS_DISALLOWED_PATHS:
        lines.append(f"Disallow: {disallowed_path}")
    for url_name in _ROBOTS_CONTENT_URL_NAMES:
        lines.append(f"Allow: {reverse(url_name)}")

    return HttpResponse(
        "\n".join(lines) + "\n",
        content_type="text/plain",
    )
