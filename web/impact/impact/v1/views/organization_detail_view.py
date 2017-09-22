# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import Organization
from impact.v1.helpers import OrganizationHelper
from impact.v1.metadata import ImpactMetadata


class OrganizationDetailView(LoggingMixin, APIView):
    model = Organization
    metadata_class = ImpactMetadata

    permission_classes = (
        V1APIPermissions,
    )
    METADATA_ACTIONS = {
        "GET": OrganizationHelper.DETAIL_METADATA
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        return Response(OrganizationHelper(self.instance).serialize())
