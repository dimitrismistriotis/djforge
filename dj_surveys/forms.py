"""Forms for the dj_surveys app."""

from django import forms

from dj_surveys.models import SurveyChoice


class SurveyVoteForm(forms.Form):
    """Form for submitting a vote on a survey question."""

    choice = forms.ModelChoiceField(
        queryset=SurveyChoice.objects.all(),
        widget=forms.RadioSelect(attrs={"class": "radio radio-sm radio-primary"}),
        empty_label=None,
        label="",
    )

    def __init__(self, *args, question=None, **kwargs):
        """Initialize form with choices filtered by question.

        Args:
            question: SurveyQuestion instance to filter choices by and determine widget type
        """
        super().__init__(*args, **kwargs)

        if question:
            # Voting on a specific question — widget depends on question type
            choices_queryset = SurveyChoice.objects.filter(question=question)

            if question.question_type == "multiple_choice":
                self.fields["choice"] = forms.ModelMultipleChoiceField(
                    queryset=choices_queryset,
                    widget=forms.CheckboxSelectMultiple(
                        attrs={"class": "checkbox checkbox-sm checkbox-primary"},
                    ),
                    label="",
                )
            else:
                self.fields["choice"].queryset = choices_queryset

    def clean_choice(self):
        """Prevent combining Decline with other multiple-choice options."""
        choice_data = self.cleaned_data["choice"]

        if isinstance(self.fields["choice"], forms.ModelMultipleChoiceField):
            selected_choices = list(choice_data)
            decline_is_selected = any(
                choice.is_decline_option for choice in selected_choices
            )
            if decline_is_selected and len(selected_choices) > 1:
                raise forms.ValidationError(
                    "Decline cannot be selected with other options."
                )

        return choice_data
