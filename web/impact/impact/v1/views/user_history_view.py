# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from impact.v1.views.base_history_view import BaseHistoryView
from impact.v1.events import (
    UserBecameConfirmedJudgeEvent,
    UserBecameFinalistEvent,
    UserCreatedEvent,
    UserJoinedStartupEvent,
)

User = get_user_model()


class UserHistoryView(BaseHistoryView):
    model = User

    event_classes = [UserBecameConfirmedJudgeEvent,
    				 UserBecameFinalistEvent,
    				 UserCreatedEvent,
                     UserJoinedStartupEvent]
