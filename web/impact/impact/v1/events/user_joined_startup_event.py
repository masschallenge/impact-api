# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from datetime import datetime
from pytz import utc
from django.contrib.auth import get_user_model
from django.db.models import Q
from ...utils import next_instance
from .base_history_event import BaseHistoryEvent

User = get_user_model()


class UserJoinedStartupEvent(BaseHistoryEvent):
    DESCRIPTION_FORMAT = "Joined {name} ({id})"
    EVENT_TYPE = "joined startup"
    NO_ORGANIZATION_DESCRIPTION = "Joined startup (organization unknown)"
    
    def __init__(self, member):
        super().__init__()
        self.member = member

    def description(self):
        startup = self.member.startup
        if startup.organization is None:
            return self.NO_ORGANIZATION_DESCRIPTION
        else:
            return self.DESCRIPTION_FORMAT.format(
                name=startup.name,
                id=startup.organization.id)

    @classmethod
    def events(cls, user):
        result = []
        for stm in user.startupteammember_set.all():
            result.append(cls(stm))
        return result

    def calc_datetimes(self):
        self.earliest = self.member.created_at
        if self.earliest:
            return
        self.earliest = self.member.user.date_joined
        self.latest = utc.localize(datetime.now())
        most_recent_stm = User.objects.filter(
            startupteammember__id__lte=self.member.id
        ).order_by('-date_joined').first()
        if most_recent_stm:
            self.earliest = most_recent_stm.date_joined
        stm_with_created_at = next_instance(
            self.member, Q(created_at__isnull=False))
        if stm_with_created_at:
            self.latest = stm_with_created_at.created_at
