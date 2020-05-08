# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from abc import ABCMeta
from rest_framework.response import Response

from ..helpers import json_object
from .import ImpactView


class BaseDetailView(ImpactView):
    __metaclass__ = ABCMeta

    def get(self, request, pk):
        self.instance = self.model().objects.get(pk=pk)
        return Response(self.serialize(self.instance))

    def metadata(self):
        result = {}
        get = self.method_options("GET", default={})
        if "GET" in self.actions:
            result["GET"] = json_object(get)
        result.update(self.metadata_object_action("PATCH"))
        return result
