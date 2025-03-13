from rest_framework import serializers
from rest_framework.reverse import reverse

from core.models import APITrigger, EventLog, OneTimeTrigger


class EventLogSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = EventLog
        fields = [
            'id',
            'is_archived',
            'is_test',
            'payload',
            'triggered_at',
            'trigger_name',
            'triggered_via',
            'url',
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
            # TODO: rename to schema
            "payload",
            "trigger_url",
            "url",
        ]

    def get_trigger_url(self, data):
        return reverse(
            "apitrigger-trigger",
            args=[data.id],
            request=self.context.get('request'),
        )


class APITriggerSerializer(serializers.ModelSerializer):

    # TODO: At the time of trigger, validate that this
    # payload conforms to schema defined for this trigger
    payload = serializers.JSONField()

    class Meta:
        model = APITrigger
        fields = ['payload']


class OneTimeTriggerSerializer(serializers.ModelSerializer):

    # TODO: Validate scheduled_at is in the future
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
