# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.permissions import (
    V1APIPermissions,
)
from impact.v1.helpers import IndustryHelper
from impact.v1.metadata import ImpactMetadata
from impact.v1.views import ImpactView


class IndustryDetailView(ImpactView):
    helper_class = IndustryHelper
    metadata_class = ImpactMetadata
    permission_classes = (
        V1APIPermissions,
    )
