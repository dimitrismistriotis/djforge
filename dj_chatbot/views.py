"""Views for the Django Chatbot application."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import ChatMessageForm


@login_required
def chat(request):
    """Chat view for authenticated users."""
    chat_messages = []
    form = ChatMessageForm()

    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            user_message = form.cleaned_data["message"]

            # Add user message to chat
            chat_messages.append(
                {
                    "sender": "user",
                    "message": user_message,
                    "sender_name": request.user.get_full_name()
                    or request.user.username,
                }
            )

            # Add bot response
            chat_messages.append(
                {
                    "sender": "bot",
                    "message": f"You wrote: {user_message}",
                    "sender_name": "Chatbot",
                }
            )

            # Reset form for new message
            form = ChatMessageForm()

    context = {
        "form": form,
        "chat_messages": chat_messages,
    }

    return render(request, "dj_chatbot/chat.html", context)
