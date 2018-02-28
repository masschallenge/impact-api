# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from accelerator.models import UserRole
from impact.v1.events.base_user_became_judge_event import (
    BaseUserBecameJudgeEvent,
)


class UserBecameConfirmedJudgeEvent(BaseUserBecameJudgeEvent):
    EVENT_TYPE = "became confirmed judge"
    USER_ROLE = UserRole.JUDGE
    ROLE_NAME = "Confirmed Judge"

    def judging_round_from_label(self, label):
        if label:
            return label.rounds_confirmed_for.first()
        return None
