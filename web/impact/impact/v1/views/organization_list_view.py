# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.list_view import ListView
from impact.v1.helpers import (
    ORGANIZATION_FIELDS,
    OrganizationHelper,
)


class OrganizationListView(ListView):
    helper_class = OrganizationHelper

    def metadata(self):
        return self.options_from_fields(ORGANIZATION_FIELDS,
                                        ["GET_LIST", "POST"])

    def description_check(self, check_name):
        if check_name == "is_startup":
            return False
        if check_name in "could_be_startup":
            return True
        return check_name
