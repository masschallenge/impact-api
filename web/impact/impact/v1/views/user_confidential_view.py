# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from impact.permissions import (
    V1ConfidentialAPIPermissions,
)
from impact.v1.metadata import (
    ImpactMetadata,
    OPTIONAL_STRING_TYPE,
)
from impact.v1.helpers import UserHelper

User = get_user_model()


class UserConfidentialView(APIView):
    metadata_class = ImpactMetadata

    permission_classes = (
        V1ConfidentialAPIPermissions,
    )

    METADATA_ACTIONS = {"GET": {
            "expert_group": OPTIONAL_STRING_TYPE,
            "internal_notes": OPTIONAL_STRING_TYPE,
            }}
    CONFIDENTIAL_KEYS = ["id", "expert_group", "internal_notes"]

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        result = UserHelper(user).serialize(fields=self.CONFIDENTIAL_KEYS)
        return Response(result)
