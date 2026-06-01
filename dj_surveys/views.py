"""Views for the dj_surveys app."""

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from dj_surveys.forms import SurveyVoteForm
from dj_surveys.models import Survey
from dj_surveys.models import SurveyChoice
from dj_surveys.models import SurveyQuestion
from dj_surveys.models import SurveyVote


def _save_survey_votes(
    user,
    survey: Survey,
    form: SurveyVoteForm,
    question: SurveyQuestion | None,
) -> None:
    """Save votes for a submitted survey form."""
    choice_data = form.cleaned_data["choice"]
    is_multiple = isinstance(form.fields["choice"], forms.ModelMultipleChoiceField)
    choice_ids = [choice.id for choice in choice_data] if is_multiple else [choice_data.id]

    with transaction.atomic():
        if question:
            SurveyVote.objects.filter(
                user=user,
                choice__question=question,
            ).delete()

        choices = SurveyChoice.objects.filter(id__in=choice_ids)
        for choice in choices:
            SurveyVote(
                survey=survey,
                user=user,
                choice=choice,
                question=choice.question,
            ).save()


@login_required
@require_http_methods(["POST"])
def submit_survey_vote(request: HttpRequest) -> HttpResponse:
    """Handle survey vote submission.

    Supports both single-choice and multiple-choice questions.
    Uses delete-then-insert pattern to allow vote changes.
    """
    survey_id = request.POST.get("survey_id")
    question_id = request.POST.get("question_id")

    try:
        survey = Survey.objects.get(id=survey_id)
    except (Survey.DoesNotExist, ValueError):
        messages.error(request, "Survey not found.")
        return redirect("dj_dashboard:dashboard")

    question = None
    if question_id:
        try:
            question = SurveyQuestion.objects.get(id=question_id, survey=survey)
        except (SurveyQuestion.DoesNotExist, ValueError):
            messages.error(request, "Question not found.")
            return redirect("dj_dashboard:dashboard")

    form = SurveyVoteForm(survey=survey, question=question, data=request.POST)
    if not form.is_valid():
        messages.error(request, "Invalid selection. Please try again.")
        return redirect("dj_dashboard:dashboard")

    try:
        _save_survey_votes(user=request.user, survey=survey, form=form, question=question)
        messages.success(request, "Your vote has been recorded. Thank you!")
    except (IntegrityError, ValidationError):
        messages.error(request, "Invalid selection. Please try again.")

    return redirect("dj_dashboard:dashboard")


@login_required
@require_http_methods(["POST"])
def skip_survey(request: HttpRequest, survey_id: int) -> HttpResponse:
    """Handle survey skip action."""
    try:
        Survey.objects.get(id=survey_id)
    except Survey.DoesNotExist:
        messages.error(request, "Survey not found.")
        return redirect("dj_dashboard:dashboard")

    messages.info(request, "Survey skipped.")
    return redirect("dj_dashboard:dashboard")
