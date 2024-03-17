"""Views for dj_dashboard app."""

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Return a Dashboard page, to use in development while integrating."""
    from_sign_up = request.path.endswith("signup")
    # print(f"{from_sign_up=}")

    return render(
        request,
        "dj_dashboard/dashboard.html",
        {
            "from_sign_up": from_sign_up,
        },
    )
