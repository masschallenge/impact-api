from impact.v1.helpers.model_helper import ModelHelper
from impact.v1.helpers.profile_helper import (
    ProfileHelper,
    expert_category,
    mentoring_specialties,
    profile_field,
)

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


OTHER_FUNCTIONS = {
    "expert_category": expert_category,
    "mentoring_specialties": mentoring_specialties,
}


class UserHelper(ModelHelper):
    KEY_TRANSLATIONS = {
        "first_name": "full_name",
        "last_name": "short_name",  # Yes, this is correct
        }
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
        ]
    OUTPUT_KEYS = READ_ONLY_KEYS + USER_INPUT_KEYS + ProfileHelper.OUTPUT_KEYS
    INPUT_KEYS = USER_INPUT_KEYS + ProfileHelper.INPUT_KEYS

    def field_value(self, field):
        function = self.field_function(field)
        if function:
            return function(self, field)
        return getattr(self.subject,
                       self.KEY_TRANSLATIONS.get(field, field))

    def field_function(self, field):
        function = OTHER_FUNCTIONS.get(field)
        if function:
            return function
        if field in ProfileHelper.OUTPUT_KEYS:
            return profile_field
        return None

    def profile_field(self, field):
        return profile_field(self, field)


def find_gender(gender):
    if not hasattr(gender, "lower"):
        return None
    gender = GENDER_TRANSLATIONS.get(gender.lower(), gender)
    if gender in VALID_GENDERS:
        return gender
    return None
