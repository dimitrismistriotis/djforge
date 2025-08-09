"""URLs for the Django Chatbot application."""

from django.urls import path

from .views import chat

app_name = "dj_chatbot"


urlpatterns = [
    path(
        "",
        chat,
        name="chat",
    ),
]
