# MIT License
# Copyright (c) 2019 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import (
    MentorProgramOfficeHourHelper,
)


LOOKUPS = {
    'mentor_email': 'mentor__email__icontains',
    'mentor_id': 'mentor_id',
    'finalist_email': 'finalist__email__icontains',
    'finalist_id': 'finalist_id',
}


class MentorProgramOfficeHourListView(BaseListView):
    view_name = "office_hour"
    helper_class = MentorProgramOfficeHourHelper

    def filter(self, queryset):
        if self.request.query_params.keys():
            filter_values = self._get_filter()
            return queryset.filter(**filter_values)
        return queryset

    def _get_filter(self):
        query_params = self.request.query_params.dict()
        query_filter = {
            LOOKUPS[key]: value for key, value in query_params.items()
            if key in LOOKUPS.keys()
        }
        return query_filter
