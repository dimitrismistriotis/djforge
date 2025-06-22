"""URL patterns for the dj_users app."""

from django.urls import path

from .views import user_list

app_name = "dj_users"

urlpatterns = [
    path("list", user_list, name="user_list"),
]
