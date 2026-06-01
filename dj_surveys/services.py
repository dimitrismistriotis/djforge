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
    return get_surveys_for_user(user).first()


def get_surveys_for_user(user):
    """Return all surveys pending the user's response."""
    return Survey.objects.visible_to(user).prefetch_related("questions__choices")


def build_question_vote_forms(survey, data=None) -> list[dict[str, object]]:
    """Build one vote form per question with a unique HTML field prefix."""
    question_forms = []
    questions = survey.questions.all().order_by("order", "id")

    for question in questions:
        decline_choice_id = (
            question.choices.filter(is_decline_option=True)
            .values_list("id", flat=True)
            .first()
        )
        question_forms.append(
            {
                "question": question,
                "form": SurveyVoteForm(
                    data=data,
                    survey=survey,
                    question=question,
                    prefix=f"question_{question.id}",
                ),
                "decline_choice_id": decline_choice_id,
            }
        )

    return question_forms


def build_survey_card_context(
    survey: Survey,
    *,
    question_forms: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    """Build template context for a single survey card."""
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


def build_survey_cards(user) -> list[dict[str, object]]:
    """Build template context for every survey pending the user's response."""
    return [build_survey_card_context(survey) for survey in get_surveys_for_user(user)]


def build_next_survey_card(user) -> dict[str, object] | None:
    """Build template context for the single next survey pending the user's response."""
    survey = get_survey_for_user(user)
    if survey is None:
        return None

    return build_survey_card_context(survey)


def build_pending_context(
    user,
    *,
    survey: Survey | None = None,
    question_forms: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    """Build context for the standalone pending-survey view (single survey)."""
    survey = survey or get_survey_for_user(user)
    if survey is None:
        return {"survey": None}

    return build_survey_card_context(survey, question_forms=question_forms)


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
