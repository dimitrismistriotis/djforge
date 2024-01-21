"""Views for dj_content app."""
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render


def manifest(request: HttpRequest) -> HttpResponse:
    """Return a manifest for the dj_content app."""
    return render(request, "dj_content/manifest.html")
