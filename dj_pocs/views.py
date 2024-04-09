"""Views for the dj_pocs app."""

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext as _

#
# Data sourced from https://www.doogal.co.uk/UKPostcodes?Search=NG10
# and ChatGPT for demand
#
POST_CODE_SAMPLE_DATA = [
    {
        "post_code": "NG10 1AA",
        "latitude": 52.897228,
        "longitude": -1.272167,
        "demand": 15,
    },
    {
        "post_code": "NG10 1AB",
        "latitude": 52.887565,
        "longitude": -1.275499,
        "demand": 16,
    },
    {
        "post_code": "NG10 1AD",
        "latitude": 52.888628,
        "longitude": -1.277339,
        "demand": 18,
    },
    {
        "post_code": "NG10 1AE",
        "latitude": 52.887459,
        "longitude": -1.277255,
        "demand": 19,
    },
    {
        "post_code": "NG10 1AF",
        "latitude": 52.886726,
        "longitude": -1.274993,
        "demand": 17,
    },
    {
        "post_code": "NG10 1AG",
        "latitude": 52.88806,
        "longitude": -1.278434,
        "demand": 10,
    },
    {
        "post_code": "NG10 1AH",
        "latitude": 52.886334,
        "longitude": -1.278448,
        "demand": 13,
    },
    {
        "post_code": "NG10 1AJ",
        "latitude": 52.886429,
        "longitude": -1.277852,
        "demand": 13,
    },
    {
        "post_code": "NG10 1AL",
        "latitude": 52.885908,
        "longitude": -1.277875,
        "demand": 12,
    },
    {
        "post_code": "NG10 1AN",
        "latitude": 52.885659,
        "longitude": -1.279871,
        "demand": 15,
    },
    {
        "post_code": "NG10 1AP",
        "latitude": 52.887616,
        "longitude": -1.280819,
        "demand": 16,
    },
    {
        "post_code": "NG10 1AQ",
        "latitude": 52.887015,
        "longitude": -1.27961,
        "demand": 14,
    },
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
