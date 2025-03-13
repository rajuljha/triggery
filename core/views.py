import jsonschema
from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response

from core.filters import EventLogFilter
from core.models import APITrigger, EventLog, OneTimeTrigger, RecurringTrigger
from core.schedule import schedule_one_off, schedule_recurring
from core.serializers import (
    APITriggerReadSerializer,
    APITriggerSerializer,
    EventLogSerializer,
    OneTimeTriggerSerializer,
    RecurringTriggerSerializer,
)
from core.tasks import exec_trigger


class RawInputRenderer(BrowsableAPIRenderer):
    """
    Custom renderer which overrides the standard DRF Browsable API
    to disable the "HTML" tab.
    """

    def get_context(self, *args, **kwargs):
        context = super(RawInputRenderer, self).get_context(*args, **kwargs)

        context["post_form"] = None
        context["put_form"] = None
        return context


class EventLogViewSet(viewsets.ModelViewSet):
    queryset = EventLog.objects.all().order_by("-id")
    serializer_class = EventLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventLogFilter
    http_method_names = ["get"]


class APITriggerViewSet(viewsets.ModelViewSet):
    queryset = APITrigger.objects.filter(is_test=False).order_by("-id")
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "trigger" and self.request.method == "POST":
            return APITriggerSerializer
        return APITriggerReadSerializer

    def get_renderers(self):
        if self.action == "trigger":
            return [RawInputRenderer()]
        return super(APITriggerViewSet, self).get_renderers()

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
            serializer = APITriggerSerializer(instance=trigger, data=request.data)
            serializer.is_valid(raise_exception=True)
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


class RecurringTriggerViewSet(viewsets.ModelViewSet):
    queryset = RecurringTrigger.objects.filter(is_test=False).order_by("-id")
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecurringTriggerSerializer

    def create(self, request):
        serializer = RecurringTriggerSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        trigger = serializer.save()
        schedule_recurring(trigger)
        return Response(serializer.data)
