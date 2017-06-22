# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from factory import (
    DjangoModelFactory,
    SubFactory,
)

from impact.models import (
    CONFIRMED_RELATIONSHIP,
    StartupMentorRelationship,
)

from .expert_factory import ExpertFactory
from .startup_mentor_tracking_record_factory import (
    StartupMentorTrackingRecordFactory
)


class StartupMentorRelationshipFactory(DjangoModelFactory):

    class Meta:
        model = StartupMentorRelationship

    startup_mentor_tracking = SubFactory(StartupMentorTrackingRecordFactory)
    mentor = SubFactory(ExpertFactory)
    status = CONFIRMED_RELATIONSHIP
    primary = True
