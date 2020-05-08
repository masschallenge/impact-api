# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from .permissions import (
    V1ConfidentialAPIPermissions,
)
from .v1.helpers import (
    PK_FIELD,
    UserHelper,
    OPTIONAL_STRING_FIELD,
)
from .v1.views.base_detail_view import BaseDetailView


class UserConfidentialView(BaseDetailView):
    view_name = "user_confidential"
    helper_class = UserHelper

    permission_classes = (
        V1ConfidentialAPIPermissions,
    )

    @classmethod
    def fields(cls):
        return {
            "id": PK_FIELD,
            "expert_group": OPTIONAL_STRING_FIELD,
            "internal_notes": OPTIONAL_STRING_FIELD,
        }
