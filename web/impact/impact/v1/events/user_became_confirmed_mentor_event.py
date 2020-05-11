# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import UserRole
from .base_user_became_mentor_event import (
    BaseUserBecameMentorEvent,
)


class UserBecameConfirmedMentorEvent(BaseUserBecameMentorEvent):
    EVENT_TYPE = "became confirmed mentor"
    USER_ROLE = UserRole.MENTOR
    ROLE_NAME = "Confirmed Mentor"
