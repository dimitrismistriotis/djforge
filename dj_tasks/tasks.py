"""Tasks from https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html.

Copied from there aiming to test Celery with Django.
"""
from typing import TypeVar

from celery import shared_task

T = TypeVar("T")


@shared_task
def add(x: T, y: T) -> T:
    """Add two numbers."""
    return x + y


@shared_task
def mul(x: T, y: T) -> T:
    """Multiply two numbers."""
    return x * y


@shared_task
def xsum(numbers: list[T]) -> T:
    """Sum a list of numbers."""
    return sum(numbers)
