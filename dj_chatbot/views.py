"""Views for the Django Chatbot application."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render

from .forms import ChatMessageForm

# Maximum number of messages to keep in cache
MAX_MESSAGES = 10


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
                    f"Chat history cleared. You can have up to {MAX_MESSAGES} messages in your chat history.",
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

                # Add bot response
                chat_messages.append(
                    {
                        "sender": "bot",
                        "message": f"You wrote: {user_message}",
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
