from impact.v1.helpers.model_helper import (
    ModelHelper,
    validate_by_role,
    validate_choices,
    validate_regex,
)
import re


GENDER_TRANSLATIONS = {
    "female": "f",
    "male": "m",
    "other": "o",
    "prefer not to state": "p",
}

VALID_GENDERS = GENDER_TRANSLATIONS.values()

INVALID_GENDER_ERROR = ("Invalid gender: '{}'. Valid values are "
                        "'f' or 'female', 'm' or 'male', "
                        "'o' or 'other', and 'p' or 'prefer not to state'")

VALID_EXPERT_CATEGORIES = [
    "Executive",
    "Investor",
    "Lawyer",
    "Other",
]

INVALID_EXPERT_CATEGORY_ERROR = ("Invalid expert category: '{}'. Valid "
                                 "values are 'Executive', 'Investor', "
                                 "'Lawyer', and 'Other'")

INVALID_BIO_ERROR = ("Invalid bio: '{}'.")
INVALID_COMPANY_ERROR = ("Invalid company: '{}'.")
INVALID_EMAIL_ERROR = ("Invalid email: '{}'.")
INVALID_OFFICE_HOURS_TOPICS_ERROR = ("Invalid office hours topics: '{}'.")
INVALID_PHONE_ERROR = ("Invalid phone: '{}'.")
INVALID_REFERRED_BY_ERROR = ("Invalid referral: '{}'.")
INVALID_SPEAKER_TOPICS_ERROR = ("Invalid speaker topics: '{}'.")
INVALID_TITLE_ERROR = ("Invalid title: '{}'.")

INVALID_IS_ACTIVE_ERROR = ("Invalid is_active: '{}'.")
INVALID_JUDGE_INTEREST_ERROR = ("Invalid judge interest: '{}'.")
INVALID_MENTOR_INTEREST_ERROR = ("Invalid mentor interest: '{}'.")
INVALID_OFFICE_HOURS_INTEREST_ERROR = ("Invalid office hours interest: '{}'.")
INVALID_SPEAKER_INTEREST_ERROR = ("Invalid speaker interest: '{}'.")

PHONE_REGEX = re.compile(r'^[0-9x.+() -]+$')
# EMAIL_REGEX = re.compile(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$')


def validate_bio(helper, bio):
    users = ["expert", "entrepreneur"]
    return validate_by_role(helper, bio, users, INVALID_BIO_ERROR)


def validate_company(helper, company):
    users = "expert"
    return validate_by_role(helper, company, users, INVALID_COMPANY_ERROR)


# def validate_email(helper, email):
#     return validate_regex(helper, email, EMAIL_REGEX, INVALID_EMAIL_ERROR)


# def validate_expert_categories(helper, expert_category):
#     return validate_choices(helper,
#                             expert_category,
#                             VALID_EXPERT_CATEGORIES,
#                             INVALID_EXPERT_CATEGORY_ERROR)


def validate_gender(helper, gender):
    if not isinstance(gender, str):
        translation = None
    else:
        translation = GENDER_TRANSLATIONS.get(gender.lower(), gender)
    return validate_choices(helper,
                            gender,
                            VALID_GENDERS,
                            INVALID_GENDER_ERROR,
                            translation)


def validate_phone(helper, phone):
    return validate_regex(helper, phone, PHONE_REGEX, INVALID_PHONE_ERROR)


def validate_title(helper, title):
    users = "expert"
    return validate_by_role(helper, title, users, INVALID_TITLE_ERROR)


def validate_office_hours_topics(helper, office_hours_topics):
    users = "expert"
    return validate_by_role(helper,
                            office_hours_topics,
                            users,
                            INVALID_OFFICE_HOURS_TOPICS_ERROR)


def validate_referred_by(helper, referred_by):
    users = "expert"
    return validate_by_role(helper,
                            referred_by,
                            users,
                            INVALID_REFERRED_BY_ERROR)


def validate_speaker_topics(helper, speaker_topics):
    users = "expert"
    return validate_by_role(helper,
                            speaker_topics,
                            users,
                            INVALID_SPEAKER_TOPICS_ERROR)


def validate_is_active(helper, is_active):
    pass


def validate_judge_interest(helper, judge_interest):
    pass


def validate_mentor_interest(helper, mentor_interest):
    pass


def validate_office_hours_interest(helper, office_hours_interest):
    pass


def validate_speaker_interest(helper, speaker_interest):
    pass


class ProfileHelper(ModelHelper):
    VALIDATORS = {
        "bio": validate_bio,
        "company": validate_company,
        # "email": validate_email,
        # "expert_category": validate_expert_categories,
        "gender": validate_gender,
        "is_active": validate_is_active,
        "judge_interest": validate_judge_interest,
        "mentor_interest": validate_mentor_interest,
        "office_hours_interest": validate_office_hours_interest,
        "office_hours_topics": validate_office_hours_topics,
        "phone": validate_phone,
        "referred_by": validate_referred_by,
        "speaker_interest": validate_speaker_interest,
        "speaker_topics": validate_speaker_topics,
        "title": validate_title,
        }
    REQUIRED_KEYS = [
        "company",
        "email",
        "expert_category",
        "gender",
        "phone",
        "primary_industry_id",
        "title",
        ]
    OPTIONAL_STRING_KEYS = [
        "bio",
        "facebook_url",
        "linked_in_url",
        "office_hours_topics",
        "personal_website_url",
        "referred_by",
        "speaker_topics",
        "twitter_handle",
        "user_type",
        ]
    OPTIONAL_BOOLEAN_KEYS = [
        "judge_interest",
        "mentor_interest",
        "office_hours_interest",
        "speaker_interest",
        ]
    OPTIONAL_KEYS = OPTIONAL_BOOLEAN_KEYS + OPTIONAL_STRING_KEYS
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

    @property
    def primary_industry_id(self):
        return self.subject.primary_industry_id

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


def find_gender(gender):
    if not isinstance(gender, str):
        return None
    gender = GENDER_TRANSLATIONS.get(gender.lower(), gender)
    if gender in VALID_GENDERS:
        return gender
    return None
