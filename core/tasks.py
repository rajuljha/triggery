from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from core.models import OneTimeTrigger, EventLog


def exec_trigger(trigger, *args, **kwargs):
    trigger.execute(*args, **kwargs)

    if trigger.is_test:
        trigger.delete()


@shared_task
def trigger_one_off(trigger_id):
    try:
        trigger = OneTimeTrigger.objects.get(id=trigger_id)
    except OneTimeTrigger.DoesNotExist:
        print(f"No such trigger id exists: {trigger_id}")
        return

    exec_trigger(trigger)


@shared_task
def purge_event_logs():
    now = timezone.now()
    archived_count = EventLog.objects.filter(
        is_archived=False, triggered_at__lt=now - timedelta(hours=2)
    ).update(is_archived=True)

    delete_count, _ = EventLog.objects.filter(
        triggered_at__lt=now - timedelta(hours=48)
    ).delete()
    print(f"Archived: {archived_count}, Deleted: {delete_count}")
    return
