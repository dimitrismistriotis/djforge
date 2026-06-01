"""URL configuration for dj_surveys app."""

from django.urls import path

from dj_surveys import views

app_name = "dj_surveys"

urlpatterns = [
    path(
        "pending",
        views.pending_survey,
        name="pending",
    ),
    path(
        "<int:survey_id>/submit",
        views.submit_pending_vote,
        name="pending_submit",
    ),
    path(
        "<int:survey_id>/skip",
        views.skip_pending_survey,
        name="pending_skip",
    ),
]
