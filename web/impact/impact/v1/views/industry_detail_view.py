# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.permissions import (
    V1APIPermissions,
)
from impact.v1.helpers import IndustryHelper
from impact.v1.metadata import ImpactMetadata
from impact.v1.views.base_detail_view import BaseDetailView


class IndustryDetailView(BaseDetailView):
    helper_class = IndustryHelper
    metadata_class = ImpactMetadata
    permission_classes = (
        V1APIPermissions,
    )
