# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import UserRole
from impact.v1.events.base_user_became_mentor_event import (
    BaseUserBecameMentorEvent,
)


class UserBecameDesiredMentorEvent(BaseUserBecameMentorEvent):
    EVENT_TYPE = "became desired mentor"
    USER_ROLE = UserRole.DESIRED_MENTOR
    ROLE_NAME = USER_ROLE
