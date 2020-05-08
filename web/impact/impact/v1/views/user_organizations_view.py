# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from accelerator.models import (
    PartnerTeamMember,
    StartupTeamMember,
)
from .impact_view import ImpactView
from .utils import (
    coalesce_dictionaries,
    map_data,
)
from ..helpers import ORGANIZATION_USER_FIELDS


class UserOrganizationsView(ImpactView):
    view_name = "user_organizations"
    model = get_user_model()
    list_key = "organizations"

    @classmethod
    def fields(self):
        return ORGANIZATION_USER_FIELDS

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        all_data = self.startup_data() + self.partner_data()
        return Response({"organizations": coalesce_dictionaries(all_data)})

    def partner_data(self):
        return map_data(PartnerTeamMember,
                        Q(team_member=self.instance),
                        "partner_id",
                        ["partner__organization_id",
                         "partner_administrator"],
                        ["id", "partner_administrator"])

    def startup_data(self):
        return map_data(StartupTeamMember,
                        Q(user=self.instance),
                        "startup_id",
                        ["startup__organization_id",
                         "startup_administrator",
                         "primary_contact"],
                        ["id", "startup_administrator", "primary_contact"])
