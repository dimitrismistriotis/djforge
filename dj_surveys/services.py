"""Service helpers for the dj_surveys app."""

from django import forms
from django.db import transaction
from django.urls import reverse

from dj_surveys.forms import SurveyVoteForm
from dj_surveys.models import Survey
from dj_surveys.models import SurveyChoice
from dj_surveys.models import SurveyQuestion
from dj_surveys.models import SurveyVote


def get_survey_for_user(user) -> Survey | None:
    """Return the next survey pending the user's response."""
    return Survey.objects.visible_to(user).prefetch_related("questions__choices").first()


def build_question_vote_forms(survey, data=None) -> list[dict[str, object]]:
    """Build one vote form per question with a unique HTML field prefix."""
    question_forms = []
    questions = survey.questions.all().order_by("order", "id")

    for question in questions:
        question_forms.append(
            {
                "question": question,
                "form": SurveyVoteForm(
                    data=data,
                    survey=survey,
                    question=question,
                    prefix=f"question_{question.id}",
                ),
            }
        )

    return question_forms


def build_pending_context(
    user,
    *,
    survey: Survey | None = None,
    question_forms: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    """Build context for the pending-survey view."""
    survey = survey or get_survey_for_user(user)
    if survey is None:
        return {"survey": None}

    return {
        "survey": survey,
        "question_forms": question_forms or build_question_vote_forms(survey),
        "survey_submit_url": reverse(
            "dj_surveys:pending_submit",
            kwargs={"survey_id": survey.id},
        ),
        "survey_skip_url": reverse(
            "dj_surveys:pending_skip",
            kwargs={"survey_id": survey.id},
        ),
    }


def save_survey_votes(
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
