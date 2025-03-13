from celery import shared_task

from core.models import OneTimeTrigger


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
