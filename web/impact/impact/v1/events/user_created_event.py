from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreatedEvent(object):
    EVENT_TYPE = "user created"

    def __init__(self, user):
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
