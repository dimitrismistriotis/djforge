"""Views for dj_content app."""
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render


def about_us(request: HttpRequest) -> HttpResponse:
    """Return a about_us for the dj_content app."""
    return render(request, "dj_content/about_us.html")


def dashboard_template(request: HttpRequest) -> HttpResponse:
    """Return a Dashboard page, to use in development while integrating."""
    return render(request, "dj_content/dashboard.html")
