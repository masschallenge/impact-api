# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from ..helpers import FunctionalExpertiseHelper
from .base_list_view import BaseListView


class FunctionalExpertiseListView(BaseListView):
    view_name = "functional_expertise"
    helper_class = FunctionalExpertiseHelper
