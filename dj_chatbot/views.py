"""Views for the Django Chatbot application."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def chat(request):
    """Chat view for authenticated users."""
    return render(request, "dj_chatbot/chat.html")
