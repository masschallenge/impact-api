from impact.utils import get_profile
from impact.v1.helpers.model_helper import ModelHelper

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
        "expert_category",
        "mentoring_specialties",
        "updated_at",
        ]
    OUTPUT_KEYS = READ_ONLY_KEYS + INPUT_KEYS


def profile_field(helper, field):
    profile = get_profile(helper.subject)
    if hasattr(profile, field):
        return getattr(profile, field)
    return None


def expert_category(helper, field):
    category = helper.profile_field(field)
    if category:
        return category.name


def mentoring_specialties(helper, field):
    specialties = helper.profile_field(field)
    if specialties:
        return [specialty.name for specialty in specialties.all()]
