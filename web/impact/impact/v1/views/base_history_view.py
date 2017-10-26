# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response

from impact.permissions import (
    V1APIPermissions,
)
from impact.v1.metadata import ImpactMetadata
from impact.v1.views.impact_view import ImpactView


class BaseHistoryView(ImpactView):
    metadata_class = ImpactMetadata

    permission_classes = (
        V1APIPermissions,
    )

    @classmethod
    def fields(cls):
        event_types = set()
        results = {}
        for klass in cls.event_classes:
            event_types.add(klass.event_type())
            results.update(klass.all_fields())
        results.update(event_type_field(event_types))
        return results

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        events = []
        for event_class in self.event_classes:
            events = events + event_class.events(self.instance)
        result = {
            "results": sorted([event.serialize() for event in events],
                              key=lambda e: (e["datetime"],
                                             e.get("latest_datetime",
                                                   e["datetime"])))
        }
        return Response(result)


def event_type_field(event_types):
    return {"event_type": {"json-schema": {"enum": list(event_types)}}}
