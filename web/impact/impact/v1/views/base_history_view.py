# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response
from rest_framework.views import APIView

from impact.permissions import (
    V1APIPermissions,
)
from impact.v1.metadata import (
    ImpactMetadata,
    READ_ONLY_LIST_TYPE,
)


class BaseHistoryView(APIView):
    metadata_class = ImpactMetadata

    permission_classes = (
        V1APIPermissions,
    )

    METADATA_ACTIONS = {"GET": {"history": READ_ONLY_LIST_TYPE}}

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
