# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from impact.v1.views.list_view import ListView
from impact.v1.helpers import (
    PROGRAM_FAMILY_FIELDS,
    ProgramFamilyHelper,
)


class ProgramFamilyListView(ListView):
    helper_class = ProgramFamilyHelper

    def metadata(self):
        return self.options_from_fields(PROGRAM_FAMILY_FIELDS, ["GET_LIST"])
