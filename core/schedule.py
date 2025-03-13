import json
import uuid

from django_celery_beat.models import ClockedSchedule, CrontabSchedule, PeriodicTask


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


def schedule_recurring(trigger):
    cron_parts = trigger.cron_expression.split(" ")
    if len(cron_parts) != 5:
        raise ValueError("Invalid cron expression format. Expected 5 parts.")
    minute, hour, day_of_month, month, day_of_week = cron_parts
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=minute,
        hour=hour,
        day_of_month=day_of_month,
        month_of_year=month,
        day_of_week=day_of_week,
    )
    one_off = False
    if trigger.is_test:
        one_off = True
    PeriodicTask.objects.create(
        crontab=schedule,
        one_off=one_off,
        name=f"Trigger: {trigger.name} {uuid.uuid4()}",
        task="core.tasks.trigger_recurring",
        args=json.dumps([trigger.id]),
        enabled=True,
    )


def execute():
    from core.models import OneTimeTrigger
    from core.schedule import schedule_one_off

    tg = OneTimeTrigger.objects.first()
    from datetime import timedelta

    from django.utils import timezone

    tg.scheduled_at = timezone.now() + timedelta(seconds=10)
    schedule_one_off(tg)
    print(tg.scheduled_at)
