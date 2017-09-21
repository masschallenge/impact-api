# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.list_view import ListView
from impact.v1.helpers import IndustryHelper


class IndustryListView(ListView):
    helper_class = IndustryHelper
