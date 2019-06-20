# MIT License
# Copyright (c) 2019 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import (
    MentorProgramOfficeHourHelper,
)


class MentorProgramOfficeHourListView(BaseListView):
    view_name = "office_hour"
    helper_class = MentorProgramOfficeHourHelper

    def filter(self, queryset):
        allowed_params = ['mentor_id', 'finalist_id']
        param_items = self.request.query_params.items()

        if not param_items:
            return queryset

        filter_values = {
            key: value for (key, value) in param_items
            if key in allowed_params}
        return queryset.filter(**filter_values)
