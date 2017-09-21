# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import Industry
from impact.v1.helpers import IndustryHelper
from impact.v1.metadata import ImpactMetadata


class IndustryDetailView(LoggingMixin, APIView):
    model = Industry
    metadata_class = ImpactMetadata

    permission_classes = (
        V1APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        return Response(IndustryHelper(self.instance).serialize())
