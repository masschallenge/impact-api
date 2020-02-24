# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

from django.contrib.auth import get_user_model
from rest_framework.response import Response

from impact.v1.helpers import (
    COULD_BE_EXPERT_CHECK,
    COULD_BE_NON_MEMBER_CHECK,
    IS_EXPERT_CHECK,
    IS_NON_MEMBER_CHECK,
    UserHelper,
    valid_keys,
)
from impact.v1.views.base_detail_view import BaseDetailView
from impact.v1.views.utils import valid_keys_note
from impact.permissions.v1_api_permissions import UserDetailViewPermission

INVALID_KEYS_ERROR = "Recevied invalid key(s): {invalid_keys}."
MISSING_PROFILE_ERROR = "User ({}) has no profile"
NO_USER_ERROR = "Unable to find user with an id of {}"

User = get_user_model()


class UserDetailView(BaseDetailView):
    view_name = "user_detail"
    helper_class = UserHelper
    actions = ["GET", "PATCH"]
    permission_classes = (
        UserDetailViewPermission,
    )

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def options(self, request, pk):
        self.user = User.objects.get(pk=pk)
        return super().options(request, pk)

    def description_check(self, check_name):
        if check_name in [IS_EXPERT_CHECK, COULD_BE_EXPERT_CHECK]:
            return self.could_be_expert()
        if check_name in [IS_NON_MEMBER_CHECK, COULD_BE_NON_MEMBER_CHECK]:
            return self.could_be_non_member()
        return check_name

    def could_be_expert(self):
        return UserHelper(self.user).profile_helper.is_expert()

    def could_be_non_member(self):
        return UserHelper(self.user).profile_helper.is_non_member()

    def patch(self, request, pk):
        self.user = User.objects.filter(pk=pk).first()
        if not self.user:
            return Response(status=404, data=NO_USER_ERROR.format(pk))
        helper = UserHelper(self.user)
        data = request.data
        keys = set(data.keys())
        invalid_keys = keys.difference(UserHelper.INPUT_KEYS)
        if invalid_keys:
            helper.errors += [
                INVALID_KEYS_ERROR.format(invalid_keys=list(invalid_keys))]
        valid_keys = set(data.keys()).intersection(UserHelper.INPUT_KEYS)
        valid_data = {}
        for key in valid_keys:
            valid_data[key] = helper.validate(key, data[key])
        if helper.errors:
            return _error_response(helper)
        for field, value in valid_data.items():
            helper.field_setter(field, value)
        helper.save()
        return Response(status=204)


def _error_response(helper):
    subject = helper.profile_helper.subject
    if subject:
        _valid_keys = valid_keys(subject.user_type)
        note = valid_keys_note(_valid_keys)
    else:
        note = MISSING_PROFILE_ERROR.format(helper.subject.id)
    return Response(status=403, data=helper.errors + [note])
