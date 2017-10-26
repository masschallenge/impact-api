# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import (
    INDUSTRY_FIELDS,
    IndustryHelper,
)


class IndustryListView(BaseListView):
    helper_class = IndustryHelper

    def metadata(self):
        return self.options_from_fields(INDUSTRY_FIELDS, ["GET_LIST"])
