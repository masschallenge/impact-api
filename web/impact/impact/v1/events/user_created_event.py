# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from .base_history_event import BaseHistoryEvent

User = get_user_model()


class UserCreatedEvent(BaseHistoryEvent):
    EVENT_TYPE = "user created"

    def __init__(self, user):
        super().__init__()
        self.user = user

    @classmethod
    def events(cls, user):
        return [cls(user)]

    def calc_datetimes(self):
        self.earliest = self.user.date_joined
