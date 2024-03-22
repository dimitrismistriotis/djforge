"""Celery configuration for the project.

https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html

... where requested to create a file within the module named celery.py and confgure
the Celery app there.
"""

import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djforge.settings")

app = Celery("proj")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps:
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task to print request information.

    >>> from djforge.celery import debug_task
    >>> task_result = debug_task.apply_async()

    Then:

    >>> task_result.id
    '1320d679-6e99-4dad-a958-92bf02857646'

    >>> task_result.status
    'PENDING'

    Result status will be always PENDING because ignore_result=True.
    """
    print(f"Request: {self.request!r}")
