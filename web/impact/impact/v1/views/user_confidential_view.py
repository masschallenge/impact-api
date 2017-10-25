# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from rest_framework.response import Response

from impact.permissions import (
    V1ConfidentialAPIPermissions,
)
from impact.v1.helpers import (
    INTEGER_FIELD,
    PK_FIELD,
    UserHelper,
    STRING_FIELD,
)
from impact.v1.metadata import ImpactMetadata
from impact.v1.views.impact_view import ImpactView

User = get_user_model()

USER_CONFIDENTIAL_FIELDS = {
    "id": PK_FIELD,
    "expert_group": INTEGER_FIELD,
    "internal_notes": STRING_FIELD,
}


class UserConfidentialView(ImpactView):
    metadata_class = ImpactMetadata

    permission_classes = (
        V1ConfidentialAPIPermissions,
    )

    CONFIDENTIAL_KEYS = ["id", "expert_group", "internal_notes"]

    def metadata(self):
        return self.options_from_fields(USER_CONFIDENTIAL_FIELDS, ["GET"])

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        result = UserHelper(user).serialize(fields=self.CONFIDENTIAL_KEYS)
        return Response(result)
