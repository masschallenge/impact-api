from impact.utils import get_profile


REQUIRED_USER_KEYS = [
    "email",
    "first_name",
    "last_name",
]
OPTIONAL_USER_KEYS = [
    "is_active",
]
INPUT_USER_KEYS = REQUIRED_USER_KEYS + OPTIONAL_USER_KEYS

READ_ONLY_USER_KEYS = [
    "id",
    "last_login",
    "date_joined",
]
OUTPUT_USER_KEYS = READ_ONLY_USER_KEYS + INPUT_USER_KEYS


REQUIRED_PROFILE_KEYS = [
    "gender",
]
OPTIONAL_PROFILE_KEYS = [
    "bio",
    "company",
    "facebook_url",
    "judge_interest",
    "linked_in_url",
    "mentor_interest",
    "office_hours_interest",
    "office_hours_topics",
    "personal_website_url",
    "phone",
    "referred_by",
    "speaker_interest",
    "speaker_topics",
    "title",
    "twitter_handle",
]
INPUT_PROFILE_KEYS = REQUIRED_PROFILE_KEYS + OPTIONAL_PROFILE_KEYS

READ_ONLY_PROFILE_KEYS = [
    "updated_at",
]
OUTPUT_PROFILE_KEYS = READ_ONLY_PROFILE_KEYS + INPUT_PROFILE_KEYS

ALL_USER_INPUT_KEYS = INPUT_USER_KEYS + INPUT_PROFILE_KEYS

KEY_TRANSLATIONS = {
    "first_name": "full_name",
    "last_name": "short_name",  # Yes, this is correct
}

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


class UserHelper(object):
    def __init__(self, user):
        self.user = user

    def serialize(self):
        result = {}
        for field in OUTPUT_USER_KEYS:
            result[field] = getattr(self.user,
                                    KEY_TRANSLATIONS.get(field, field))
        result.update(self.profile_fields(OUTPUT_PROFILE_KEYS))
        category = self.profile_field("expert_category")
        if category:
            result["expert_category"] = category.name
        specialties = self.profile_field("mentoring_specialties")
        if specialties:
            result["mentoring_specialties"] = [
                specialty.name for specialty in specialties.all()]
        return result

    def profile(self):
        return get_profile(self.user)

    def profile_fields(self, fields):
        profile = self.profile()
        result = {}
        for field in fields:
            if hasattr(profile, field):
                result[field] = getattr(profile, field)
        return result

    def profile_field(self, field):
        profile = self.profile()
        if hasattr(profile, field):
            return getattr(profile, field)
        return None


def find_gender(gender):
    if not hasattr(gender, "lower"):
        return None
    gender = GENDER_TRANSLATIONS.get(gender.lower(), gender)
    if gender in VALID_GENDERS:
        return gender
    return None
