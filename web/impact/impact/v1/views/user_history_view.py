# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from .v1.views.base_history_view import BaseHistoryView
from .v1.events import (
    UserBecameConfirmedJudgeEvent,
    UserBecameConfirmedMentorEvent,
    UserBecameDesiredJudgeEvent,
    UserBecameDesiredMentorEvent,
    UserBecameFinalistEvent,
    UserCreatedEvent,
    UserJoinedStartupEvent,
    UserReceivedNewsletterEvent,
)

User = get_user_model()


class UserHistoryView(BaseHistoryView):
    view_name = "user_history"
    model = User
    event_classes = [UserBecameConfirmedJudgeEvent,
                     UserBecameConfirmedMentorEvent,
                     UserBecameDesiredJudgeEvent,
                     UserBecameDesiredMentorEvent,
                     UserBecameFinalistEvent,
                     UserCreatedEvent,
                     UserJoinedStartupEvent,
                     UserReceivedNewsletterEvent]
