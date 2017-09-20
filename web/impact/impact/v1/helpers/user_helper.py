from django.conf import settings

from impact.utils import get_profile
from impact.v1.helpers.model_helper import ModelHelper
from impact.v1.helpers.profile_helper import ProfileHelper


class UserHelper(ModelHelper):
    MODEL = settings.AUTH_USER_MODEL

    REQUIRED_KEYS = [
        "email",
        "first_name",
        "last_name",
        ]
    OPTIONAL_KEYS = [
        "is_active",
        ]
    USER_INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS
    READ_ONLY_KEYS = [
        "date_joined",
        "id",
        "last_login",
        ]
    OUTPUT_KEYS = READ_ONLY_KEYS + USER_INPUT_KEYS + ProfileHelper.OUTPUT_KEYS
    INPUT_KEYS = USER_INPUT_KEYS + ProfileHelper.INPUT_KEYS
    KEY_TRANSLATIONS = {
        "first_name": "full_name",
        "last_name": "short_name",
        }

    def __init__(self, *args, **kwargs):
        super(UserHelper, self).__init__(*args, **kwargs)
        self.profile = get_profile(self.subject)

    @classmethod
    def translate_key(cls, key):
        return cls.KEY_TRANSLATIONS.get(key, key)

    def field_value(self, field):
        result = super(UserHelper, self).field_value(field)
        if result is not None:
            return result
        return ProfileHelper(self.profile).field_value(field)

    @property
    def first_name(self):
        return self.subject.full_name

    @property
    def last_name(self):
        return self.subject.short_name
