"""Views for dj_theme app."""
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse


def mesages_demo(request: HttpRequest) -> HttpResponse:
    """Display different messages to demonstrate their UI."""
    return render(request, "dj_theme/demo_display_messages.html")
