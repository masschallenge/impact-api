# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ...api_data import APIData
from accelerator.models import ProgramStartupStatus


class StartupListData(APIData):
    ALPHA_ASC_ORDER = "AlphaAsc"
    ALPHA_DSC_ORDER = "AlphaDsc"
    RANDOM_ORDER = "Random"
    ORDER_BY_VALUES = [ALPHA_ASC_ORDER, ALPHA_DSC_ORDER, RANDOM_ORDER]
    STATUS_GROUP_PREFIX = "StatusGroup:"
    INDUSTRY_GROUP_BY = "Industry"
    ALL_INDUSTRY = "All"

    def valid(self):
        self.debug = (self.YES == self.validate_field("Debug",
                                                      [self.NO, self.YES]))
        self.all_group = self.validate_field("IncludeAllGroup",
                                             self.YES_NO_VALUES)
        self.order_by = self.validate_field("OrderBy", self.ORDER_BY_VALUES)
        self.program = self.validate_program()
        self.startup_statuses = self._validate_startup_status()
        self.group_by = self._validate_group_by()
        return self.errors == []

    def _validate_startup_status(self):
        status = self.data.get("StartupStatus", None)
        result = None
        if status:
            result = ProgramStartupStatus.objects.filter(
                program=self.program,
                startup_list_include=True,
                startup_list_tab_id=status)
            if not result:
                self.record_invalid_value(status, "StartupStatus")
        return result

    def _validate_group_by(self):
        group_by = self.data.get("GroupBy", None)
        if group_by == self.INDUSTRY_GROUP_BY or group_by is None:
            return group_by
        if group_by.startswith(self.STATUS_GROUP_PREFIX):
            return self._validate_status_group(group_by)
        if group_by is not None:
            self.record_invalid_value(group_by, "GroupBy")
        return None

    def _validate_status_group(self, group_by):
        status_group = group_by[len(self.STATUS_GROUP_PREFIX):]
        if status_group in ProgramStartupStatus.objects.filter(
                startup_list_include=True
                ).values_list("status_group", flat=True):
            return group_by
        self.record_invalid_value(group_by, "StatusGroup")
        return None
