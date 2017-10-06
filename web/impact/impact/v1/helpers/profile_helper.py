import re
from impact.v1.helpers.model_helper import (
    INVALID_CHOICE_ERROR,
    ModelHelper,
    format_choices,
    validate_boolean,
    validate_choices,
    validate_regex,
    validate_string,
)
from impact.models import (
    EntrepreneurProfile,
    ExpertCategory,
    ExpertProfile,
    MemberProfile
)


GENDER_TRANSLATIONS = {
    "female": "f",
    "male": "m",
    "other": "o",
    "prefer not to state": "p",
}

USER_TYPE_TO_PROFILE_MODEL = {
    "entrepreneur": EntrepreneurProfile,
    "expert": ExpertProfile,
    "member": MemberProfile,
}
VALID_USER_TYPES = USER_TYPE_TO_PROFILE_MODEL.keys()

VALID_GENDERS = GENDER_TRANSLATIONS.values()

VALID_EXPERT_CATEGORIES = [
    "Executive",
    "Investor",
    "Lawyer",
    "Other",
]

PHONE_REGEX = re.compile(r'^[0-9x.+() -]+$')
# EMAIL_REGEX = re.compile(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$')

EXPERT_ONLY = ["expert"]
NON_MEMBER = ["expert", "entrepreneur"]


def _validate_expert_only_boolean(helper, field, value):
    validate_boolean(helper, field, value)
    return _validate_by_user_type(helper, field, value, EXPERT_ONLY)


def _validate_expert_only_string(helper, field, value):
    validate_string(helper, field, value)
    return _validate_by_user_type(helper, field, value, EXPERT_ONLY)


def _validate_non_member_string(helper, field, value):
    validate_string(helper, field, value)
    return _validate_by_user_type(helper, field, value, NON_MEMBER)


def _validate_by_user_type(helper, field, value, user_types):
    validate_string(helper, field, value)
    if helper.subject.user_type not in user_types:
        helper.errors.append(INVALID_CHOICE_ERROR.format(
                field=field,
                value=helper.subject.user_type,
                choices=format_choices(user_types)))
    return value


# def validate_email(helper, email):
#     return validate_regex(helper, email, EMAIL_REGEX, INVALID_EMAIL_ERROR)


def validate_expert_categories(helper, field, value):
    translations = dict([(category.name, category)
                         for category in ExpertCategory.objects.all()])
    return validate_choices(helper,
                            field,
                            value,
                            translations.keys(),
                            translations)


def validate_gender(helper, field, value):
    return validate_choices(helper,
                            field,
                            value,
                            VALID_GENDERS,
                            GENDER_TRANSLATIONS)


def validate_phone(helper, field, value):
    return validate_regex(helper, field, value, PHONE_REGEX)


class ProfileHelper(ModelHelper):
    VALIDATORS = {
        "bio": _validate_non_member_string,
        "company": _validate_expert_only_string,
        "expert_category": validate_expert_categories,
        "gender": validate_gender,
        "judge_interest": _validate_expert_only_boolean,
        "mentor_interest": _validate_expert_only_string,
        "office_hours_interest": _validate_expert_only_boolean,
        "office_hours_topics": _validate_expert_only_string,
        "phone": validate_phone,
        "referred_by": _validate_expert_only_string,
        "speaker_interest": _validate_expert_only_boolean,
        "speaker_topics": _validate_expert_only_string,
        "title": _validate_expert_only_string,
        }
    CORE_OPTIONAL_KEYS = [
        "facebook_url",
        "linked_in_url",
        ]
    CORE_REQUIRED_KEYS = [
        "gender",
        "user_type",
        ]
    ENTREPRENEUR_OPTIONAL_KEYS = [
        "bio",
        ]
    EXPERT_OPTIONAL_KEYS = [
        "bio",
        "office_hours_topics",
        "personal_website_url",
        "referred_by",
        "speaker_topics",
        "twitter_handle",
        ]
    EXPERT_OPTIONAL_BOOLEAN_KEYS = [
        "judge_interest",
        "mentor_interest",
        "office_hours_interest",
        "speaker_interest",
        ]
    EXPERT_REQUIRED_KEYS = [
        "company",
        "expert_category",
        "home_program_family_id",
        "phone",
        "primary_industry_id",
        "title",
        ]
    EXPERT_KEYS = (EXPERT_REQUIRED_KEYS +
                   EXPERT_OPTIONAL_BOOLEAN_KEYS +
                   EXPERT_REQUIRED_KEYS)
    ENTREPRENEUR_KEYS = ENTREPRENEUR_OPTIONAL_KEYS
    EXPERT_ONLY_KEYS = list(set(EXPERT_KEYS) - set(ENTREPRENEUR_KEYS))
    OPTIONAL_BOOLEAN_KEYS = EXPERT_OPTIONAL_BOOLEAN_KEYS
    OPTIONAL_KEYS = list(set(
            CORE_OPTIONAL_KEYS + ENTREPRENEUR_OPTIONAL_KEYS +
            EXPERT_OPTIONAL_BOOLEAN_KEYS + EXPERT_OPTIONAL_KEYS))
    OPTIONAL_STRING_KEYS = list(set(
            CORE_OPTIONAL_KEYS + ENTREPRENEUR_OPTIONAL_KEYS +
            EXPERT_OPTIONAL_KEYS))
    REQUIRED_KEYS = CORE_REQUIRED_KEYS + EXPERT_REQUIRED_KEYS
    INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS

    READ_ONLY_KEYS = [
        "additional_industry_ids",
        "mentoring_specialties",
        "updated_at",
        ]
    OUTPUT_KEYS = READ_ONLY_KEYS + INPUT_KEYS

    @property
    def additional_industry_ids(self):
        return self.subject.additional_industries.values_list(
            "id", flat=True)

#     @property
#     def primary_industry_id(self):
#         return self.subject.primary_industry_id

    @property
    def expert_category(self):
        if hasattr(self.subject, "expert_category"):
            category = self.subject.expert_category
            if category:
                return category.name

    @property
    def mentoring_specialties(self):
        if hasattr(self.subject, "mentoring_specialties"):
            specialties = self.subject.mentoring_specialties
            if specialties:
                return [specialty.name for specialty in specialties.all()]
