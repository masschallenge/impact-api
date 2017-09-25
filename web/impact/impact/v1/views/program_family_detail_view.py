# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import ProgramFamily
from impact.v1.helpers import ProgramFamilyHelper
from impact.v1.metadata import ImpactMetadata


class ProgramFamilyDetailView(LoggingMixin, APIView):
    model = ProgramFamily
    metadata_class = ImpactMetadata

    permission_classes = (
        V1APIPermissions,
    )

    METADATA_ACTIONS = {
        "GET": ProgramFamilyHelper.DETAIL_METADATA
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        return Response(ProgramFamilyHelper(self.instance).serialize())
