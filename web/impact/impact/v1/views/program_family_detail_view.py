# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from rest_framework.response import Response

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import ProgramFamily
from impact.v1.helpers import (
    PROGRAM_FAMILY_FIELDS,
    ProgramFamilyHelper,
)
from impact.v1.metadata import ImpactMetadata
from impact.v1.views import ImpactView


class ProgramFamilyDetailView(ImpactView):
    model = ProgramFamily
    metadata_class = ImpactMetadata

    permission_classes = (
        V1APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def metadata(self):
        return self.options_from_fields(PROGRAM_FAMILY_FIELDS, ["GET"])

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        return Response(ProgramFamilyHelper(self.instance).serialize())
