from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class SurveyQuerySet(models.QuerySet):
    """QuerySet for Survey model."""

    pass


class Survey(models.Model):
    """
    Container for a poll or survey.

    A survey is the top-level object that contains questions and tracks votes.
    Once created, surveys are immutable (no editing).
    """

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(
        max_length=255,
        help_text="Title of the survey displayed to users.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    objects = SurveyQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class SurveyQuestionQuerySet(models.QuerySet):
    """QuerySet for SurveyQuestion model."""

    pass


class SurveyQuestion(models.Model):
    """A question within a survey. Supports multiple questions per survey with display ordering for future iterations."""

    id = models.BigAutoField(primary_key=True)
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name="questions",
        help_text="The survey this question belongs to.",
    )
    text = models.TextField(
        help_text="The question text displayed to users.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order of questions within the survey.",
    )
    question_type = models.CharField(
        max_length=15,
        default="single_choice",
        choices=[
            ("single_choice", "Single Choice"),
            ("multiple_choice", "Multiple Choice"),
        ],
        help_text="single_choice: user selects one option; multiple_choice: user selects one or more options.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    objects = SurveyQuestionQuerySet.as_manager()

    class Meta:
        ordering = ["survey", "order"]

    def __str__(self):
        return f"{self.survey.title}: {self.text}"

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            SurveyChoice.objects.create(
                question=self,
                text="Decline",
                order=999,
                is_decline_option=True,
            )


class SurveyChoiceQuerySet(models.QuerySet):
    """QuerySet for SurveyChoice model."""

    pass


class SurveyChoice(models.Model):
    """
    An answer option for a survey question.

    Choices are displayed in order. Users select choices based on the question_type.
    A choice can be marked as a decline/don't vote option to track user dismissals.
    """

    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(
        SurveyQuestion,
        on_delete=models.CASCADE,
        related_name="choices",
        help_text="The question this choice belongs to.",
    )
    text = models.CharField(
        max_length=255,
        help_text="The choice text displayed to users (e.g., 'Build Tailwind integration').",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order of choices within the question.",
    )
    is_decline_option = models.BooleanField(
        default=False,
        help_text="If true, this choice represents 'I prefer not to answer' or 'Decline'. Used for banner dismissal and question opt-outs.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    objects = SurveyChoiceQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["question"],
                condition=models.Q(is_decline_option=True),
                name="one_decline_choice_per_question",
            ),
            models.CheckConstraint(
                condition=~models.Q(text=""),
                name="choice_text_not_empty",
            ),
        ]
        ordering = ["question", "order"]

    def __str__(self):
        return self.text


class SurveyVoteQuerySet(models.QuerySet):
    """QuerySet for SurveyVote model."""

    pass


class SurveyVote(models.Model):
    """
    A user's vote for a choice on a survey question.

    For single_choice questions: one vote row per user per question (enforced via clean()).
    For multiple_choice questions: multiple vote rows per user per question (one per selected choice).
    Voting on a decline_option choice tracks user dismissals without a separate model.
    """

    id = models.BigAutoField(primary_key=True)
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name="votes",
        help_text="The survey being voted on.",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="survey_votes",
        help_text="The user who cast this vote.",
    )
    question = models.ForeignKey(
        SurveyQuestion,
        on_delete=models.CASCADE,
        related_name="votes",
        null=True,
        blank=True,
        help_text="The question being voted on. Denormalized for efficient querying.",
    )
    choice = models.ForeignKey(
        SurveyChoice,
        on_delete=models.CASCADE,
        related_name="votes",
        help_text="The choice selected by the user.",
    )
    voted_at = models.DateTimeField(auto_now_add=True)
    objects = SurveyVoteQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "choice"],
                name="one_vote_per_user_per_choice",
            ),
        ]
        ordering = ["-voted_at"]

    def __str__(self):
        return f"{self.user.get_username()} voted on {self.survey.title}"

    def clean(self) -> None:
        """Validate vote rules for single-choice and decline choices."""
        super().clean()

        if not self.choice_id or not self.user_id:
            return

        question = self.question or self.choice.question
        if self.question_id and self.choice.question_id != self.question_id:
            raise ValidationError("Choice does not belong to this question.")

        if self.survey_id and self.choice.question.survey_id != self.survey_id:
            raise ValidationError("Choice does not belong to this survey.")

        self.question = question
        existing_votes = SurveyVote.objects.filter(
            user=self.user,
            question=question,
        ).exclude(pk=self.pk)

        if self.choice.is_decline_option:
            if existing_votes.exists():
                raise ValidationError(
                    "Decline cannot be selected with other options."
                )
        elif existing_votes.filter(choice__is_decline_option=True).exists():
            raise ValidationError("Decline cannot be selected with other options.")

        if question.question_type == "single_choice":
            if existing_votes.exists():
                raise ValidationError(
                    f"User has already voted on '{question.text}'. "
                    "Single choice questions only allow one vote per user."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
