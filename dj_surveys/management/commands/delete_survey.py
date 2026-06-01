from typing import Any

import questionary

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from dj_surveys.models import Survey


class Command(BaseCommand):
    """Management command to delete a survey and all associated data."""

    help = "Delete a survey and all its associated questions, choices, and votes"

    def add_arguments(self, parser: Any) -> None:
        """Add command arguments."""
        parser.add_argument(
            "--id",
            type=int,
            dest="survey_id",
            help="The ID of the survey to delete (skip interactive selection)",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the command."""
        survey_id = options.get("survey_id")

        if survey_id:
            try:
                survey = Survey.objects.get(id=survey_id)
            except Survey.DoesNotExist as exception:
                raise CommandError(
                    f"Survey with ID {survey_id} does not exist"
                ) from exception
        else:
            survey = self._select_survey_interactive()
            if not survey:
                return

        # Gather statistics
        questions_count = survey.questions.count()
        choices_count = 0
        votes_count = survey.votes.count()

        for question in survey.questions.all():
            choices_count += question.choices.count()

        # Display warning
        self._show_deletion_warning(survey, questions_count, choices_count, votes_count)

        # Request confirmation
        try:
            user_input = input(
                f"\nType the survey title '{survey.title}' to confirm deletion: "
            ).strip()
        except KeyboardInterrupt, EOFError:
            self.stdout.write(self.style.WARNING("\n\nOperation cancelled."))
            return

        # Validate confirmation
        if user_input != survey.title:
            self.stdout.write(
                self.style.ERROR(
                    f"\n✗ Confirmation mismatch. Entered: '{user_input}', Expected: '{survey.title}'"
                )
            )
            self.stdout.write(self.style.WARNING("Deletion cancelled."))
            return

        # Execute deletion
        self._delete_survey(survey, questions_count, choices_count, votes_count)

    def _select_survey_interactive(self) -> Survey | None:
        """Interactively select a survey from the database using questionary.

        Returns the selected survey or None if cancelled.
        """
        surveys = Survey.objects.all().order_by("id")

        if not surveys.exists():
            self.stdout.write(self.style.WARNING("No surveys found in the database."))
            return None

        choices = [f"{survey.title} (ID: {survey.id})" for survey in surveys]
        choices.append("Cancel")

        try:
            selected = questionary.select(
                "Select a survey to delete:",
                choices=choices,
                use_search_filter=True,
                use_jk_keys=False,
                instruction="(Type to filter, arrow keys to move)",
            ).ask()
        except KeyboardInterrupt, EOFError:
            self.stdout.write(self.style.WARNING("\n\nOperation cancelled."))
            return None

        if not selected or selected == "Cancel":
            self.stdout.write(self.style.WARNING("Operation cancelled."))
            return None

        survey_id = int(selected.split("(ID: ")[-1].rstrip(")"))
        return surveys.get(id=survey_id)

    def _show_deletion_warning(
        self,
        survey: Survey,
        questions_count: int,
        choices_count: int,
        votes_count: int,
    ) -> None:
        """Display warning about what will be deleted."""
        self.stdout.write(self.style.WARNING("\n" + "=" * 60))
        self.stdout.write(self.style.WARNING("WARNING: PERMANENT DELETION"))
        self.stdout.write(self.style.WARNING("=" * 60))
        self.stdout.write(
            self.style.WARNING("\nYou are about to delete the following:")
        )
        self.stdout.write(
            self.style.WARNING(f"\nSurvey:       {survey.title} (ID: {survey.id})")
        )
        self.stdout.write(self.style.WARNING(f"Questions:    {questions_count}"))
        self.stdout.write(self.style.WARNING(f"Choices:      {choices_count}"))
        self.stdout.write(self.style.WARNING(f"Votes:        {votes_count}"))
        self.stdout.write(
            self.style.WARNING(
                "\nThis action CANNOT be undone. All data associated with this survey will be permanently deleted."
            )
        )
        self.stdout.write(self.style.WARNING("=" * 60))

    def _delete_survey(
        self,
        survey: Survey,
        questions_count: int,
        choices_count: int,
        votes_count: int,
    ) -> None:
        """Delete survey and all associated data."""
        try:
            survey_title = survey.title
            survey_id = survey.id
            survey.delete()

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✓ Survey successfully deleted: {survey_title} (ID: {survey_id})"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(f"✓ Deleted {questions_count} question(s)")
            )
            self.stdout.write(
                self.style.SUCCESS(f"✓ Deleted {choices_count} choice(s)")
            )
            self.stdout.write(self.style.SUCCESS(f"✓ Deleted {votes_count} vote(s)"))
            self.stdout.write(
                self.style.SUCCESS("\n✓ Deletion completed successfully!\n")
            )

        except Exception as exception:
            raise CommandError(
                f"Failed to delete survey: {str(exception)}"
            ) from exception
