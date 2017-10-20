from django.conf import settings

from impact.models import (
    EntrepreneurProfile,
    ExpertProfile,
)
from impact.utils import get_profile
from impact.v1.helpers.model_helper import (
    BOOLEAN_FIELD,
    EMAIL_FIELD,
    ModelHelper,
    PK_FIELD,
    READ_ONLY_DATE_FIELD,
    REQUIRED_STRING_FIELD,
    URL_FIELD,
    validate_boolean,
    validate_email_address,
    validate_string,
)
from impact.v1.helpers.profile_helper import (
    ADDITIONAL_INDUSTRY_IDS_FIELD,
    EXPERT_BOOLEAN_FIELD,
    EXPERT_CATEGORY_FIELD,
    EXPERT_STRING_FIELD,
    GENDER_FIELD,
    HOME_PROGRAM_FAMILY_ID_FIELD,
    MENTORING_SPECIALTIES_FIELD,
    NON_MEMBER_STRING_FIELD,
    PERSONAL_WEBSITE_URL_FIELD,
    PHONE_FIELD,
    PRIMARY_INDUSTRY_ID_FIELD,
    ProfileHelper,
    TWITTER_FIELD,
    USER_TYPE_FIELD,
)
from impact.v1.metadata import (
    OPTIONAL_STRING_TYPE,
    OPTIONAL_BOOLEAN_TYPE,
    OPTIONAL_LIST_TYPE,
    OPTIONAL_ID_TYPE,
    PK_TYPE,
    READ_ONLY_STRING_TYPE,
)


VALID_KEYS_NOTE = "Valid keys are: {}"

USER_PATCH_OPTIONS = {
    "first_name": OPTIONAL_STRING_TYPE,
    "last_name": OPTIONAL_STRING_TYPE,
    "email": OPTIONAL_STRING_TYPE,
    "is_active": OPTIONAL_BOOLEAN_TYPE,
    "gender": OPTIONAL_STRING_TYPE,
    "phone": OPTIONAL_STRING_TYPE,
    "company": OPTIONAL_STRING_TYPE,
    "title": OPTIONAL_STRING_TYPE,
    "expert_category": OPTIONAL_STRING_TYPE,
    "primary_industry_id": OPTIONAL_ID_TYPE,
    "home_program_family_id": OPTIONAL_ID_TYPE,
}

USER_PATCH_OPTIONS.update(dict([
            (key, OPTIONAL_BOOLEAN_TYPE)
            for key in ProfileHelper.OPTIONAL_BOOLEAN_KEYS]))
USER_PATCH_OPTIONS.update(dict([
            (key, OPTIONAL_STRING_TYPE)
            for key in ProfileHelper.OPTIONAL_STRING_KEYS]))
USER_POST_OPTIONS = USER_PATCH_OPTIONS.copy()
USER_POST_OPTIONS["user_type"] = OPTIONAL_STRING_TYPE

USER_GET_OPTIONS = USER_POST_OPTIONS.copy()
USER_GET_OPTIONS.update(
    {
        "id": PK_TYPE,
        "updated_at": READ_ONLY_STRING_TYPE,
        "last_login": READ_ONLY_STRING_TYPE,
        "date_joined": READ_ONLY_STRING_TYPE,
        "additional_industry_ids": OPTIONAL_LIST_TYPE,
        "mentoring_specialties": OPTIONAL_LIST_TYPE,
    })

USER_FIELDS = {
    "id": PK_FIELD,
    "updated_at": READ_ONLY_DATE_FIELD,
    "last_login": READ_ONLY_DATE_FIELD,
    "date_joined": READ_ONLY_DATE_FIELD,
    "user_type": USER_TYPE_FIELD,
    "first_name": REQUIRED_STRING_FIELD,
    "last_name": REQUIRED_STRING_FIELD,
    "phone": PHONE_FIELD,
    "is_active": BOOLEAN_FIELD,
    "judge_interest": EXPERT_BOOLEAN_FIELD,
    "mentor_interest": EXPERT_BOOLEAN_FIELD,
    "office_hours_interest": EXPERT_BOOLEAN_FIELD,
    "speaker_interest": EXPERT_BOOLEAN_FIELD,
    "speaker_topics": EXPERT_STRING_FIELD,
    "office_hours_topics": EXPERT_STRING_FIELD,
    "referred_by": EXPERT_STRING_FIELD,
    "company": EXPERT_STRING_FIELD,
    "title": EXPERT_STRING_FIELD,
    "bio": NON_MEMBER_STRING_FIELD,
    "primary_industry_id": PRIMARY_INDUSTRY_ID_FIELD,
    "home_program_family_id": HOME_PROGRAM_FAMILY_ID_FIELD,
    "additional_industry_ids": ADDITIONAL_INDUSTRY_IDS_FIELD,
    "gender": GENDER_FIELD,
    "expert_category": EXPERT_CATEGORY_FIELD,
    "mentoring_specialties": MENTORING_SPECIALTIES_FIELD,
    "email": EMAIL_FIELD,
    "twitter_handle": TWITTER_FIELD,
    "facebook_url": URL_FIELD,
    "linked_in_url": URL_FIELD,
    "personal_website_url": PERSONAL_WEBSITE_URL_FIELD,
}


class UserHelper(ModelHelper):
    VALIDATORS = {
        "email": validate_email_address,
        "full_name": validate_string,
        "is_active": validate_boolean,
        "short_name": validate_string,
        }

    MODEL = settings.AUTH_USER_MODEL

    DETAIL_GET_METADATA = USER_GET_OPTIONS
    DETAIL_PATCH_METADATA = USER_PATCH_OPTIONS
    LIST_POST_METADATA = USER_POST_OPTIONS

    REQUIRED_KEYS = [
        "email",
        "first_name",
        "last_name",
        ]
    OPTIONAL_BOOLEAN_KEYS = [
        "is_active",
        ]
    OPTIONAL_KEYS = OPTIONAL_BOOLEAN_KEYS
    USER_INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS
    READ_ONLY_KEYS = [
        "date_joined",
        "id",
        "last_login",
        ]
    OUTPUT_KEYS = READ_ONLY_KEYS + USER_INPUT_KEYS + ProfileHelper.OUTPUT_KEYS
    INPUT_KEYS = USER_INPUT_KEYS + ProfileHelper.INPUT_KEYS
    ALL_BOOLEAN_KEYS = (OPTIONAL_BOOLEAN_KEYS +
                        ProfileHelper.OPTIONAL_BOOLEAN_KEYS)
    KEY_TRANSLATIONS = {
        "first_name": "full_name",
        "last_name": "short_name",
        }

    def __init__(self, *args, **kwargs):
        super(UserHelper, self).__init__(*args, **kwargs)
        self.profile_helper = ProfileHelper(get_profile(self.subject))

    @classmethod
    def translate_key(cls, key):
        return cls.KEY_TRANSLATIONS.get(key, key)

    def field_value(self, field):
        result = super(UserHelper, self).field_value(field)
        if result is not None:
            return result
        return self.profile_helper.field_value(field)

    def field_setter(self, field, value):
        if field in ProfileHelper.INPUT_KEYS:
            self.profile_helper.field_setter(field, value)
        else:
            super(UserHelper, self).field_setter(field, value)

    def validate(self, field, value):
        if field in ProfileHelper.INPUT_KEYS:
            self.profile_helper.errors = []
            result = self.profile_helper.validate(field, value)
            self.errors += self.profile_helper.errors
            return result
        return super(UserHelper, self).validate(field, value)

    def save(self):
        self.profile_helper.save()
        super(UserHelper, self).save()

    @property
    def first_name(self):
        return self.subject.full_name

    @property
    def last_name(self):
        return self.subject.short_name


def valid_keys_note(user_type, post=False):
    keys = UserHelper.USER_INPUT_KEYS.copy()
    if post:
        keys += ProfileHelper.CORE_KEYS
    else:
        keys += ProfileHelper.CORE_PATCH_KEYS
    if not user_type or user_type == ExpertProfile.user_type:
        keys += ProfileHelper.EXPERT_KEYS
    if not user_type or user_type == EntrepreneurProfile.user_type:
        keys += ProfileHelper.ENTREPRENEUR_KEYS
    return VALID_KEYS_NOTE.format(keys)
