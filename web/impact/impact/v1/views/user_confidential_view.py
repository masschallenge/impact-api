# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.permissions import (
    V1ConfidentialAPIPermissions,
)
from impact.v1.helpers import (
    PK_FIELD,
    UserHelper,
    STRING_FIELD,
)
from impact.v1.views.base_detail_view import BaseDetailView


class UserConfidentialView(BaseDetailView):
    helper_class = UserHelper

    permission_classes = (
        V1ConfidentialAPIPermissions,
    )

    @classmethod
    def fields(cls):
        return {
            "id": PK_FIELD,
            "expert_group": STRING_FIELD,
            "internal_notes": STRING_FIELD,
        }
