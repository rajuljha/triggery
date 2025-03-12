from django.shortcuts import render
from rest_framework import permissions, viewsets

from core.models import EventLog, Trigger
from core.serializers import EventLogSerializer


class EventLogViewSet(viewsets.ModelViewSet):
    queryset = EventLog.objects.all().order_by('-id')
    serializer_class = EventLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get"]
