"""Forms for the Django Chatbot application."""

from django import forms


class ChatMessageForm(forms.Form):
    """Form for submitting chat messages."""

    message = forms.CharField(
        max_length=1000,
        widget=forms.TextInput(
            attrs={
                "class": "flex-1 p-2 border border-gray-300 rounded-lg dark:bg-gray-600 dark:border-gray-500 dark:text-white",
                "placeholder": "Type your message here...",
                "id": "message-input",
            }
        ),
        strip=True,
    )
