"""Views for Dj Users."""

from django.http import HttpResponse, HttpResponseForbidden, HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .utilities import is_member


@login_required
def admin_account(request: HttpRequest) -> HttpResponse:
    """Return the account details of the dj_content app."""
    user = request.user
    if user.is_authenticated and is_member(user, "admin_group"):
        return render(request, "dj_users/admin_account.html")
    return HttpResponseForbidden("Need admin group permission to access this page.")


@login_required
def user_account(request: HttpRequest) -> HttpResponse:
    """Return the account details of the dj_content app."""
    user = request.user
    if user.is_authenticated and is_member(user, "user_group"):
        return render(request, "dj_users/user_account.html")
    return HttpResponseForbidden("Need user group permission to access this page.")
