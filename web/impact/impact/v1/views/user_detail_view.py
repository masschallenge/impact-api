from django.contrib.auth import get_user_model
from rest_framework.response import Response

from impact.permissions import (
    V1APIPermissions,
)
from impact.v1.helpers import (
    USER_FIELDS,
    UserHelper,
    valid_keys_note,
)
from impact.v1.metadata import ImpactMetadata
from impact.v1.views import ImpactView


INVALID_KEYS_ERROR = "Recevied invalid key(s): {invalid_keys}."
NO_USER_ERROR = "Unable to find user with an id of {}"

User = get_user_model()


class UserDetailView(ImpactView):
    permission_classes = (
        V1APIPermissions,
    )
    metadata_class = ImpactMetadata

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def metadata(self):
        return self.options_from_fields(USER_FIELDS, ["GET", "PATCH"])

    def options(self, request, pk):
        self.user = User.objects.get(pk=pk)
        return super().options(request, pk)

    def description_check(self, check_name):
        if check_name in ["is_expert", "could_be_expert"]:
            return self.could_be_expert()
        return check_name

    def could_be_expert(self):
        return UserHelper(self.user).profile_helper.is_expert()

    def get(self, request, pk):
        self.user = User.objects.get(pk=pk)
        return Response(UserHelper(self.user).serialize())

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
