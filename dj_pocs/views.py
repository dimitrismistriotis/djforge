"""Views for the dj_pocs app."""

from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render


def map_and_postcode_analysis(request: HttpRequest) -> HttpResponse:
    """Display a map and a table with postcode analysis."""
    return render(request, "dj_pocs/map.html")
