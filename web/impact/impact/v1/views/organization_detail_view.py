# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.models import Organization
from impact.v1.helpers import OrganizationHelper
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
        if check_name in ["is_startup", "could_be_startup"]:
            return OrganizationHelper(self.organization).is_startup
        return check_name
