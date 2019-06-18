# MIT License
# Copyright (c) 2019 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import (
    MentorProgramOfficeHourHelper,
)


LOOKUPS = {
    'mentor_email': 'mentor__email__icontains',
    'mentor_first_name': 'mentor__first_name__icontains',
    'finalist_email': 'finalist__email__icontains',
    'finalist_first_name': 'mentor__first_name__icontains',
}


class MentorProgramOfficeHourListView(BaseListView):
    view_name = "office_hour"
    helper_class = MentorProgramOfficeHourHelper

    def filter(self, qs):
        if self.request.query_params.keys():
            lookup = self._get_lookup()
        return qs.filter(**lookup)

    def _get_lookup(self):
        query_params = self.request.query_params.dict()
        query_filter = {
            LOOKUPS[key]: value for key, value in query_params.items()
            if key in LOOKUPS.keys()
        }
        return query_filter
