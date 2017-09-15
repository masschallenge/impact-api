from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from impact.permissions import (
    V1APIPermissions,
)
from impact.models import (
    BaseProfile,
    MemberProfile
)
from impact.utils import parse_date
from impact.v1.helpers import (
    ALL_USER_INPUT_KEYS,
    find_gender,
    INPUT_PROFILE_KEYS,
    INPUT_USER_KEYS,
    INVALID_GENDER_ERROR,
    REQUIRED_PROFILE_KEYS,
    REQUIRED_USER_KEYS,
    UserHelper,
)
from impact.v1.metadata import ImpactMetadata


EMAIL_EXISTS_ERROR = "User with email {} already exists"
INVALID_KEY_ERROR = "'{}' is not a valid key."
KEY_ERROR = "'{}' is required"
VALID_KEYS_NOTE = "Valid keys are: {}"
User = get_user_model()


class UserListView(LoggingMixin, APIView):
    permission_classes = (
        V1APIPermissions,
    )
    metadata_class = ImpactMetadata

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []

    def get(self, request):
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        base_url = request.build_absolute_uri().split("?")[0]
        results = self._results(limit, offset)
        result = {
            "count": len(results),
            "next": _url(base_url, limit, offset + limit),
            "previous": _url(base_url, limit, offset - limit),
            "results": results
        }
        return Response(result)

    def post(self, request):
        user_args = self._user_args(request.POST)
        profile_args = self._profile_args(request.POST)
        self._invalid_keys(request.POST)
        if self.errors:
            self.errors.append(VALID_KEYS_NOTE.format(ALL_USER_INPUT_KEYS))
            return Response(status=403, data=self.errors)
        user = _construct_user(user_args, profile_args)
        return Response({"id": user.id})

    def _user_args(self, dict):
        self._check_required_keys(dict, REQUIRED_USER_KEYS)
        results = self._copy_translated_keys(dict, INPUT_USER_KEYS)
        email = results.get("email")
        if email and User.objects.filter(email=email).exists():
            self.errors.append(EMAIL_EXISTS_ERROR.format(email))
        if "is_active" not in results:
            results["is_active"] = False
        return results

    def _check_required_keys(self, user_keys, required_keys):
        for key in set(required_keys) - set(user_keys):
            self.errors.append(KEY_ERROR.format(key))

    def _copy_translated_keys(self, user_data, keys):
        result = {}
        for key in keys:
            if key in user_data:
                target_key = UserHelper.translate(key)
                result[target_key] = user_data[key]
        return result

    def _profile_args(self, user_data):
        self._check_required_keys(user_data, REQUIRED_PROFILE_KEYS)
        results = self._copy_translated_keys(user_data, INPUT_PROFILE_KEYS)
        results["gender"] = self._find_gender(results.get("gender"))
        results["privacy_policy_accepted"] = False
        results["newsletter_sender"] = False
        return results

    def _find_gender(self, user_value):
        result = find_gender(user_value)
        if result is None:
            self.errors.append(INVALID_GENDER_ERROR.format(user_value))
        return result

    def _invalid_keys(self, user_keys):
        for key in set(user_keys) - set(ALL_USER_INPUT_KEYS):
            self.errors.append(INVALID_KEY_ERROR.format(key))

    def _results(self, limit, offset):
        queryset = User.objects.all()
        updated_at_gt = self.request.query_params.get('updated_at__gt', None)
        updated_at_lt = self.request.query_params.get('updated_at__lt', None)
        if updated_at_gt or updated_at_lt:
            queryset = _filter_profiles_by_date(
                queryset,
                updated_at_gt,
                updated_at_lt)
        return [
            UserHelper(user).serialize()
            for user in queryset[offset:offset + limit]]


def _filter_profiles_by_date(queryset, updated_at_gt, updated_at_lt):
    updated_at_gt = parse_date(updated_at_gt)
    updated_at_lt = parse_date(updated_at_lt)
    if updated_at_lt:
        queryset = queryset.filter(
            Q(expertprofile__updated_at__isnull=False) |
            Q(entrepreneurprofile__updated_at__isnull=False) |
            Q(memberprofile__updated_at__isnull=False)
        ).exclude(
            Q(expertprofile__updated_at__gte=updated_at_lt) |
            Q(entrepreneurprofile__updated_at__gte=updated_at_lt) |
            Q(memberprofile__updated_at__gte=updated_at_lt)
        )
    if updated_at_gt:
        queryset.filter(
            Q(expertprofile__updated_at__isnull=False) |
            Q(entrepreneurprofile__updated_at__isnull=False) |
            Q(memberprofile__updated_at__isnull=False)
        ).exclude(
            Q(expertprofile__updated_at__lte=updated_at_gt) |
            Q(entrepreneurprofile__updated_at__lte=updated_at_gt) |
            Q(memberprofile__updated_at__lte=updated_at_gt)
        )
    return queryset


def _url(base_url, limit, offset):
    if offset >= 0:
        return base_url + "?limit={limit}&offset={offset}".format(
            limit=limit, offset=offset)
    return None


def _construct_user(user_args, profile_args):
    user = User.objects.create_user(**user_args)
    BaseProfile.objects.create(user=user, user_type="MEMBER")
    profile_args["user"] = user
    MemberProfile.objects.create(**profile_args)
    return user
