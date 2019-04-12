# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import (
    COULD_BE_STARTUP_CHECK,
    # IS_STARTUP_CHECK,
    OrganizationHelper,
)


class OrganizationListView(BaseListView):
    view_name = "organization"
    helper_class = OrganizationHelper

    def description_check(self, check_name):
        # This will be needed once we do POST/PATCH for
        # organizations, but not yet...
        # if check_name == IS_STARTUP_CHECK:
        #     return False
        if check_name == COULD_BE_STARTUP_CHECK:
            return True
        return check_name
