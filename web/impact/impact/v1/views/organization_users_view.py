from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.metadata import SimpleMetadata
from impact.permissions import (
    V1APIPermissions,
)
from impact.models import (
    Organization,
    PartnerTeamMember,
    StartupTeamMember,
)
from impact.v1.metadata import OrganizationUsersMetadata


class OrganizationUsersView(APIView):
    permission_classes = (
        V1APIPermissions,
    )
    metadata_class = OrganizationUsersMetadata
    model = Organization

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        users = set(list(self.partner_users()) + list(self.startup_users()))
        result = {"users": list(users)}
        return Response(result)

    def partner_users(self):

        team = PartnerTeamMember.objects.filter(
            partner__organization=self.instance)
        return team.values_list('team_member_id', flat=True)

    def startup_users(self):
        team = StartupTeamMember.objects.filter(
            startup__organization=self.instance)
        return team.values_list('user_id', flat=True)
