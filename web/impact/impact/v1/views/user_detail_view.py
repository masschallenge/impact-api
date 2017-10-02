from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from impact.permissions import (
    V1APIPermissions,
)
from impact.utils import get_profile
from impact.v1.helpers import (
    INVALID_EXPERT_CATEGORY_ERROR,
    INVALID_GENDER_ERROR,
    find_gender,
    ProfileHelper,
    UserHelper,
)
from impact.v1.metadata import ImpactMetadata


INVALID_KEYS_ERROR = ("Recevied invalid key(s): {invalid_keys}. "
                      "Valid keys are: {valid_keys}.")


User = get_user_model()


class UserDetailView(LoggingMixin, APIView):
    permission_classes = (
        V1APIPermissions,
    )
    metadata_class = ImpactMetadata

    METADATA_ACTIONS = {
        "GET": UserHelper.DETAIL_GET_METADATA,
        "PATCH": UserHelper.DETAIL_PATCH_METADATA,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        return Response(UserHelper(user).serialize())

    def patch(self, request, pk):
        user = User.objects.get(pk=pk)
        helper = UserHelper(user)
        data = request.data
        invalid_keys = set(data.keys()) - set(UserHelper.INPUT_KEYS)
        if invalid_keys:
            return Response(
                status=403,
                data=INVALID_KEYS_ERROR.format(
                    invalid_keys=list(invalid_keys),
                    valid_keys=UserHelper.INPUT_KEYS))
        if "gender" in data and not find_gender(data.get("gender")):
            return Response(
                status=403,
                data=INVALID_GENDER_ERROR.format(data.get("gender")))
        for key, value in data.items():
            field = helper.translate_key(key)
            if key in UserHelper.USER_INPUT_KEYS:
                setattr(user, field, value)
            elif key in ProfileHelper.INPUT_KEYS:
                profile = get_profile(user)
                setattr(profile, field, value)
                profile.save()
        user.save()
        return Response(status=200)
