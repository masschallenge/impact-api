from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import (
    PartnerTeamMember,
    StartupTeamMember,
)
from impact.v1.metadata import ImpactMetadata
from impact.v1.views.impact_view import ImpactView
from impact.v1.views.utils import (
    coalesce_dictionaries,
    map_data,
)
from impact.v1.helpers import ORGANIZATION_USER_FIELDS


class UserOrganizationsView(ImpactView):
    permission_classes = (
        V1APIPermissions,
    )
    metadata_class = ImpactMetadata
    model = get_user_model()

    def metadata(self):
        return self.options_from_fields(ORGANIZATION_USER_FIELDS,
                                        ["SIMPLE_LIST"],
                                        key="organizations")

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
