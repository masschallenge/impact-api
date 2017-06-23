from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from simpleuser.models import USER_KEY_TRANSLATIONS
from impact.permissions import (
    V1APIPermissions,
)
from impact.models import (
    BaseProfile,
    MemberProfile,
)
from impact.utils import user_gender


USER_KEYS = [
    "email",
    "first_name",
    "last_name",
]
PROFILE_KEYS = [
    "gender",
]
EMAIL_EXISTS_ERROR = "User with email {} already exists"
KEY_ERROR = "'{}' is required"
User = get_user_model()


class UserListView(APIView):
    permission_classes = (
        V1APIPermissions,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.errors = []

    def get(self, request):
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        base_url = request.build_absolute_uri().split("?")[0]
        result = {
            "count": User.objects.count(),
            "next": _url(base_url, limit, offset + limit),
            "previous": _url(base_url, limit, offset - limit),
            "results": _user_results(limit, offset),
            }
        return Response(result)

    def post(self, request):
        user_args = self._user_args(request.POST)
        profile_args = self._profile_args(request.POST)
        if self.errors:
            return Response(status=403, data=self.errors)
        user = _construct_user(user_args, profile_args)
        return Response({"id": user.id})

    def _user_args(self, dict):
        results = self._copy_required_keys(dict, USER_KEYS)
        email = results.get("email")
        if email and User.objects.filter(email=email).exists():
            self.errors.append(EMAIL_EXISTS_ERROR.format(email))
        return results

    def _profile_args(self, dict):
        result = self._copy_required_keys(dict, PROFILE_KEYS)
        result["privacy_policy_accepted"] = False
        result["newsletter_sender"] = False
        return result

    def _copy_required_keys(self, dict, keys):
        result = {}
        for input_key in keys:
            try:
                output_key = USER_KEY_TRANSLATIONS.get(input_key, input_key)
                result[output_key] = dict[input_key]
            except:
                self.errors.append(KEY_ERROR.format(input_key))
        return result


def _url(base_url, limit, offset):
    if offset >= 0:
        return base_url + "?limit={limit}&offset={offset}".format(
            limit=limit, offset=offset)
    return None


def _user_results(limit, offset):
    return [_serialize_user(user)
            for user in User.objects.all()[offset:offset+limit]]


def _serialize_user(user):
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.full_name,
        "last_name": user.short_name,
        "is_active": user.is_active,
        "gender": user_gender(user),
        }


def _construct_user(user_args, profile_args):
    user = User.objects.create_user(**user_args)
    base = BaseProfile.objects.create(user=user, user_type="MEMBER")
    profile_args["user"] = user
    MemberProfile.objects.create(**profile_args)
    return user

