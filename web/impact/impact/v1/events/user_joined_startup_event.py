from datetime import datetime
from pytz import utc
from django.contrib.auth import get_user_model
from django.db.models import Q
from impact.utils import (
    next_instance,
)

User = get_user_model()


class UserJoinedStartupEvent(object):
    DESCRIPTION_FORMAT = "Joined {name} ({id})"
    EVENT_TYPE = "joined startup"

    def __init__(self, member):
        self.member = member

    @classmethod
    def events(cls, user):
        result = []
        for stm in user.startupteammember_set.all():
            result.append(cls(stm))
        return result

    def serialize(self):
        earliest, latest = self._join_time()
        return {
            "datetime": earliest,
            "latest_datetime": latest,
            "event_type": self.EVENT_TYPE,
            "description": self.DESCRIPTION_FORMAT.format(
                name=self.member.startup.name,
                id=self.member.startup.organization.id)
            }

    def _join_time(self):
        member_time = self.member.created_at
        if member_time:
            return (member_time, member_time)
        earliest = self.member.user.date_joined
        latest = utc.localize(datetime.now())
        most_recent_stm = User.objects.filter(
            startupteammember__id__lte=self.member.id
            ).order_by('-date_joined').first()
        if most_recent_stm:
            earliest = most_recent_stm.date_joined
        stm_with_created_at = next_instance(self.member,
                                            Q(created_at__isnull=False))
        if stm_with_created_at:
            latest = stm_with_created_at.created_at
        return (earliest, latest)
