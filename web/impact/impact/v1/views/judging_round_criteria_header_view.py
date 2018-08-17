# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from itertools import chain
from accelerator.models import (
    Application,
    CriterionOptionSpec,
    JudgingRound,
)
from rest_framework.response import Response
from impact.v1.views.impact_view import ImpactView
from impact.v1.classes.option_analysis import OptionAnalysis
from impact.v1.helpers.model_helper import (
    READ_ONLY_ID_FIELD,
    READ_ONLY_INTEGER_FIELD,
    READ_ONLY_OBJECT_FIELD,
    READ_ONLY_STRING_FIELD,
)


JUDGING_ROUND_CRITERIA_HEADER_FIELDS = {    
    "start_date": READ_ONLY_INTEGER_FIELD,
    "end_date": READ_ONLY_INTEGER_FIELD,
    "application_count": READ_ONLY_INTEGER_FIELD, 
    "reads_per_app": READ_ONLY_INTEGER_FIELD,
    "total_reads_required": READ_ONLY_INTEGER_FIELD,
    "judging_capacity": READ_ONLY_INTEGER_FIELD,
}


class JudgingRoundCriteriaHeaderView(ImpactView):
    view_name = "judging_round_criteria_header_view"
    model = JudgingRound

    @classmethod
    def fields(cls):
        return JUDGING_ROUND_CRITERIA_HEADER_FIELDS

    def get(self, request, pk):
        self.instance = self.model.objects.get(pk=pk)
        application_type = self.instance.application_type
        application_count = application_type.application_set.filter(
            application_status="submitted").count()
        reads_criteria = CriterionOptionSpec.objects.filter(
            criterion__judging_round=self.instance,
            criterion__type="reads")
        if reads_criteria.exists():
            reads_per_app = reads_criteria.first().count
        else:
            reads_per_app = 0
        total_reads_required = reads_per_app * application_count
        judging_capacity = _judging_capacity_for_round(self.instance)        
        
        return Response({    
            "start_date": self.instance.start_date_time,
            "end_date": self.instance.end_date_time,
            "application_count": application_count,
            "reads_per_app": reads_per_app,
            "total_reads_required": total_reads_required,
            "judging_capacity": judging_capacity,
        })
                        

def _judging_capacity_for_round(judging_round):
    return sum(judging_round.judgeroundcommitment_set.filter(
        commitment_state=True).values_list('capacity', flat=True))
