# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import (
    Clearance,
    IN_PERSON_JUDGING_ROUND_TYPE,
    ONLINE_JUDGING_ROUND_TYPE,
)

from .v1.views.base_list_view import BaseListView
from .v1.helpers import JudgingRoundHelper

INVALID_ROUND_TYPE_ERROR = ("Invalid value '{}' for round_type. "
                            "Use 'Online' or 'In-Person'.")


class JudgingRoundListView(BaseListView):
    view_name = "judging_round"
    helper_class = JudgingRoundHelper

    def get(self, request):
        self._validate_round_type(request)
        self.ignore_clearance = request.GET.get("ignore_clearance") is not None
        return super().get(request)

    def _validate_round_type(self, request):
        round_type = request.GET.get("round_type")
        if round_type is not None:
            if round_type.lower() not in [
                    IN_PERSON_JUDGING_ROUND_TYPE.lower(),
                    ONLINE_JUDGING_ROUND_TYPE.lower()]:
                self.errors.append(INVALID_ROUND_TYPE_ERROR.format(round_type))

    def filter(self, qs):
        by_round = self._filter_by_round_type(super().filter(qs))
        if self.ignore_clearance:
            return by_round
        else:
            # Only show ProgramFamilies the user has clearance for
            user = self.request.user
            clearances = Clearance.objects.filter(user=user)
            program_families = [c.program_family for c in clearances]
            by_round_and_clearance = by_round.filter(
                program__program_family__in=program_families)
            return by_round_and_clearance

    def _filter_by_round_type(self, qs):
        round_type = self.request.query_params.get("round_type", None)
        if round_type is not None:
            return qs.filter(round_type=round_type)
        return qs
