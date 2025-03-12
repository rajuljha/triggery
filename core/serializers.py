from rest_framework import serializers
from rest_framework.reverse import reverse

from core.models import EventLog, Trigger


class EventLogSerializer(serializers.HyperlinkedModelSerializer):
    trigger_name = serializers.SerializerMethodField()
    triggered_via = serializers.SerializerMethodField()

    class Meta:
        model = EventLog
        fields = [
            'is_test',
            'payload',
            'triggered_at',
            'trigger_name',
            'triggered_via',
        ]

    def get_trigger_name(self, data):
        if data.trigger:
            return data.trigger.name

    def get_triggered_via(self, data):
        return data.trigger.type


class TriggerListSerializer(serializers.HyperlinkedModelSerializer):
    trigger_url = serializers.SerializerMethodField()

    class Meta:
        model = Trigger
        fields = [
            "id",
            "created_at",
            "name",
            "trigger_url",
            "type",
        ]

    def get_trigger_url(self, data):
        return reverse(
            "triggers-trigger",
            args=[data.id],
            request=self.context.get('request'),
        )

class TriggerSerializer(serializers.ModelSerializer):

    payload = serializers.JSONField()

    class Meta:
        model = Trigger
        fields = ['payload']
