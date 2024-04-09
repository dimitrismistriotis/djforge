"""Views for the dj_pocs app."""

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext as _


def map_and_postcode_analysis(request: HttpRequest) -> HttpResponse:
    """Display a map and a table with postcode analysis."""
    if not (google_maps_api_key := getattr(settings, "GOOGLE_MAPS_API_KEY", None)):
        messages.error(
            request, _("Google Maps API key is not set, cannot display map.")
        )

    return render(
        request, "dj_pocs/map.html", {google_maps_api_key: google_maps_api_key}
    )
