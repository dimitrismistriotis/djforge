"""Views for dj_dashboard app."""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from dj_surveys.services import build_next_survey_card


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Return a Dashboard page, to use in development while integrating."""
    from_sign_up = request.path.endswith("signup")

    context = {
        "from_sign_up": from_sign_up,
        "survey_card": build_next_survey_card(request.user),
    }

    return render(
        request,
        "dj_dashboard/dashboard.html",
        context,
    )
