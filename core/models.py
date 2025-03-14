from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class TriggerType(models.TextChoices):
    API = "API"
    SCHEDULED = "SCHEDULED"


class Trigger(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    is_test = models.BooleanField(default=False)

    def execute(self, payload=None):
        # TODO: Introduce `run_async` as an argument to
        # determine whether this needs to run in the same
        # thread, or go via the queueing system.
        if isinstance(self, APITrigger):
            triggered_via = TriggerType.API
            if payload is None:
                raise ValueError("'payload' cannot be None")
        else:
            triggered_via = TriggerType.SCHEDULED

        EventLog.objects.create(
            is_test=self.is_test,
            payload=payload,
            trigger=self,
            triggered_via=triggered_via,
            trigger_name=self.name,
        )


class APITrigger(Trigger):
    schema = models.JSONField(null=False)


class OneTimeTrigger(Trigger):
    scheduled_at = models.DateTimeField(null=False)


class RecurringTrigger(Trigger):
    cron_expression = models.CharField(
        max_length=128,
        null=False,
        help_text="Cron format: */5 * * * * (Please look at: https://crontab.guru for generating Cron Expressions.)",
    )


class EventLog(models.Model):
    is_archived = models.BooleanField(default=False)
    is_test = models.BooleanField(default=False)
    payload = models.JSONField(null=True)
    content_type = models.ForeignKey(
        ContentType, null=True, blank=True, on_delete=models.SET_NULL
    )
    object_id = models.PositiveIntegerField()
    trigger = GenericForeignKey("content_type", "object_id")
    triggered_at = models.DateTimeField(auto_now_add=True)
    trigger_name = models.CharField(max_length=128)
    triggered_via = models.CharField(max_length=16, choices=TriggerType.choices)
