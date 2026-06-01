from typing import Any

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from dj_surveys.models import Survey
from dj_surveys.models import SurveyChoice
from dj_surveys.models import SurveyQuestion


class Command(BaseCommand):
    """Management command to create surveys with multiple questions and choices."""

    help = "Create a survey with multiple questions and answer choices (interactive)"

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the command."""
        self.stdout.write(self.style.HTTP_INFO("\n=== Create Survey ===\n"))

        # Prompt for survey title
        while True:
            title = self._prompt("Survey Title")
            if not title:
                self.stdout.write(self.style.ERROR("Survey title cannot be empty"))
                continue
            break

        # Collect questions
        questions = []
        question_order = 1

        while True:
            self.stdout.write(
                self.style.HTTP_INFO(f"\n--- Question {question_order} ---")
            )

            # Prompt for question text
            question_text = self._prompt("Question Text")
            if not question_text:
                self.stdout.write(self.style.ERROR("Question text cannot be empty"))
                continue

            # Prompt for question type
            self.stdout.write("Question Type options: single_choice, multiple_choice")
            question_type = self._prompt("Question Type", default="single_choice")
            if question_type not in ["single_choice", "multiple_choice"]:
                self.stdout.write(
                    self.style.ERROR(f"Invalid question type: {question_type}")
                )
                continue

            # Collect choices
            choices_list = []
            choice_order = 1
            while True:
                choice_text = self._prompt(f"Choice #{choice_order}")
                if not choice_text:
                    if not choices_list:
                        self.stdout.write(
                            self.style.ERROR("At least one choice must be provided")
                        )
                        continue
                    break

                choices_list.append(choice_text)
                add_another = self._prompt("Add another choice? (y/N)").lower()
                if add_another != "y":
                    break
                choice_order += 1

            # Show confirmation for this question
            self._show_question_confirmation(
                question_order, question_text, choices_list, question_type
            )

            # Confirm this question
            confirm = self._prompt("Add this question? (y/N)").lower()
            if confirm == "y":
                questions.append(
                    {
                        "text": question_text,
                        "choices": choices_list,
                        "type": question_type,
                    }
                )
                question_order += 1

                # Ask if user wants to add another question
                add_another = self._prompt("Add another question? (y/N)").lower()
                if add_another != "y":
                    break
            # If user didn't confirm, loop to re-enter this question

        if not questions:
            self.stdout.write(
                self.style.WARNING("No questions added. Survey creation cancelled.")
            )
            return

        # Show final survey confirmation
        self._show_survey_confirmation(title, questions)

        # Final confirmation
        confirm = self._prompt("Create survey with these questions? (y/N)").lower()
        if confirm != "y":
            self.stdout.write(self.style.WARNING("Survey creation cancelled."))
            return

        # Create the survey and questions
        self._create_survey(title, questions)

    def _prompt(self, prompt_text: str, default: str = "") -> str:
        """Prompt user for input with optional default."""
        if default:
            prompt_display = f"{prompt_text} [{default}]: "
        else:
            prompt_display = f"{prompt_text}: "

        response = input(prompt_display).strip()
        return response if response else default

    def _show_question_confirmation(
        self,
        question_order: int,
        question_text: str,
        choices_list: list[str],
        question_type: str,
    ) -> None:
        """Display a single question's details for confirmation."""
        self.stdout.write(
            self.style.HTTP_INFO(f"\n--- Question {question_order} Details ---")
        )
        self.stdout.write(f"Text: {question_text}")
        self.stdout.write(f"Type: {question_type}")
        self.stdout.write("Choices:")
        for index, choice in enumerate(choices_list, start=1):
            self.stdout.write(f"  {index}. {choice}")
        self.stdout.write("")

    def _show_survey_confirmation(
        self,
        title: str,
        questions: list[dict[str, Any]],
    ) -> None:
        """Display full survey with all questions for final confirmation."""
        self.stdout.write(self.style.HTTP_INFO("\n=== Survey Summary ==="))
        self.stdout.write(f"Title: {title}")
        self.stdout.write(f"Total Questions: {len(questions)}\n")

        for question_order, question in enumerate(questions, start=1):
            self.stdout.write(f"Question {question_order}: {question['text']}")
            self.stdout.write(f"  Type: {question['type']}")
            self.stdout.write("  Choices:")
            for choice_order, choice in enumerate(question["choices"], start=1):
                self.stdout.write(f"    {choice_order}. {choice}")
            self.stdout.write("")

    def _create_survey(
        self,
        title: str,
        questions: list[dict[str, Any]],
    ) -> None:
        """Create survey, questions, and choices in the database."""
        try:
            # Create survey
            survey = Survey.objects.create(title=title)
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Created survey: {survey.title} (ID: {survey.id})"
                )
            )

            # Create questions and choices
            for question_order, question_data in enumerate(questions, start=1):
                question = SurveyQuestion.objects.create(
                    survey=survey,
                    text=question_data["text"],
                    order=question_order,
                    question_type=question_data["type"],
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Created question {question_order}: {question.text}"
                    )
                )

                # Create choices for this question
                for choice_order, choice_text in enumerate(
                    question_data["choices"], start=1
                ):
                    choice = SurveyChoice.objects.create(
                        question=question,
                        text=choice_text,
                        order=choice_order,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  ✓ Added choice #{choice_order}: {choice.text}"
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✓ Survey created successfully with {len(questions)} question(s)! "
                    f"Survey ID: {survey.id}\n"
                )
            )

        except Exception as exception:
            raise CommandError(
                f"Failed to create survey: {str(exception)}"
            ) from exception
