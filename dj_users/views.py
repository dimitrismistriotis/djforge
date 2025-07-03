"""Views for the dj_users app."""

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import User
from .permissions import restrict_to_platform_admin_404


@login_required
@restrict_to_platform_admin_404
def user_list(request):
    """List all users with pagination and impersonation links.

    Only accessible by Platform Administrators or superusers.
    """
    users = User.objects.all().order_by("email")

    paginator = Paginator(users, 25)  # Show 25 users per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "users": page_obj,
    }

    return render(request, "dj_users/user_list.html", context)
