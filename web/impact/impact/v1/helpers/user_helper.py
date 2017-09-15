from impact.utils import get_profile
from impact.v1.helpers.model_helper import ModelHelper
from impact.v1.helpers.profile_helper import ProfileHelper

VALID_GENDERS = ["f", "m", "o", "p"]

INVALID_GENDER_ERROR = ("Invalid gender: '{}'. Valid values are "
                        "'f' or 'female', 'm' or 'male', "
                        "'o' or 'other', and 'p' or 'prefer not to state'")

GENDER_TRANSLATIONS = {
    "female": "f",
    "male": "m",
    "other": "o",
    "prefer not to state": "p",
}


class UserHelper(ModelHelper):
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
        "id",
        "last_login",
        "date_joined",
        "expert_category",
        "mentoring_specialties",
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
        return getattr(self.profile, field, None)

    @property
    def first_name(self):
        return self.subject.full_name

    @property
    def last_name(self):
        return self.subject.short_name

    @property
    def expert_category(self):
        profile = get_profile(self.subject)
        if hasattr(profile, "expert_category"):
            category = profile.expert_category
            if category:
                return category.name

    @property
    def mentoring_specialties(self):
        profile = get_profile(self.subject)
        if hasattr(profile, "mentoring_specialties"):
            specialties = profile.mentoring_specialties
            if specialties:
                return [specialty.name for specialty in specialties.all()]


def find_gender(gender):
    if not hasattr(gender, "lower"):
        return None
    gender = GENDER_TRANSLATIONS.get(gender.lower(), gender)
    if gender in VALID_GENDERS:
        return gender
    return None
