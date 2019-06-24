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
            return self._filter_by_participant_names(qs)

        if self._has_participant_filter(ID_FIELDS):
            return self._filter_by_ids(qs)

        user_name = self.request.query_params.get('user_name', None)
        if user_name:
            return self._filter_by_user_name(user_name, qs)

    def _filter_by_id(self, id_field, qs):
        value = self.request.query_params.get(id_field, None)
        if value and value.isdigit():
            return self.filter_by_field(id_field, qs)
        return qs

    def _filter_by_ids(self, qs):
        qs = self._filter_by_id('mentor_id', qs)
        qs = self._filter_by_id('finalist_id', qs)
        return qs

    def _filter_by_participant_names(self, qs):
        qs = self._filter_by_participant_name('mentor_name', qs)
        qs = self._filter_by_participant_name('finalist_name', qs)
        return qs

    def _filter_by_participant_name(self, name_field, qs):
        value = self.request.query_params.get(name_field, None)
        user_type = name_field.replace('_name', '')
        if value:
            return self._filter_by_full_name(qs, user_type, value)
        return qs

    def _filter_by_user_name(self, user_name, qs):
        mentor_qs = self._filter_by_full_name(qs, 'mentor', user_name)
        finalist_qs = self._filter_by_full_name(qs, 'finalist', user_name)
        return mentor_qs | finalist_qs

    def _filter_by_full_name(self, qs, user, name_value):
        first_name_field = '{}__first_name'.format(user)
        last_name_field = '{}__last_name'.format(user)
        result = qs.annotate(
            full_name=Concat(
                first_name_field, V(' '), last_name_field)).filter(
                    full_name__icontains=name_value)
        return result

    def _has_participant_filter(self, fields):
        return any(
            field in self.request.query_params.keys() for field in fields)
