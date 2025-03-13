import json
import uuid

from django_celery_beat.models import ClockedSchedule, PeriodicTask


def schedule_one_off(trigger):
    clocked, _ = ClockedSchedule.objects.get_or_create(
        clocked_time=trigger.scheduled_at
    )
    PeriodicTask.objects.create(
        clocked=clocked,
        name=f"run {trigger.name} {uuid.uuid4()}",
        task="core.tasks.trigger_one_off",
        one_off=True,
        args=json.dumps(
            [
                trigger.id,
            ]
        ),
    )


# def schedule_periodic(trigger: ScheduleTrigger):


def execute():
    from core.models import OneTimeTrigger
    from core.schedule import schedule_one_off

    tg = OneTimeTrigger.objects.first()
    from datetime import timedelta

    from django.utils import timezone

    tg.scheduled_at = timezone.now() + timedelta(seconds=10)
    schedule_one_off(tg)
    print(tg.scheduled_at)
