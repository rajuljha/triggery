from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from core.models import APITrigger, EventLog, OneTimeTrigger
from core.schedule import schedule_one_off
from core.serializers import (
    APITriggerReadSerializer,
    APITriggerSerializer,
    EventLogSerializer,
    OneTimeTriggerSerializer,
)
from core.tasks import exec_trigger


class EventLogViewSet(viewsets.ModelViewSet):
    queryset = EventLog.objects.all().order_by("-id")
    serializer_class = EventLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]


class APITriggerViewSet(viewsets.ModelViewSet):
    queryset = APITrigger.objects.filter(is_test=False).order_by("-id")
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "trigger" and self.request.method == "POST":
            return APITriggerSerializer
        return APITriggerReadSerializer

    def create(self, request):
        serializer = APITriggerReadSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"])
    def trigger(self, request, pk):
        try:
            trigger = APITrigger.objects.get(pk=pk)
        except APITrigger.DoesNotExist:
            raise NotFound(f"No Trigger exists with id={pk}")

        if request.method == "POST":
            exec_trigger(trigger, payload=request.data.get("payload"))
            return Response({"status": "ok"})

        return Response(
            APITriggerReadSerializer(trigger, context={"request": request}).data
        )


class OneTimeTriggerViewSet(viewsets.ModelViewSet):
    queryset = OneTimeTrigger.objects.filter(is_test=False).order_by("-id")
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OneTimeTriggerSerializer

    def create(self, request):
        serializer = OneTimeTriggerSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        trigger = serializer.save()

        schedule_one_off(trigger)
        return Response(serializer.data)
