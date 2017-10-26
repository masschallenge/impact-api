# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import Organization
from impact.v1.helpers import OrganizationHelper
from impact.v1.metadata import ImpactMetadata
from impact.v1.views import ImpactView


class OrganizationDetailView(ImpactView):
    helper_class = OrganizationHelper
    metadata_class = ImpactMetadata

    permission_classes = (
        V1APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        self.organization = None
        super().__init__(*args, **kwargs)

    def options(self, request, pk):
        self.organization = Organization.objects.get(pk=pk)
        return super().options(request, pk)

    def description_check(self, check_name):
        if check_name in ["is_startup", "could_be_startup"]:
            return OrganizationHelper(self.organization).is_startup
        return check_name
