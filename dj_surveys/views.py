"""Views for the dj_surveys app."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods

from dj_surveys.models import Survey
from dj_surveys.services import build_pending_context
from dj_surveys.services import build_question_vote_forms
from dj_surveys.services import save_survey_votes


def _resolve_next(request: HttpRequest) -> str:
    """Return a safe redirect target, falling back to the pending view.

    Lets an embedding page (e.g. the dashboard) submit a `next` field so the
    user returns to where the survey was shown instead of the standalone page.
    """
    next_url = request.POST.get("next", "")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url

    return reverse("dj_surveys:pending")


@login_required
def pending_survey(request: HttpRequest) -> HttpResponse:
    """Render the next survey pending the user's response."""
    return render(
        request,
        "dj_surveys/modal.html",
        build_pending_context(request.user),
    )


@login_required
@require_http_methods(["POST"])
def submit_pending_vote(
    request: HttpRequest,
    survey_id: int,
) -> HttpResponse:
    """Handle survey vote submission from the pending-survey view."""
    survey = Survey.objects.visible_to(request.user).filter(id=survey_id).first()
    if survey is None:
        messages.error(request, "Survey is no longer available.")
        return redirect("dj_surveys:pending")

    question_forms = build_question_vote_forms(survey, data=request.POST)
    forms_are_valid = [
        question_form["form"].is_valid() for question_form in question_forms
    ]
    if not question_forms or not all(forms_are_valid):
        messages.error(request, "Please choose an option before voting.")
        return redirect(_resolve_next(request))

    try:
        with transaction.atomic():
            for question_form in question_forms:
                save_survey_votes(
                    user=request.user,
                    survey=survey,
                    form=question_form["form"],
                    question=question_form["question"],
                )
    except (IntegrityError, ValidationError):
        messages.error(request, "Your vote could not be saved. Please try again.")
        return redirect(_resolve_next(request))

    return redirect(_resolve_next(request))


@login_required
@require_http_methods(["POST"])
def skip_pending_survey(
    request: HttpRequest,
    survey_id: int,
) -> HttpResponse:
    """Handle survey skip from the pending-survey view."""
    survey = Survey.objects.visible_to(request.user).filter(id=survey_id).first()
    if survey is None:
        messages.error(request, "Survey is no longer available.")
        return redirect("dj_surveys:pending")

    return render(request, "dj_surveys/modal.html", {"survey": None})
