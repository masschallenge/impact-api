# MIT License
# Copyright (c) 2019 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import (
    MentorProgramOfficeHourHelper,
)


LOOKUPS = {
    'mentor_email': 'mentor__email',
    'mentor_name': 'mentor__name',
    'finalist_email': 'finalist__email',
    'finalist_name': 'mentor__name',
}

class MentorProgramOfficeHourListView(BaseListView):
    view_name = "office_hour"
    helper_class = MentorProgramOfficeHourHelper

    def filter(self, qs):
        return self.filter_by_field("mentor_email", qs, "mentor__email")
