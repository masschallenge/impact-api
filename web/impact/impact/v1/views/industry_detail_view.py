# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import Industry
from impact.v1.helpers import (
    INDUSTRY_FIELDS,
    IndustryHelper,
)
from impact.v1.metadata import ImpactMetadata
from impact.v1.views import ImpactView


class IndustryDetailView(ImpactView):
    model = Industry
    metadata_class = ImpactMetadata

    permission_classes = (
        V1APIPermissions,
    )

    def metadata(self):
        return self.options_from_fields(INDUSTRY_FIELDS, ["GET"])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        return Response(IndustryHelper(self.instance).serialize())
