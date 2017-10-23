from django.db.models import Q
from rest_framework.response import Response

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import (
    Organization,
    PartnerTeamMember,
    StartupTeamMember,
)
from impact.v1.metadata import ImpactMetadata
from impact.v1.views.impact_view import ImpactView
from impact.v1.views.utils import (
    coalesce_dictionaries,
    map_data,
)
from impact.v1.helpers import INTEGER_ARRAY_FIELD

ORGANIZATION_USERS_FIELDS = {
    "users": INTEGER_ARRAY_FIELD,
}


class OrganizationUsersView(ImpactView):
    permission_classes = (
        V1APIPermissions,
    )
    metadata_class = ImpactMetadata
    model = Organization

    def metadata(self):
        return self.options_from_fields(ORGANIZATION_USERS_FIELDS, ["GET"])

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        all_data = self.startup_data() + self.partner_data()
        return Response({"users": coalesce_dictionaries(all_data)})

    def partner_data(self):
        return map_data(PartnerTeamMember,
                        Q(partner__organization=self.instance),
                        "partner__id",
                        ["team_member_id", "partner_administrator"],
                        ["id", "partner_administrator"])

    def startup_data(self):
        return map_data(StartupTeamMember,
                        Q(startup__organization=self.instance),
                        "startup__id",
                        ["user_id",
                         "startup_administrator",
                         "primary_contact"],
                        ["id", "startup_administrator", "primary_contact"])
