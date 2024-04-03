"""Views for dj_content app."""

from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render


def about_us(request: HttpRequest) -> HttpResponse:
    """Return a about_us for the dj_content app."""
    return render(request, "dj_content/about_us.html")


def health(_request: HttpRequest) -> HttpResponse:
    """Return a health for the dj_content app."""
    return HttpResponse("OK")


def license(request: HttpRequest) -> HttpResponse:
    """Return the license of the dj_content app from License.md."""
    return render(request, "dj_content/license.html")
