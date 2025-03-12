from rest_framework import serializers
from rest_framework.reverse import reverse

from core.models import EventLog, Trigger


class EventLogSerializer(serializers.HyperlinkedModelSerializer):
    trigger_name = serializers.SerializerMethodField()

    class Meta:
        model = EventLog
        fields = [
            'type',
            'trigger_name',
            'triggered_at',
            'is_test',
            'payload',
        ]

    def get_trigger_name(self, data):
        if data.trigger:
            return data.trigger.name


class TriggerSerializer(serializers.HyperlinkedModelSerializer):
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
        return reverse("triggers-trigger", args=[data.id], request=self.context.get('request'))
