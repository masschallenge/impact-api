from django.db.models import Q
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
from impact.v1.views.utils import (
    map_data,
    merge_data_by_id,
)


class UserOrganizationsView(LoggingMixin, APIView):
    permission_classes = (
        V1APIPermissions,
    )
    metadata_class = ImpactMetadata
    model = get_user_model()

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        all_data = self.startup_data() + self.partner_data()
        return Response({"organizations": merge_data_by_id(all_data)})

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
