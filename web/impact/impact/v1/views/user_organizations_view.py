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
        organizations = set(list(self.partner_organizations()) +
                            list(self.startup_organizations()))
        result = {"organizations": list(organizations)}
        return Response(result)

    def partner_organizations(self):
        team = PartnerTeamMember.objects.filter(
            team_member=self.instance)
        return team.values_list('partner__organization_id', flat=True)

    def startup_organizations(self):
        team = StartupTeamMember.objects.filter(
            user=self.instance)
        return team.values_list('startup__organization_id', flat=True)
