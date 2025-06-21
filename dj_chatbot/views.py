"""Views for the Django Chatbot application."""

import logging

import anthropic

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render

from .forms import ChatMessageForm

logger = logging.getLogger(__name__)

# Maximum number of messages to keep in cache
MAX_MESSAGES = 10


def get_ai_response(user_message: str) -> str:
    """Generate AI response using Anthropic's Claude if an API key is available."""
    if not settings.ANTHROPIC_API_KEY:
        return f"You wrote: {user_message}"

    try:
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        # Use Claude 3 Haiku, its least expensive model for proof of concept
        response = client.messages.create(
            model=getattr(
                settings, "CLAUDE_MODEL_FOR_CHAT", "claude-3-5-haiku-20241022"
            ),
            max_tokens=1000,
            messages=[{"role": "user", "content": user_message}],
        )

        return response.content[0].text
    except Exception as exception:
        logger.error("Error generating AI response:")
        logger.exception(exception)
        return f"Sorry, I encountered an error processing your message. You wrote: {user_message}"


@login_required
def chat(request):
    """Chat view for authenticated users."""
    cache_key = f"chat_messages_{request.user.id}"
    chat_messages = cache.get(cache_key, [])
    form = ChatMessageForm()

    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            user_message = form.cleaned_data["message"]

            # Handle /clear command
            if user_message.strip() == "/clear":
                cache.delete(cache_key)
                chat_messages = []
                messages.success(
                    request,
                    "Chat history cleared.",
                )
                form = ChatMessageForm()
            else:
                # Add the user message to chat
                chat_messages.append(
                    {
                        "sender": "user",
                        "message": user_message,
                        "sender_name": request.user.get_full_name()
                        or request.user.username,
                    }
                )

                # Add bot response using AI if available
                bot_response = get_ai_response(user_message)
                chat_messages.append(
                    {
                        "sender": "bot",
                        "message": bot_response,
                        "sender_name": "Chatbot",
                    }
                )

                # Keep only the last MAX_MESSAGES
                if len(chat_messages) > MAX_MESSAGES:
                    chat_messages = chat_messages[-MAX_MESSAGES:]

                # Save to cache
                cache.set(cache_key, chat_messages)

                # Reset form for a new message
                form = ChatMessageForm()

    context = {
        "form": form,
        "chat_messages": chat_messages,
        "max_messages": MAX_MESSAGES,
    }

    return render(request, "dj_chatbot/chat.html", context)
