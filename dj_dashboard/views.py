"""Views for dj_dashboard app."""

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render


def dashboard(request: HttpRequest) -> HttpResponse:
    """Return a Dashboard page, to use in development while integrating."""
    return render(request, "dj_dashboard/dashboard.html")
