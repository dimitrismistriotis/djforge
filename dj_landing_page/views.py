"""Views for dj_landing_page app."""
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse


def index_page(request: HttpRequest) -> HttpResponse:
    """Index page."""
    return render(request, "dj_landing_page/index.html")
