# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import Organization
from impact.v1.helpers import (
    COULD_BE_STARTUP_CHECK,
    IS_STARTUP_CHECK,
    OrganizationHelper,
)
from impact.v1.views.base_detail_view import BaseDetailView


class OrganizationDetailView(BaseDetailView):
    view_name = "organization_detail"
    helper_class = OrganizationHelper

    def __init__(self, *args, **kwargs):
        self.organization = None
        super().__init__(*args, **kwargs)

    def options(self, request, pk):
        self.organization = Organization.objects.get(pk=pk)
        return super().options(request, pk)

    def description_check(self, check_name):
        if check_name in [IS_STARTUP_CHECK, COULD_BE_STARTUP_CHECK]:
            return OrganizationHelper(self.organization).is_startup
        return check_name
