# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model

from mc.models import (
    EntrepreneurProfile,
    ExpertProfile,
)
from ...utils import get_profile
from .model_helper import (
    BOOLEAN_FIELD,
    REQUIRED_EMAIL_FIELD,
    ModelHelper,
    PK_FIELD,
    READ_ONLY_STRING_FIELD,
    REQUIRED_STRING_FIELD,
    TWITTER_FIELD,
    OPTIONAL_URL_FIELD,
    READ_ONLY_OBJECT_FIELD
)
from .validators import (
    validate_boolean,
    validate_email_address,
    validate_string,
)
from .profile_helper import (
    EXPERT_BOOLEAN_FIELD,
    EXPERT_CATEGORY_FIELD,
    EXPERT_INDUSTRY_FIELD,
    EXPERT_PHONE_FIELD,
    EXPERT_STRING_FIELD,
    GENDER_FIELD,
    HOME_PROGRAM_FAMILY_ID_FIELD,
    MENTORING_SPECIALTIES_FIELD,
    MPTT_ARRAY_FIELD,
    NON_MEMBER_STRING_FIELD,
    PERSONAL_WEBSITE_URL_FIELD,
    PRIMARY_INDUSTRY_ID_FIELD,
    ProfileHelper,
    USER_TYPE_FIELD,
)

User = get_user_model()

USER_FIELDS = {
    "id": PK_FIELD,
    "updated_at": READ_ONLY_STRING_FIELD,
    "last_login": READ_ONLY_STRING_FIELD,
    "date_joined": READ_ONLY_STRING_FIELD,
    "user_type": USER_TYPE_FIELD,
    "first_name": REQUIRED_STRING_FIELD,
    "last_name": REQUIRED_STRING_FIELD,
    "phone": EXPERT_PHONE_FIELD,
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
    "primary_industry": EXPERT_INDUSTRY_FIELD,
    "primary_industry_id": PRIMARY_INDUSTRY_ID_FIELD,
    "home_program_family_id": HOME_PROGRAM_FAMILY_ID_FIELD,
    "additional_industries": MPTT_ARRAY_FIELD,
    "gender": GENDER_FIELD,
    "expert_category": EXPERT_CATEGORY_FIELD,
    "mentoring_specialties": MENTORING_SPECIALTIES_FIELD,
    "email": REQUIRED_EMAIL_FIELD,
    "twitter_handle": TWITTER_FIELD,
    "facebook_url": OPTIONAL_URL_FIELD,
    "linked_in_url": OPTIONAL_URL_FIELD,
    "personal_website_url": PERSONAL_WEBSITE_URL_FIELD,
    "functional_expertise": MPTT_ARRAY_FIELD,
    "program_families": MPTT_ARRAY_FIELD,
    "confirmed_user_program_families": READ_ONLY_OBJECT_FIELD,
    "latest_active_program_location": READ_ONLY_STRING_FIELD,
}


class UserHelper(ModelHelper):
    VALIDATORS = {
        "email": validate_email_address,
        "first_name": validate_string,
        "is_active": validate_boolean,
        "last_name": validate_string,
        }

    model = User

    REQUIRED_KEYS = [
        "email",
        "first_name",
        "last_name",
        ]
    OPTIONAL_BOOLEAN_KEYS = [
        "is_active",
        ]
    OPTIONAL_KEYS = OPTIONAL_BOOLEAN_KEYS
    ALL_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS
    INPUT_KEYS = ALL_KEYS + ProfileHelper.INPUT_KEYS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile_helper = ProfileHelper(get_profile(self.subject))

    def field_value(self, field):
        result = super().field_value(field)
        if result is not None:
            return result
        return self.profile_helper.field_value(field)

    def field_setter(self, field, value):
        if field in ProfileHelper.INPUT_KEYS:
            self.profile_helper.field_setter(field, value)
        else:
            super().field_setter(field, value)

    def validate(self, field, value):
        if field in ProfileHelper.INPUT_KEYS:
            result = self.profile_helper.validate(field, value)
            self.errors += self.profile_helper.errors
            self.profile_helper.errors = []
            return result
        return super().validate(field, value)

    def save(self):
        if self.profile_helper:
            self.profile_helper.save()
        super().save()

    @classmethod
    def fields(cls):
        return USER_FIELDS


def valid_keys(user_type, post=False):
    keys = UserHelper.ALL_KEYS.copy()
    if post:
        keys += ProfileHelper.CORE_KEYS
    else:
        keys += ProfileHelper.CORE_PATCH_KEYS
    if not user_type or user_type == ExpertProfile.user_type:
        keys += ProfileHelper.EXPERT_KEYS
    if not user_type or user_type == EntrepreneurProfile.user_type:
        keys += ProfileHelper.ENTREPRENEUR_KEYS
    return keys
