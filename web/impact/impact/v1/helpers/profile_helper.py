# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.core.exceptions import (
    ObjectDoesNotExist,
    ValidationError,
)
from django.core.validators import RegexValidator
from django.db.models import Subquery, OuterRef

from accelerator.models import (
    EntrepreneurProfile,
    ExpertCategory,
    ExpertProfile,
    Industry,
    MemberProfile,
    ProgramFamily,
    Program
)

from accelerator_abstract.models import (
    HIDDEN_PROGRAM_STATUS,
    UPCOMING_PROGRAM_STATUS,
    ACTIVE_PROGRAM_STATUS,
    ENDED_PROGRAM_STATUS
)

from impact.v1.helpers import (
    BOOLEAN_FIELD,
    INVALID_URL_ERROR,
    MPTT_TYPE,
    PHONE_FIELD,
    PHONE_REGEX,
    OPTIONAL_STRING_FIELD,
    TWITTER_REGEX,
    json_array,
    merge_fields,
    serialize_list_field,
    validate_boolean,
    validate_choices,
    validate_regex,
    validate_string,
    validate_url,
    FunctionalExpertiseHelper,
    IndustryHelper,
    ModelHelper,
    ProgramFamilyHelper,
)

COULD_BE_EXPERT_CHECK = "could_be_expert"
COULD_BE_NON_MEMBER_CHECK = "could_be_non_member"
IS_EXPERT_CHECK = "is_expert"
IS_NON_MEMBER_CHECK = "is_non_member"

EXPERT_DESCRIPTION = "This field exists only when user_type is 'expert'."

OPTIONAL_EXPERT_FIELD = {
    "GET": {
        "included": COULD_BE_EXPERT_CHECK,
        "description": EXPERT_DESCRIPTION,
    },
    "PATCH": {"required": False, "allowed": IS_EXPERT_CHECK},
    "POST": {"required": False, "allowed": COULD_BE_EXPERT_CHECK},
}

EXPERT_BOOLEAN_FIELD = merge_fields(OPTIONAL_EXPERT_FIELD,
                                    BOOLEAN_FIELD)

EXPERT_STRING_FIELD = merge_fields(OPTIONAL_EXPERT_FIELD,
                                   OPTIONAL_STRING_FIELD)

NON_MEMBER_STRING_FIELD = {
    "json-schema": {
        "type": "string",
    },
    "GET": {
        "included": COULD_BE_NON_MEMBER_CHECK,
        "description": ("This field exists only when user_type is "
                        "'entrepreneur' or 'expert'"),
    },
    "PATCH": {"required": False, "allowed": IS_NON_MEMBER_CHECK},
    "POST": {"required": False, "allowed": COULD_BE_NON_MEMBER_CHECK},
}

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
VALID_USER_TYPES = list(USER_TYPE_TO_PROFILE_MODEL.keys())

USER_TYPE_FIELD = {
    "json-schema": {
        "enum": VALID_USER_TYPES,
    },
    "POST": {"required": True},
}

EXPERT_PHONE_FIELD = merge_fields(
    PHONE_FIELD,
    {
        "POST": {
            "required": IS_EXPERT_CHECK,
            "description": "Required when user_type is 'expert'",
        }
    })

VALID_GENDERS = list(GENDER_TRANSLATIONS.values())

GENDER_FIELD = {
    "json-schema": {
        "enum": VALID_GENDERS,
    },
    "POST": {"required": True},
    "PATCH": {"required": False},
}

VALID_EXPERT_CATEGORIES = [
    "Executive",
    "Investor",
    "Lawyer",
    "Other",
]

EXPERT_CATEGORY_FIELD = {
    "json-schema": {
        "enum": VALID_EXPERT_CATEGORIES,
    },
    "GET": {
        "included": COULD_BE_EXPERT_CHECK,
        "description": EXPERT_DESCRIPTION,
    },
    "PATCH": {
        "required": False,
        "allowed": IS_EXPERT_CHECK,
        "description": ("Allowed only when user_type is 'expert' and "
                        "Expert Category is valid"),
    },
    "POST": {
        "required": IS_EXPERT_CHECK,
        "allowed": COULD_BE_EXPERT_CHECK,
        "description": "Required when user_type is 'expert'",
    },
}

MENTOR_TYPE_FIELD = {
    "json-schema": {
        "type": "string"
    },
    "GET": {
        "included": COULD_BE_EXPERT_CHECK,
        "description": EXPERT_DESCRIPTION,
    },
    "PATCH": {
        "required": False,
        "allowed": IS_EXPERT_CHECK,
        "description": ("Allowed only when user_type is 'expert' and "
                        "Mentor Type is valid"),
    },
    "POST": {
        "required": False,
        "allowed": IS_EXPERT_CHECK,
        "description": ("Allowed only when user_type is 'expert' and "
                        "Mentor Type is valid"),
    },
}

JUDGE_TYPE_FIELD = {
    "json-schema": {
        "type": "string"
    },
    "GET": {
        "included": COULD_BE_EXPERT_CHECK,
        "description": EXPERT_DESCRIPTION,
    },
    "PATCH": {
        "required": False,
        "allowed": IS_EXPERT_CHECK,
        "description": ("Allowed only when user_type is 'expert' and "
                        "Judge Type is valid"),
    },
    "POST": {
        "required": False,
        "allowed": IS_EXPERT_CHECK,
        "description": ("Allowed only when user_type is 'expert' and "
                        "Judge Type is valid"),
    },
}

MENTORING_SPECIALTIES_FIELD = {
    "json-schema": {
        "type": "array",
        "items": {"type": "string"},
    },
    "GET": {
        "included": COULD_BE_EXPERT_CHECK,
        "description": EXPERT_DESCRIPTION,
    },
}

EXPERT_OBJECT_ID_FIELD = {
    "GET": {
        "included": COULD_BE_EXPERT_CHECK,
    },
    "PATCH": {
        "required": False,
        "allowed": IS_EXPERT_CHECK,
    },
    "POST": {
        "required": IS_EXPERT_CHECK,
        "allowed": COULD_BE_EXPERT_CHECK,
    },
}

EXPERT_ALLOWED = "Field is allowed only when user_type is 'expert'."
EXPERT_REQUIRED = "Field is required when user_type is 'expert'."
RESOURCE_MUST_EXIST = "A matching {classname} resource must exist."
RESOURCE_WILL_BE = "Field will be an existing {classname} resource id."


def get_description(classname):
    return " ".join([EXPERT_DESCRIPTION,
                     RESOURCE_WILL_BE.format(classname=classname)])


def patch_description(classname):
    return " ".join([EXPERT_ALLOWED,
                     RESOURCE_MUST_EXIST.format(classname=classname)])


def post_description(classname):
    return " ".join([EXPERT_REQUIRED,
                     RESOURCE_MUST_EXIST.format(classname=classname)])


def object_id_field(klass):
    classname = klass.__name__
    return {
        "json-schema": {"type": "integer"},
        "GET": {"description": get_description(classname)},
        "PATCH": {"description": patch_description(classname)},
        "POST": {"description": post_description(classname)}
    }


HOME_PROGRAM_FAMILY_ID_FIELD = merge_fields(object_id_field(ProgramFamily),
                                            EXPERT_OBJECT_ID_FIELD)
PRIMARY_INDUSTRY_ID_FIELD = merge_fields(
    {"GET": {"included": False}},
    merge_fields(object_id_field(Industry),
                 EXPERT_OBJECT_ID_FIELD))

EXPERT_INDUSTRY_FIELD = {
    "json-schema": MPTT_TYPE,
    "GET": {"description": EXPERT_DESCRIPTION,
            "included": COULD_BE_EXPERT_CHECK}}

MPTT_ARRAY_FIELD = {
    "json-schema": json_array(MPTT_TYPE),
    "GET": {"included": COULD_BE_EXPERT_CHECK,
            "description": EXPERT_DESCRIPTION}}

URL_SCHEMA = "^[hH][tT][tT][pP][sS]?://"
NETLOC_ELEMENT = "([^/:@]+(:[^/@]+)?@)?([\w-]+)"
DOT = "\."
URL_REGEX = "{schema}({netloc_element}{dot})+{netloc_element}".format(
    schema=URL_SCHEMA,
    netloc_element=NETLOC_ELEMENT,
    dot=DOT
)

PERSONAL_WEBSITE_URL_FIELD = {
    "json-schema": {
        "type": "string",
        "pattern": URL_REGEX,
    },
    "PATCH": {"required": False},
    "POST": {"required": False},
}

INVALID_ID_ERROR = "Invalid {field}: Expected valid integer {classname} id"

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
    validate_choices(helper, field, user_type, user_types)
    return value


def validate_personal_website_url(helper, field, value):
    # This is essentially copied from mc.models.utils in accelerate.
    # This logic should move to a shared library once we decide to
    # do that.  See AC-4946.
    try:
        RegexValidator(regex=URL_REGEX)(value)
    except ValidationError:
        helper.errors.append(INVALID_URL_ERROR.format(field=field,
                                                      value=value))
    return value


def validate_expert_categories(helper, field, value):
    translations = dict([(category.name, category)
                         for category in ExpertCategory.objects.all()])
    result = validate_choices(helper, field, value, translations.keys())
    return translations.get(result, result)


def validate_gender(helper, field, value):
    std_value = value.lower()
    db_value = GENDER_TRANSLATIONS.get(std_value, std_value)
    return validate_choices(helper, field, db_value, VALID_GENDERS)


def validate_phone(helper, field, value):
    return validate_regex(helper, field, value, PHONE_REGEX)


def validate_twitter_handle(helper, field, value):
    return validate_regex(helper, field, value, TWITTER_REGEX)


def validate_object_id(klass, helper, field, value):
    try:
        value = int(value)
        klass.objects.get(id=value)
    except (ValueError, ObjectDoesNotExist):
        classname = klass.__name__
        helper.errors.append(INVALID_ID_ERROR.format(classname=classname,
                                                     field=field,
                                                     value=value))
    return validate_by_user_type(helper, field, value, EXPERT_ONLY)


def validate_primary_industry_id(helper, field, value):
    return validate_object_id(Industry, helper, field, value)


def validate_home_program_family_id(helper, field, value):
    return validate_object_id(ProgramFamily, helper, field, value)


def latest_distinct_program_families_dict(program_families):
    program_families_dict = {}
    for program_family in program_families:
        location, created_at = program_family[0], program_family[1]
        created_at = created_at or program_family[2]
        if location in program_families_dict.keys():
            if created_at > program_families_dict[location]:
                program_families_dict[location] = created_at
        else:
            program_families_dict[location] = created_at
    return program_families_dict


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
        "mentor_type",
        "judge_type",
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

    def find_user_type(self):
        if hasattr(self.subject, "user_type"):
            return self.subject.user_type

    @property
    def additional_industries(self):
        return serialize_list_field(self.subject,
                                    "additional_industries",
                                    IndustryHelper)

    @property
    def primary_industry(self):
        if hasattr(self.subject, "primary_industry"):
            helper = IndustryHelper(self.subject.primary_industry)
            return helper.serialize(helper.fields())

    @property
    def primary_industry_id(self):
        return None

    @property
    def functional_expertise(self):
        return serialize_list_field(self.subject,
                                    "functional_expertise",
                                    FunctionalExpertiseHelper)

    @property
    def program_families(self):
        return serialize_list_field(self.subject,
                                    "program_families",
                                    ProgramFamilyHelper)

    @property
    def expert_category(self):
        return self.field_element("expert_category", "name")

    @property
    def mentoring_specialties(self):
        return self.list_of_field_elements("mentoring_specialties", "name")

    def is_expert(self):
        if hasattr(self.subject, "user_type"):
            return self.subject.user_type == ExpertProfile.user_type

    def is_non_member(self):
        if hasattr(self.subject, "user_type"):
            return self.subject.user_type != MemberProfile.user_type

    @property
    def confirmed_user_program_families(self):
        prg = _confirmed_non_future_program_role_grant(self.subject)
        program_ids = _latest_program_id_foreach_program_family()
        program_families = list(
            prg.filter(
                program_role__program__pk__in=program_ids
            ).values_list(
                'program_role__program__program_family__name',
                'created_at',
                'person__date_joined'
            )
        )
        return latest_distinct_program_families_dict(program_families)

    @property
    def latest_active_program_location(self):
        prg = _latest_confirmed_non_future_program_role_grant(self.subject)
        if not prg:
            return None
        return prg.program_role.program.program_family.name


def _confirmed_non_future_program_role_grant(obj):
    return obj.user.programrolegrant_set.exclude(
        program_role__program__program_status__in=[
            HIDDEN_PROGRAM_STATUS,
            UPCOMING_PROGRAM_STATUS]
    ).prefetch_related(
        'program_role__program',
        'program_role__program__program_family'
    )


def _latest_confirmed_non_future_program_role_grant(obj):
    prg = _confirmed_non_future_program_role_grant(obj)
    return prg.order_by('-created_at').first()


def _latest_program_id_foreach_program_family():
    latest_program_subquery = Program.objects.filter(
        program_family=OuterRef('pk'),
        program_status__in=[ACTIVE_PROGRAM_STATUS, ENDED_PROGRAM_STATUS]
    ).order_by("-created_at").values('pk')[:1]
    return list(ProgramFamily.objects.annotate(
        latest_program=Subquery(latest_program_subquery)
    ).values_list("latest_program", flat=True))
