import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "triggery.settings")

from celery import Celery
from celery.schedules import crontab

app = Celery("triggery")


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    "purge-event-logs-every-5-mins": {
        "task": "core.tasks.purge_event_logs",
        "schedule": crontab(minute="*/5"),
    }
}
