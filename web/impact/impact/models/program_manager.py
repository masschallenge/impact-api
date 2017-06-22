# MIT License
# Copyright (c) 2017 MassChallenge, Inc.


from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

from impact.utils import compose_filter


class ProgramManager(models.Manager):

    def visible(self):
        return self.get_queryset().filter(~Q(program_status__exact='hidden'))

    def accepting_applications(self):
        return self.get_queryset().filter(cycle__applications_open=True)

    def visible_to_startups(self, startups):
        if not isinstance(startups, (list, tuple, set, QuerySet)):
            startups = [startups]
        is_open = Q(cycle__applications_open=True)
        filter = compose_filter(["cycle",
                                 "program_overrides",
                                 "startupoverridegrant",
                                 "startup",
                                 "in"], startups)
        filter.update(compose_filter(["cycle",
                                      "program_overrides",
                                      "applications_open"], True))
        has_override = Q(**filter)
        return self.get_queryset().filter(is_open |
                                          has_override).distinct()
