import re
from django.core.exceptions import (
    ObjectDoesNotExist,
    ValidationError,
)
from django.core.validators import RegexValidator
from impact.v1.helpers.model_helper import (
    INVALID_CHOICE_ERROR,
    INVALID_URL_ERROR,
    ModelHelper,
    format_choices,
    validate_boolean,
    validate_choices,
    validate_regex,
    validate_string,
    validate_url,
)
from impact.models import (
    EntrepreneurProfile,
    ExpertCategory,
    ExpertProfile,
    Industry,
    MemberProfile,
    ProgramFamily,
)


GENDER_TRANSLATIONS = {
    "female": "f",
    "male": "m",
    "other": "o",
    "prefer not to state": "p",
}

USER_TYPE_TO_PROFILE_MODEL = {
    EntrepreneurProfile.user_type: EntrepreneurProfile,
    ExpertProfile.user_type: ExpertProfile,
    MemberProfile.user_type: MemberProfile,
}
VALID_USER_TYPES = USER_TYPE_TO_PROFILE_MODEL.keys()

VALID_GENDERS = GENDER_TRANSLATIONS.values()

VALID_EXPERT_CATEGORIES = [
    "Executive",
    "Investor",
    "Lawyer",
    "Other",
]

INVALID_INDUSTRY_ID_ERROR = ("Invalid {field}: "
                             "Expected valid id for an industry resource")
INVALID_PROGRAM_FAMILY_ID_ERROR = (
    "Invalid {field}: Expected valid id for an program family resource")

PHONE_REGEX = re.compile(r'^[0-9x.+() -]+$')
TWITTER_REGEX = re.compile(r'^\S+$')

EXPERT_ONLY = [ExpertProfile.user_type]
NON_MEMBER = [ExpertProfile.user_type, EntrepreneurProfile.user_type]


def validate_expert_only_boolean(helper, field, value):
    value = validate_boolean(helper, field, value)
    return validate_by_user_type(helper, field, value, EXPERT_ONLY)


def validate_expert_only_string(helper, field, value):
    validate_string(helper, field, value)
    return validate_by_user_type(helper, field, value, EXPERT_ONLY)


def validate_non_member_string(helper, field, value):
    validate_string(helper, field, value)
    return validate_by_user_type(helper, field, value, NON_MEMBER)


def validate_by_user_type(helper, field, value, user_types):
    user_type = helper.find_user_type()
    if user_type not in user_types:
        helper.errors.append(INVALID_CHOICE_ERROR.format(
                field=field,
                value=user_type,
                choices=format_choices(user_types)))
    return value


def validate_personal_website_url(helper, field, value):
    # This is essentially copied from mc.models.utils in accelerate.
    # This logic should move to a shared library once we decide to
    # do that.  See AC-4946.
    schema = "^[hH][tT][tT][pP][sS]?://"
    netloc_element = "([^/:@]+(:[^/@]+)?@)?([\w-]+)"
    dot = "\."

    url_regex = "{schema}({netloc_element}{dot})+{netloc_element}".format(
        schema=schema,
        netloc_element=netloc_element,
        dot=dot
    )

    try:
        RegexValidator(regex=url_regex)(value)
    except ValidationError:
        helper.errors.append(INVALID_URL_ERROR.format(field=field,
                                                      value=value))
    return value


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


def validate_twitter_handle(helper, field, value):
    return validate_regex(helper, field, value, TWITTER_REGEX)


def validate_primary_industry_id(helper, field, value):
    try:
        value = int(value)
        Industry.objects.get(id=value)
    except (ValueError, ObjectDoesNotExist):
        helper.errors.append(INVALID_INDUSTRY_ID_ERROR.format(field=field,
                                                              value=value))
    return validate_by_user_type(helper, field, value, EXPERT_ONLY)


def validate_home_program_family_id(helper, field, value):
    try:
        value = int(value)
        ProgramFamily.objects.get(id=value)
    except (ValueError, ObjectDoesNotExist):
        helper.errors.append(INVALID_PROGRAM_FAMILY_ID_ERROR.format(
                field=field, value=value))
    return validate_by_user_type(helper, field, value, EXPERT_ONLY)


class ProfileHelper(ModelHelper):
    VALIDATORS = {
        "bio": validate_non_member_string,
        "company": validate_expert_only_string,
        "expert_category": validate_expert_categories,
        "facebook_url": validate_url,
        "gender": validate_gender,
        "home_program_family_id": validate_home_program_family_id,
        "judge_interest": validate_expert_only_boolean,
        "linked_in_url": validate_url,
        "mentor_interest": validate_expert_only_boolean,
        "office_hours_interest": validate_expert_only_boolean,
        "office_hours_topics": validate_expert_only_string,
        "personal_website_url": validate_personal_website_url,
        "phone": validate_phone,
        "primary_industry_id": validate_primary_industry_id,
        "referred_by": validate_expert_only_string,
        "speaker_interest": validate_expert_only_boolean,
        "speaker_topics": validate_expert_only_string,
        "title": validate_expert_only_string,
        "twitter_handle": validate_twitter_handle,
        }
    CORE_OPTIONAL_KEYS = [
        "facebook_url",
        "linked_in_url",
        "personal_website_url",
        "phone",
        "twitter_handle",
        ]
    CORE_REQUIRED_KEYS = [
        "gender",
        "user_type",
        ]
    CORE_PATCH_KEYS = CORE_OPTIONAL_KEYS + ["gender"]
    ENTREPRENEUR_OPTIONAL_KEYS = [
        "bio",
        ]
    EXPERT_OPTIONAL_KEYS = [
        "bio",
        "office_hours_topics",
        "referred_by",
        "speaker_topics",
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
                   EXPERT_OPTIONAL_KEYS +
                   EXPERT_OPTIONAL_BOOLEAN_KEYS +
                   EXPERT_REQUIRED_KEYS)
    ENTREPRENEUR_KEYS = ENTREPRENEUR_OPTIONAL_KEYS
    CORE_KEYS = CORE_OPTIONAL_KEYS + CORE_REQUIRED_KEYS
    EXPERT_ONLY_KEYS = list(set(EXPERT_KEYS) -
                            set(ENTREPRENEUR_KEYS + CORE_KEYS))
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

    def find_user_type(self):
        return self.subject.user_type

    @property
    def additional_industry_ids(self):
        return self.subject.additional_industries.values_list(
            "id", flat=True)

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
