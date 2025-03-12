from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from core.models import EventLog, Trigger, TriggerType
from core.serializers import EventLogSerializer, TriggerSerializer, TriggerListSerializer


class EventLogViewSet(viewsets.ModelViewSet):
    queryset = EventLog.objects.all().order_by('-id')
    serializer_class = EventLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]


class TriggerViewSet(viewsets.ModelViewSet):
    queryset = Trigger.objects.all().order_by('-id')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "trigger":
            return TriggerSerializer
        return TriggerListSerializer

    def create(self, request):
        if request.data.get("name") is None:
            raise ValidationError("'name' of the trigger was not supplied")
        trigger = Trigger.objects.create(
            name=request.data.get("name"),
            type=TriggerType.API,
        )
        trigger_url = self.reverse_action(self.trigger.url_name, args=[trigger.id])
        data = {"trigger_url": trigger_url}
        return Response(data)

    @action(detail=True, methods=['post'])
    def trigger(self, request, pk):
        try:
            trigger = Trigger.objects.get(pk=pk)
        except Trigger.DoesNotExist:
            raise NotFound(f"No Trigger exists with id={pk}")
        trigger.execute(payload=request.data)
        return Response({"status": "ok"})
