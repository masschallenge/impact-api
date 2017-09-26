# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.list_view import ListView
from impact.v1.helpers import OrganizationHelper
from impact.v1.views.organization_detail_view import OrganizationDetailView


class OrganizationListView(ListView):
    helper_class = OrganizationHelper
    METADATA_ACTIONS = OrganizationDetailView.METADATA_ACTIONS
