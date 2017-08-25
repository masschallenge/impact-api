# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import Organization
from impact.v1.metadata import ImpactMetadata
from impact.v1.events import (
    OrganizationBecomeEntrantEvent,
    OrganizationBecomeFinalistEvent,
    OrganizationCreatedEvent,
)

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

class BaseHistoryView(APIView):
    metadata_class = ImpactMetadata

    permission_classes = (
        V1APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        events = []
        for event_class in self.event_classes:
            events = events + event_class.events(self.instance)
        result = {
            "history": sorted([event.serialize() for event in events],
                       key=_event_key)
        }
        return Response(result)


def _event_key(event):
    date_time = event["datetime"]
    if isinstance(date_time, datetime):
        return date_time.strftime(DATETIME_FORMAT)
    return date_time