"""Tasks from https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html.

Copied from there aiming to test Celery with Django.
"""

from typing import TypeVar

from celery import shared_task

T = TypeVar("T")


@shared_task
def add(x: T, y: T) -> T:
    """Add two numbers.

    Example Execution:

    >>> from dj_tasks.tasks import add
    >>> task_result = add.apply_async((2, 5))

    Then:

    >>> task_result.id
    'b3f1ba36-d69c-470d-870f-62e359c83122'
    >>> task_result.status
    'PENDING'
    >>> task_result.status
    'SUCCESS'
    >>> task_result.result
    7
    """
    return x + y


@shared_task
def mul(x: T, y: T) -> T:
    """Multiply two numbers.

    Example Execution:

    >>> from dj_tasks.tasks import mul
    >>> task_result = mul.apply_async((2, 5))

    Then:

    >>> task_result.id
    '07e845ea-3288-4696-a916-4efd76eb3904'
    >>> task_result.status
    'PENDING'
    >>> task_result.status
    'SUCCESS'
    >>> task_result.result
    10
    """
    return x * y


@shared_task
def xsum(numbers: list[T]) -> T:
    """Sum a list of numbers.

    Example Execution:

    Compared with other tasks above the input is one list of numbers,
    notice the comma after the list. This ensures that the input is a tuple.

    Also we could calculate the sequence below with the Gauss formula, which is
    more efficient but besides the point.

    >>> from dj_tasks.tasks import xsum
    >>> task_result = xsum.apply_async(((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ))

    Then:

    >>> task_result.id
    '06e15531-0ef9-4d4d-b6ed-4d71f7e648b1'
    >>> task_result.status
    'PENDING'
    >>> task_result.status
    'SUCCESS'
    >>> task_result.result
    55
    """
    return sum(numbers)
