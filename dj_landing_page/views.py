"""Views for dj_landing_page app."""

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render


def index_page(request: HttpRequest) -> HttpResponse:
    """Index page."""
    return render(request, "dj_landing_page/index.html")
