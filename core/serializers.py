import jsonschema
from django.utils import timezone
from rest_framework import serializers
from rest_framework.reverse import reverse

from core.models import APITrigger, EventLog, OneTimeTrigger, RecurringTrigger


class EventLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventLog
        fields = [
            "id",
            "is_archived",
            "is_test",
            "payload",
            "triggered_at",
            "trigger_name",
            "triggered_via",
            "url",
        ]


class APITriggerReadSerializer(serializers.HyperlinkedModelSerializer):
    trigger_url = serializers.SerializerMethodField()

    class Meta:
        model = APITrigger
        fields = [
            "id",
            "created_at",
            "is_test",
            "name",
            "schema",
            "trigger_url",
            "url",
        ]

    def get_trigger_url(self, data):
        return reverse(
            "apitrigger-trigger",
            args=[data.id],
            request=self.context.get("request"),
        )


class APITriggerSerializer(serializers.ModelSerializer):

    payload = serializers.JSONField()

    class Meta:
        model = APITrigger
        fields = ["payload"]

    def validate(self, data):
        trigger = self.instance
        try:
            jsonschema.validate(instance=data["payload"], schema=trigger.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"payload": f"Invalid payload: {e.message}"}
            )
        return data


class OneTimeTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneTimeTrigger
        fields = [
            "created_at",
            "id",
            "is_test",
            "name",
            "scheduled_at",
            "url",
        ]

    def validate(self, data):
        scheduled_at = data.get("scheduled_at")
        if scheduled_at < timezone.now():
            raise serializers.ValidationError(
                {"scheduled_at": "Scheduled time cannot be in the future."}
            )
        return data


class RecurringTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTrigger
        fields = [
            "id",
            "created_at",
            "is_test",
            "name",
            "cron_expression",
            "url",
        ]
