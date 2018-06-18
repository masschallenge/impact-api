# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from django.db.models import Q


from accelerator.models import (
    BaseProfile,
    ExpertProfile,
    MemberProfile,
)
from impact.utils import parse_date
from impact.v1.helpers import (
    COULD_BE_EXPERT_CHECK,
    COULD_BE_NON_MEMBER_CHECK,
    IS_EXPERT_CHECK,
    IS_NON_MEMBER_CHECK,
    ProfileHelper,
    USER_TYPE_TO_PROFILE_MODEL,
    UserHelper,
    VALID_USER_TYPES,
    validate_choices,
)
from impact.v1.views.utils import valid_keys_note
from impact.v1.views.base_list_view import BaseListView
from impact.v1.views.post_mixin import PostMixin

EMAIL_EXISTS_ERROR = "User with email {} already exists"
UNSUPPORTED_KEY_ERROR = "'{key}' is not supported for {type}"

User = get_user_model()


class UserListView(BaseListView,
                   PostMixin):
    view_name = "user"
    helper_class = UserHelper
    actions = ['GET', 'POST']

    def description_check(self, check_name):
        if check_name in [IS_EXPERT_CHECK, IS_NON_MEMBER_CHECK]:
            return False
        if check_name in [COULD_BE_EXPERT_CHECK, COULD_BE_NON_MEMBER_CHECK]:
            return True
        return check_name

    def _user_args(self, posted_data):
        self.check_required_keys(posted_data)
        results = self.copy_keys(posted_data, self.helper_class.ALL_KEYS)
        email = results.get("email")
        if email and User.objects.filter(email=email).exists():
            self.errors.append(EMAIL_EXISTS_ERROR.format(email))
        if "is_active" not in results:
            results["is_active"] = False
        self._validate_args(results, self.helper_class.VALIDATORS)
        return results

    def _check_unsupported_keys(self, user_type, user_keys, unsupported_keys):
        for key in set(unsupported_keys).intersection(set(user_keys)):
            self.errors.append(UNSUPPORTED_KEY_ERROR.format(key=key,
                                                            type=user_type))

    def _profile_args(self, user_data):
        self.check_required_keys(user_data, ProfileHelper.CORE_REQUIRED_KEYS)
        results = self.copy_keys(user_data, ProfileHelper.INPUT_KEYS)
        self.user_type = validate_choices(
            self, "user_type", results.get("user_type"), VALID_USER_TYPES)
        if self.user_type == ExpertProfile.user_type:
            self.check_required_keys(
                user_data, ProfileHelper.EXPERT_REQUIRED_KEYS)
        else:
            self._check_unsupported_keys(
                self.user_type, user_data, ProfileHelper.EXPERT_ONLY_KEYS)
            if self.user_type == MemberProfile.user_type:
                self._check_unsupported_keys(
                    self.user_type,
                    user_data,
                    ProfileHelper.ENTREPRENEUR_OPTIONAL_KEYS)
        results["newsletter_sender"] = False
        self._validate_args(results, ProfileHelper.VALIDATORS)
        return results

    def find_user_type(self):
        return self.user_type

    def _apply_filter_by_date(self, qs, after, before):
        updated_at_after = parse_date(after)
        updated_at_before = parse_date(before)
        if updated_at_after:
            qs = qs.filter(
                Q(expertprofile__updated_at__gte=updated_at_after) |
                Q(entrepreneurprofile__updated_at__gte=updated_at_after) |
                Q(memberprofile__updated_at__gte=updated_at_after))
        if updated_at_before:
            qs = qs.exclude(
                Q(expertprofile__updated_at__gt=updated_at_before) |
                Q(entrepreneurprofile__updated_at__gt=updated_at_before) |
                Q(memberprofile__updated_at__gt=updated_at_before))
        return qs

    def create_object(self, posted_data):
        user_args = self._user_args(posted_data)
        profile_args = self._profile_args(posted_data)
        self._invalid_keys(posted_data)
        if self.errors:
            valid_keys = self.helper_class.valid_keys(
                profile_args.get("user_type"),
                post=True)
            self.errors.append(valid_keys_note(valid_keys))
            return None
        return _construct_user(user_args, profile_args)


def _construct_user(user_args, profile_args):
    user = User.objects.create_user(**user_args)
    user_type = profile_args.pop("user_type")
    BaseProfile.objects.create(user=user, user_type=user_type.upper())
    profile_args["user"] = user
    klass = USER_TYPE_TO_PROFILE_MODEL[user_type]
    klass.objects.create(**profile_args)
    return user
