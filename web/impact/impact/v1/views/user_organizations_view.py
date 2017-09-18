from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import (
    PartnerTeamMember,
    StartupTeamMember,
)
from impact.v1.metadata import ImpactMetadata


class UserOrganizationsView(LoggingMixin, APIView):
    permission_classes = (
        V1APIPermissions,
    )
    metadata_class = ImpactMetadata
    model = get_user_model()

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        data_by_org_id = {}
        # Partner data wins over startup data.
        all_data = self.startup_data() + self.partner_data()
        for data in all_data:
            id = data["id"]
            org = data_by_org_id.get(id, {})
            org.update(data)
            data_by_org_id[id] = org
        return Response({"organizations": data_by_org_id.values()})

    def partner_data(self):
        # Oldest/lowest id first
        team = PartnerTeamMember.objects.filter(
            team_member=self.instance).order_by("partner__id")
        data = team.values_list("partner__organization_id",
                                "partner_administrator")
        return [{"id": id,
                 "partner_administrator": administrator}
                for id, administrator in data]

    def startup_data(self):
        # Oldest/lowest id first
        team = StartupTeamMember.objects.filter(
            user=self.instance).order_by("startup__id")
        data = team.values_list("startup__organization_id",
                                "startup_administrator",
                                "primary_contact")
        return [{"id": id,
                 "startup_administrator": administrator,
                 "primary_contact": primary_contact}
                for id, administrator, primary_contact in data]
