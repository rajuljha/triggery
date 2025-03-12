from django.db import models


class Trigger(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)


class EventLogType(models.TextChoices):
    API = "API"
    SCHEDULED = "SCHEDULED"


class EventLog(models.Model):

    trigger = models.ForeignKey(
        Trigger,
        null=True,
        blank=True,
        # todo (on deletion, set all event triggers to a single trigger which
        # is a 'ghost')
        on_delete=models.SET_NULL
    )
    type = models.CharField(max_length=16, choices=EventLogType.choices)
    triggered_at = models.DateTimeField(auto_now_add=True)
    is_test = models.BooleanField(default=False)
    payload = models.JSONField()

