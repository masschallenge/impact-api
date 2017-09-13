from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from impact.permissions import (
    V1APIPermissions,
)
from impact.utils import (
    ALL_USER_RELATED_KEYS,
    INVALID_GENDER_ERROR,
    PROFILE_KEYS,
    USER_KEYS,
    KEY_TRANSLATIONS,
    find_gender,
    get_profile,
    user_gender,
)
from impact.v1.helpers import UserHelper
from impact.v1.metadata import ImpactMetadata


INVALID_KEYS_ERROR = ("Recevied invalid key(s): {invalid_keys}. "
                      "Valid keys are: {valid_keys}.")


User = get_user_model()


class UserDetailView(LoggingMixin, APIView):
    permission_classes = (
        V1APIPermissions,
    )
    metadata_class = ImpactMetadata

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        return Response(UserHelper(user).serialize())

    def patch(self, request, pk):
        user = User.objects.get(pk=pk)
        data = request.data
        invalid_keys = set(data.keys()) - set(ALL_USER_RELATED_KEYS)
        if invalid_keys:
            return Response(
                status=403,
                data=INVALID_KEYS_ERROR.format(
                    invalid_keys=list(invalid_keys),
                    valid_keys=ALL_USER_RELATED_KEYS))
        if "gender" in data and not find_gender(data.get("gender")):
            return Response(
                status=403,
                data=INVALID_GENDER_ERROR.format(data.get("gender")))
        for key, value in data.items():
            if key in KEY_TRANSLATIONS:
                setattr(user, KEY_TRANSLATIONS[key], data[key])
            elif key in USER_KEYS:
                setattr(user, key, data[key])
            elif key in PROFILE_KEYS:
                profile = get_profile(user)
                setattr(profile, key, data[key])
                profile.save()
        user.save()
        return Response(status=200)
