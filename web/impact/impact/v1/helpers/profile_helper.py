from impact.v1.helpers.model_helper import ModelHelper

VALID_GENDERS = ["f", "m", "o", "p"]

GENDER_TRANSLATIONS = {
    "female": "f",
    "male": "m",
    "other": "o",
    "prefer not to state": "p",
}

INVALID_GENDER_ERROR = ("Invalid gender: '{}'. Valid values are "
                        "'f' or 'female', 'm' or 'male', "
                        "'o' or 'other', and 'p' or 'prefer not to state'")


class ProfileHelper(ModelHelper):
    REQUIRED_KEYS = [
        "gender",
        ]
    OPTIONAL_KEYS = [
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
    INPUT_KEYS = REQUIRED_KEYS + OPTIONAL_KEYS

    READ_ONLY_KEYS = [
        "additional_industry_ids",
        "expert_category",
        "mentoring_specialties",
        "primary_industry_id",
        "updated_at",
        ]
    OUTPUT_KEYS = READ_ONLY_KEYS + INPUT_KEYS

    @property
    def additional_industry_ids(self):
        return self.subject.additional_industry_expertise.values_list(
            "id", flat=True)

    @property
    def primary_industry_id(self):
        return self.subject.primary_industry_expertise_id

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
    if not hasattr(gender, "lower"):
        return None
    gender = GENDER_TRANSLATIONS.get(gender.lower(), gender)
    if gender in VALID_GENDERS:
        return gender
    return None
