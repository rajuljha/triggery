from rest_framework import serializers

from core.models import EventLog


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
