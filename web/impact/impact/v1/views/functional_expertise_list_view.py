# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.helpers import FunctionalExpertiseHelper
from impact.v1.views.base_list_view import BaseListView


class FunctionalExpertiseListView(BaseListView):
    view_name = "functional_expertise"
    helper_class = FunctionalExpertiseHelper
