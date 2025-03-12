from django.db import models


class TriggerType(models.TextChoices):
    API = "API"
    SCHEDULED = "SCHEDULED"


class Trigger(models.Model):
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=16, choices=TriggerType.choices)
    created_at = models.DateTimeField(auto_now_add=True)


class EventLog(models.Model):
    trigger = models.ForeignKey(
        Trigger,
        null=True,
        blank=True,
        on_delete=models.SET_NULL  # TODO: Maybe, move to a ghost trigger?
    )
    triggered_at = models.DateTimeField(auto_now_add=True)
    is_test = models.BooleanField(default=False)
    payload = models.JSONField()
