from django.contrib.auth import get_user_model
from impact.v1.events.base_history_event import BaseHistoryEvent

User = get_user_model()


class UserCreatedEvent(BaseHistoryEvent):
    EVENT_TYPE = "user created"

    def __init__(self, user):
        super(UserCreatedEvent, self).__init__()
        self.user = user

    @classmethod
    def events(cls, user):
        return [cls(user)]

    def serialize(self):
        return {
            "datetime": self.user.date_joined,
            "event_type": self.EVENT_TYPE,
            "description": "",
            }
