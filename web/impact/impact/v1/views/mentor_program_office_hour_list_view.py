# MIT License
# Copyright (c) 2019 MassChallenge, Inc.
from django.db.models import Value as V
from django.db.models.functions import Concat

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import (
    MentorProgramOfficeHourHelper,
)

ID_FIELDS = ['mentor_id', 'finalist_id']
NAME_FIELDS = ['mentor_name', 'finalist_name']


class MentorProgramOfficeHourListView(BaseListView):
    view_name = "office_hour"
    helper_class = MentorProgramOfficeHourHelper

    def filter(self, qs):
        qs = super().filter(qs)
        if not self.request.query_params.keys():
            return qs

        if self._has_participant_filter(NAME_FIELDS):
            return self._filter_by_participant_name(qs)

        if self._has_participant_filter(ID_FIELDS):
            param_items = self.request.query_params.dict().items()
            return self._filter_by_participant_id(qs, param_items)

    def _filter_by_participant_name(self, qs):
        params = self.request.query_params
        mentor_name = params.get('mentor_name', None)
        finalist_name = params.get('finalist_name', None)

        if mentor_name:
            return self._filter_by_full_name(qs, 'mentor', mentor_name)
        if finalist_name:
            return self._filter_by_full_name(qs, 'finalist', finalist_name)
        return qs.none()

    def _filter_by_full_name(self, qs, user, name_value):
        first_name_field = '{}__first_name'.format(user)
        last_name_field = '{}__last_name'.format(user)
        result = qs.annotate(
            full_name=Concat(
                first_name_field, V(' '), last_name_field)).filter(
                    full_name__icontains=name_value)
        return result

    def _filter_by_participant_id(self, qs, param_items):
        filter_values = {
            key: value for key, value in param_items
            if key in ID_FIELDS and value.isdigit()}
        if filter_values:
            return qs.filter(**filter_values)
        return qs.none()

    def _has_participant_filter(self, fields):
        return any(
            field in self.request.query_params.keys() for field in fields)
