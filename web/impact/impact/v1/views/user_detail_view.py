from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from impact.permissions import (
    V1APIPermissions,
)
from impact.v1.helpers import (
    UserHelper,
    valid_keys_note,
)
from impact.v1.metadata import ImpactMetadata

INVALID_KEYS_ERROR = "Recevied invalid key(s): {invalid_keys}."

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
        keys = set(data.keys())
        invalid_keys = keys.difference(UserHelper.INPUT_KEYS)
        if invalid_keys:
            helper.errors += [
                INVALID_KEYS_ERROR.format(invalid_keys=list(invalid_keys))]
        valid_keys = set(data.keys()).intersection(UserHelper.INPUT_KEYS)
        valid_data = {}
        for key in valid_keys:
            field = helper.translate_key(key)
            valid_data[field] = helper.validate(field, data[key])
        if helper.errors:
            return _error_response(helper)
        for field, value in valid_data.items():
            helper.field_setter(field, value)
        helper.save()
        return Response(status=204)


def _error_response(helper):
    note = valid_keys_note(helper.profile_helper.subject.user_type)
    return Response(status=403, data=helper.errors + [note])
