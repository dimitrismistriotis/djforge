"""Views for dj_register_interest app."""
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .forms import InterestForm


class RegisterInterestView(View):
    """View for registering interest in the project."""

    form_class = InterestForm
    template_name = "dj_register_interest/register_interest.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Get request for the view."""
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect | HttpResponse:
        """Post request for the view."""
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for registering your interest!")

            # Redirect to same page as a "success" page:
            return redirect(reverse("dj_register_interest:register_interest"))

        return render(request, self.template_name, {"form": form})
