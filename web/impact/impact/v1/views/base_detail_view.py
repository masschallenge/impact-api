# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from abc import ABCMeta
from rest_framework.response import Response

from impact.permissions import (
    V1APIPermissions,
)
from impact.v1.helpers import json_object
from impact.v1.metadata import ImpactMetadata
from impact.v1.views import ImpactView


class BaseDetailView(ImpactView):
    __metaclass__ = ABCMeta

    permission_classes = (
        V1APIPermissions,
    )

    metadata_class = ImpactMetadata

    def get(self, request, pk):
        self.instance = self.model().objects.get(pk=pk)
        return Response(self.serialize(self.instance))

    def metadata(self):
        result = {}
        get = self.method_options("GET", default={})
        if "GET" in self.actions:
            result["GET"] = json_object(get)
        if "PATCH" in self.actions:
            patch = self.method_options("PATCH")
            if patch:
                result["PATCH"] = json_object(patch)
        return result
