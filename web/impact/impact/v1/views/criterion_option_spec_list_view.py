# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.base_list_view import BaseListView
from impact.v1.helpers import CriterionOptionSpecHelper


class CriterionOptionSpecListView(BaseListView):
    view_name = "criterion_option_spec"
    helper_class = CriterionOptionSpecHelper

    
