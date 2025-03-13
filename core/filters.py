from django import forms
from django.db import models
from django_filters import rest_framework as filters
from django_filters import widgets

from core.models import EventLog


class EventLogFilter(filters.FilterSet):
    # archived = filters.BooleanFilter(
    #     field_name="is_archived", widget=widgets.BooleanWidget()
    # )

    class Meta:
        model = EventLog
        fields = ["is_archived", "is_test"]
        filter_overrides = {
            models.BooleanField: {
                "filter_class": filters.BooleanFilter,
                "extra": lambda f: {
                    "widget": forms.CheckboxInput,
                },
            },
        }
