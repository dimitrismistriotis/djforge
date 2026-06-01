"""Views for the dj_surveys app."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods

from dj_surveys.models import Survey
from dj_surveys.models import SurveyChoice
from dj_surveys.models import SurveyVote
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
    """Redirect to the dashboard, where pending surveys are now surfaced.

    The standalone survey page was a temporary placeholder; surveys now appear
    as a banner on the dashboard. This route is retained because the submit,
    skip, and decline views fall back to it when a survey is unavailable.
    """
    return redirect("dj_dashboard:dashboard")


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
    except IntegrityError, ValidationError:
        messages.error(request, "Your vote could not be saved. Please try again.")
        return redirect(_resolve_next(request))

    return redirect(_resolve_next(request))


@login_required
@require_http_methods(["POST"])
def skip_pending_survey(
    request: HttpRequest,
    survey_id: int,
) -> HttpResponse:
    """Ephemerally dismiss a survey for this page load only.

    No vote is recorded, so the survey reappears on the next load. Redirecting
    (rather than rendering) means no-JS users land back on the embedding page
    instead of a blank standalone modal. The JS ``dismissSurvey`` enhancement
    removes the card client-side without this round-trip.
    """
    survey = Survey.objects.visible_to(request.user).filter(id=survey_id).first()
    if survey is None:
        messages.error(request, "Survey is no longer available.")
        return redirect("dj_surveys:pending")

    return redirect(_resolve_next(request))


@login_required
@require_http_methods(["POST"])
def decline_pending_survey(
    request: HttpRequest,
    survey_id: int,
) -> HttpResponse:
    """Persistently opt the user out of a survey by recording a decline vote.

    Records a vote on each question's decline choice so that
    ``Survey.objects.visible_to(user)`` (which excludes ``votes__user=user``)
    hides the survey on every subsequent load.
    """
    survey = Survey.objects.visible_to(request.user).filter(id=survey_id).first()
    if survey is None:
        messages.error(request, "Survey is no longer available.")
        return redirect("dj_surveys:pending")

    decline_choices = SurveyChoice.objects.filter(
        question__survey=survey,
        is_decline_option=True,
    )
    for choice in decline_choices:
        # Each insert runs in its own savepoint, mirroring save_survey_votes:
        # a concurrent duplicate decline races into the unique constraint and is
        # swallowed as an idempotent "already declined" rather than a 500.
        try:
            with transaction.atomic():
                SurveyVote(
                    survey=survey,
                    user=request.user,
                    choice=choice,
                    question=choice.question,
                ).save()
        except IntegrityError:
            continue

    return redirect(_resolve_next(request))
