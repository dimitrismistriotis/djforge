"""Views for the dj_pocs app."""

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext as _

POST_CODE_SAMPLE_DATA = [
    {"post_code": "NG1", "demand": 15},
    {"post_code": "NG2", "demand": 16},
    {"post_code": "NG3", "demand": 18},
    {"post_code": "NG4", "demand": 18},
    {"post_code": "NG5", "demand": 19},
    {"post_code": "NG6", "demand": 17},
    {"post_code": "NG7", "demand": 10},
    {"post_code": "NG8", "demand": 13},
    {"post_code": "NG9", "demand": 13},
    {"post_code": "NG10", "demand": 12},
    {"post_code": "NG11", "demand": 15},
    {"post_code": "NG12", "demand": 13},
    {"post_code": "NG13", "demand": 15},
    {"post_code": "NG14", "demand": 15},
    {"post_code": "NG15", "demand": 16},
    {"post_code": "NG16", "demand": 14},
    {"post_code": "NG17", "demand": 12},
    {"post_code": "NG18", "demand": 20},
    {"post_code": "NG19", "demand": 18},
    {"post_code": "NG20", "demand": 16},
]


def map_and_postcode_analysis(request: HttpRequest) -> HttpResponse:
    """Display a map and a table with postcode analysis."""
    if not (google_maps_api_key := getattr(settings, "GOOGLE_MAPS_API_KEY", None)):
        messages.error(
            request, _("Google Maps API key is not set, cannot display map.")
        )

    post_code_and_demand = POST_CODE_SAMPLE_DATA  # Will later be ordered/filtered

    return render(
        request,
        "dj_pocs/map.html",
        {
            "google_maps_api_key": google_maps_api_key,
            "post_code_and_demand": post_code_and_demand,
        },
    )
