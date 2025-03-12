from django.db import models
from django.utils import timezone


class TriggerType(models.TextChoices):
    API = "API"
    SCHEDULED = "SCHEDULED"


class Trigger(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=16, choices=TriggerType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def execute(self, payload=None, is_test=False):
        # TODO: Introduce `run_async` as an argument to
        # determine whether this needs to run in the same
        # thread, or go via the queueing system.
        EventLog.objects.create(
            trigger=self,
            triggered_at=timezone.now(),
            is_test=is_test,
            payload=payload
        )


class EventLog(models.Model):
    trigger = models.ForeignKey(
        Trigger,
        null=True,
        blank=True,
        on_delete=models.SET_NULL  # TODO: Maybe, move to a ghost trigger?
    )
    triggered_at = models.DateTimeField(auto_now_add=True)
    is_test = models.BooleanField(default=False)
    payload = models.JSONField(null=True)
