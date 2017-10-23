# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import Organization
from impact.v1.helpers import (
    ORGANIZATION_FIELDS,
    OrganizationHelper,
)
from impact.v1.metadata import ImpactMetadata
from impact.v1.views import ImpactView


class OrganizationDetailView(ImpactView):
    model = Organization
    metadata_class = ImpactMetadata

    permission_classes = (
        V1APIPermissions,
    )

    def metadata(self):
        return self.options_from_fields(ORGANIZATION_FIELDS, ["GET"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        return Response(OrganizationHelper(self.instance).serialize())
