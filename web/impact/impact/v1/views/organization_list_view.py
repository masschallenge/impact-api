# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import OrganizationHelper


class OrganizationListView(BaseListView):
    helper_class = OrganizationHelper

    def description_check(self, check_name):
        # This will be needed once we do POST/PATCH for
        # organizations, but not yet...
        # if check_name == "is_startup":
        #     return False
        if check_name == "could_be_startup":
            return True
        return check_name
