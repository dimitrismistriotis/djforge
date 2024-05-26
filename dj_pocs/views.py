"""Views for the dj_pocs app."""

import json
from functools import reduce
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required


from dj_users.permissions import restrict_to_platform_admin_404


#
# Data sourced from https://www.doogal.co.uk/UKPostcodes?Search=NG10
# and ChatGPT for demand
#
POST_CODE_SAMPLE_DATA = json.loads(
    (Path(__file__).parent / "sample_data" / "post_codes_and_demand.json").read_bytes()
)


@login_required
@restrict_to_platform_admin_404
def admin_only_display(request: HttpRequest) -> HttpResponse:
    """Allow to be seen only from Platform Administrators."""
    return render(request, "dj_pocs/view_for_admin_prermissions.html", {})


def map_and_postcode_analysis(request: HttpRequest) -> HttpResponse:
    """Display a map and a table with postcode analysis."""
    if not (google_maps_api_key := getattr(settings, "GOOGLE_MAPS_API_KEY", None)):
        messages.error(
            request, _("Google Maps API key is not set, cannot display map.")
        )

    post_codes_and_demand = sorted(
        POST_CODE_SAMPLE_DATA, key=lambda x: x["demand"], reverse=True
    )

    approximate_center = reduce(
        lambda acc, post_code: (
            acc[0] + post_code["latitude"],
            acc[1] + post_code["longitude"],
        ),
        post_codes_and_demand,
        (0, 0),
    )
    approximate_center = (
        approximate_center[0] / len(post_codes_and_demand),
        approximate_center[1] / len(post_codes_and_demand),
    )
    approximate_center_dict = {
        "latitude": approximate_center[0],
        "longitude": approximate_center[1],
    }

    return render(
        request,
        "dj_pocs/map.html",
        {
            "google_maps_api_key": google_maps_api_key,
            "post_codes_and_demand": post_codes_and_demand,
            "approximate_center": approximate_center_dict,
        },
    )
