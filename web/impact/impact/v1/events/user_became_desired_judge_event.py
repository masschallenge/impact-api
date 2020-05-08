# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import UserRole
from .v1.events.base_user_became_judge_event import (
    BaseUserBecameJudgeEvent,
)


class UserBecameDesiredJudgeEvent(BaseUserBecameJudgeEvent):
    EVENT_TYPE = "became desired judge"
    USER_ROLE = UserRole.DESIRED_JUDGE
    ROLE_NAME = USER_ROLE

    def judging_round_from_label(self, label):
        if label:
            return label.rounds_desired_for.first()
        return None
