# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response
from rest_framework.views import APIView

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import Organization
from impact.v1.metadata import ImpactMetadata
from impact.v1.events import (
    OrganizationBecomeEntrantEvent,
    OrganizationCreatedEvent,
)


class OrganizationHistoryView(APIView):
    model = Organization
    metadata_class = ImpactMetadata

    permission_classes = (
        V1APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        events = []
        for event_class in [OrganizationCreatedEvent,
                            OrganizationBecomeEntrantEvent]:
            events = events + event_class.events(self.instance)
        result = {
            "history": [event.serialize() for event in events]
        }
        return Response(result)
